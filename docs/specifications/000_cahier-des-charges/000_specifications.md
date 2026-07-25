# Cahier des charges - AT Pro Pilotage

Version du document : `1.1`  
Date : 25 juillet 2026  
Statut : document de cadrage pour developpement par IA et revue par IA  
Projet : application dockerisee de pilotage des appels, contre-appels, tickets et activites agents

## 1. Objet du document

Ce cahier des charges decrit de maniere complete le projet de developpement **AT Pro Pilotage**. Il est destine a une IA de developpement chargee de produire l'application, puis a d'autres IA chargees de relire, corriger, challenger et ameliorer la solution.

Le document est prescriptif : lorsqu'une exigence est indiquee comme obligatoire, l'IA de developpement doit l'appliquer sauf contradiction explicite avec une contrainte technique verifiee. Toute deviation doit etre documentee dans un fichier de decision d'architecture.

## 2. Synthese du besoin

AT Pro Pilotage est une application interne permettant :

- d'importer des fichiers CSV issus des outils d'appels, de contre-appels, de tickets et d'activites agents ;
- de detecter automatiquement le type et la version des fichiers ;
- de normaliser ces fichiers vers des modeles metier canoniques ;
- d'enregistrer les donnees en base PostgreSQL sans doublons ;
- de calculer des statistiques par site, agent et periode ;
- de consulter les indicateurs depuis un CLI, une API FastAPI et une interface React ;
- de generer des rapports en **Quarkdown** a partir de la version `0.5.0`, avec rendu HTML pour la previsualisation et PDF pour la diffusion ;
- de conserver la tracabilite complete des imports, calculs et rapports.

Le projet doit etre livre sous forme d'application dockerisee, testee, documentee et exploitable.

## 3. Perimetre fonctionnel

### 3.1 Donnees sources

Les donnees sources sont des fichiers CSV hebdomadaires ou periodiques comprenant notamment :

- appels entrants ;
- appels sortants ou contre-appels ;
- tickets ;
- activites agents ;
- variations historiques de schemas ;
- un rapport hebdomadaire de reference ;
- une charte graphique DGFIP ;
- les polices Marianne.

Les fichiers sources sont des references en lecture seule. L'application doit etre capable de les lire, mais le developpement ne doit pas les modifier, les renommer, les deplacer ni les supprimer.

Lorsque les CSV de reference ne sont pas presents dans le depot de developpement, le projet doit expliciter leur mode de fourniture :

- `samples/reference/` pour des echantillons anonymises versionnables ;
- volume Docker externe pour les fichiers reels ;
- stockage documentaire hors depot pour les sources sensibles ;
- script ou procedure de copie locale non commitee ;
- jeux de test synthetiques lorsque les sources reelles ne peuvent pas etre partagees.

Le depot ne doit jamais dependre silencieusement de fichiers absents. Toute suite de tests qui exige des donnees de reference doit indiquer clairement comment les obtenir ou proposer un mode degrade avec fixtures anonymisees.

### 3.2 Actions utilisateur attendues

L'utilisateur doit pouvoir :

- deposer un ou plusieurs CSV ;
- inspecter un fichier avant import ;
- valider ou refuser un import ;
- consulter l'historique des imports ;
- voir les erreurs et avertissements ;
- gerer les agents, alias, sites et rattachements ;
- lancer ou relancer des calculs statistiques ;
- consulter les statistiques par site ou agent ;
- comparer des periodes ;
- generer un rapport ;
- modifier les textes editoriaux d'un rapport ;
- previsualiser un rapport en HTML ;
- exporter le projet source Quarkdown ;
- exporter le rapport en PDF ;
- suivre les traitements longs ;
- administrer la configuration minimale.

### 3.3 Perimetre exclu de la premiere version de production

Les elements suivants ne sont pas requis pour `1.0.0`, sauf decision contraire :

- rapprochement automatique appels/tickets ;
- prediction de charge ;
- alimentation temps reel ;
- connecteurs API vers les outils sources ;
- edition libre et non controlee du code Quarkdown par les utilisateurs fonctionnels ;
- notation individuelle ou score opaque des agents ;
- reconstitution artificielle de donnees horaires absentes.

## 4. Principes directeurs

1. Le parseur ne connait pas la base de donnees.
2. La base n'enregistre que des modeles metier valides.
3. Les statistiques ne lisent jamais directement les CSV.
4. Les rapports utilisent des statistiques enregistrees et figees.
5. Le CLI et l'API appellent les memes cas d'usage applicatifs.
6. React n'execute jamais directement de commande CLI.
7. Les imports et calculs sont idempotents.
8. Chaque donnee conserve sa provenance.
9. Chaque formule statistique est versionnee.
10. Les donnees personnelles sont minimisee, masquees ou hachees.
11. Les donnees horaires manquantes ne sont jamais inventees.
12. Les parties editoriales d'un rapport sont modifiables, les chiffres calcules ne le sont pas.
13. Les comparaisons entre agents doivent etre contextualisees et non transformees en classement simpliste.

## 5. Architecture cible

### 5.1 Vue d'ensemble

```text
Navigateur
    |
    v
Nginx
    |-------------------|
    v                   v
React               FastAPI
                        |
                        v
                 Cas d'usage Python
                        |
        |---------------|---------------|
        v               v               v
   Parseurs CSV   Moteur stats   Moteur rapports
                        |
                        v
                  PostgreSQL
                        |
                        v
                    Worker
```

### 5.2 Composants

| Composant | Technologie imposee ou recommandee | Role |
|---|---|---|
| Back-end | Python 3.12+ | Domaine, cas d'usage, parsing, statistiques, reporting |
| API | FastAPI, Pydantic | Interface HTTP/JSON |
| Base | PostgreSQL 17+ | Donnees metier, imports, statistiques, jobs, rapports |
| ORM | SQLAlchemy 2.x | Persistance |
| Migrations | Alembic | Evolution du schema |
| CLI | Typer | Exploitation et automatisation |
| CSV | Polars en priorite, csv standard si necessaire | Lecture et transformation |
| Front-end | React, TypeScript, Vite | Interface utilisateur |
| Graphiques Web | Apache ECharts ou Recharts | Tableaux de bord |
| Rapports | Quarkdown | Source de rapport, HTML, PDF |
| Worker | Python | Imports, recalculs, compilation rapports |
| Reverse proxy | Nginx | Point d'entree HTTP |
| Docker | Docker Compose | Execution locale et production |

### 5.3 Architecture back-end

Le back-end doit suivre une architecture modulaire inspiree de l'architecture hexagonale :

```text
backend/
├── pyproject.toml
├── alembic/
├── src/atpro/
│   ├── domain/
│   │   ├── agents/
│   │   ├── sites/
│   │   ├── calls/
│   │   ├── tickets/
│   │   ├── activities/
│   │   ├── statistics/
│   │   └── reports/
│   ├── application/
│   │   ├── imports/
│   │   ├── reconciliation/
│   │   ├── statistics/
│   │   ├── reporting/
│   │   └── jobs/
│   ├── parser/
│   │   ├── detection/
│   │   ├── readers/
│   │   ├── schemas/
│   │   ├── normalizers/
│   │   └── validation/
│   ├── infrastructure/
│   │   ├── database/
│   │   ├── storage/
│   │   ├── quarkdown/
│   │   └── logging/
│   ├── interfaces/
│   │   ├── api/
│   │   ├── cli/
│   │   └── worker/
│   └── shared/
└── tests/
```

Le domaine ne doit pas importer FastAPI, SQLAlchemy, Polars, Typer ni Quarkdown. Ces dependances doivent rester dans les couches d'interface ou d'infrastructure.

### 5.4 Arbitrage depot et workflow IA

Le projet cible reste une application dockerisee multi-services. Toutefois, si le depot initial est cadre par un `AGENTS.md` oriente **librairie Python reutilisable mono-package**, cet `AGENTS.md` doit etre interprete comme la regle de developpement du **coeur Python back-end** tant qu'un cadrage racine plus large n'a pas ete ajoute.

Si un fichier de specifications local, par exemple `000_specifications.md`, diverge de `AGENTS.md`, l'IA de developpement doit ouvrir une ADR ou une issue de cadrage avant de coder les lots applicatifs. La hierarchie recommandee est :

1. `AGENTS.md` pour les regles de workflow et de style imposees au depot ;
2. `000_specifications.md` ou le cahier des charges pour le perimetre fonctionnel ;
3. ADR pour les arbitrages qui reconcilient les deux.

Decision d'architecture :

- conserver la cible applicative de ce cahier des charges ;
- faire du package Python `src/atpro` le coeur reutilisable ;
- exposer CLI, API, worker et adaptateurs depuis ce package ou depuis des modules d'interface proches ;
- ajouter un cadrage complementaire pour `frontend/`, `docker/`, `docs/` et l'orchestration CI/CD ;
- ne pas reduire le projet a une simple librairie Python, sauf decision explicite documentee dans une ADR.

Si le depot impose temporairement une structure `src/<package>` sans dossiers `backend/` et `frontend/`, l'implementation doit suivre une trajectoire progressive :

```text
Phase 1 - package Python
    src/atpro/
    tests/
    pyproject.toml
    Makefile

Phase 2 - interfaces Python
    src/atpro/interfaces/cli/
    src/atpro/interfaces/api/
    src/atpro/interfaces/worker/

Phase 3 - application dockerisee
    frontend/
    docker/
    compose.yml
    nginx/

Phase 4 - monorepo complet
    backend/ ou package Python conserve a la racine selon ADR
    frontend/
    docker/
    docs/
```

Le choix final entre `backend/src/atpro` et `src/atpro` doit etre tranche par une ADR avant `0.2.0`. Dans tous les cas, les cas d'usage metier doivent rester dans le package Python et rester testables sans React ni Docker.

### 5.5 Regles de workflow par zone du depot

Le depot doit expliciter les commandes de validation par zone :

| Zone | Regles minimales |
|---|---|
| Python | `black`, `ruff`, `mypy`, `bandit`, `pytest`, build Hatchling si impose |
| API | tests unitaires, tests integration, validation OpenAPI |
| CLI | tests commandes, sorties humaines et JSON, codes retour |
| Front-end | TypeScript strict, ESLint, Prettier, Vitest, build Vite, Playwright |
| Docker | build images, healthchecks, smoke tests Compose |
| Rapports | generation projet Quarkdown, compilation HTML/PDF de test |
| Documentation | liens valides, ADR presentes, cahier des charges a jour |

`make all` peut rester la commande Python tant que le projet est au stade package. Avant l'arrivee de `frontend/` et `docker/`, une commande racine plus large doit etre creee, par exemple :

```bash
make check-python
make check-frontend
make check-docker
make check-reports
make all
```

`make all` doit progressivement devenir la validation complete du produit, pas seulement du package Python.

Si `AGENTS.md` impose des contraintes Python particulieres, par exemple `1 classe = 1 fichier`, build Hatchling ou integration inter-librairies par reference Git, elles s'appliquent au package `atpro` jusqu'a modification explicite du workflow. Les modules front-end et Docker doivent recevoir des regles equivalentes, mais adaptees a leur ecosysteme.

Si `AGENTS.md` ou le `Makefile` impose un seuil de couverture global, par exemple `--cov-fail-under=95`, ce seuil prevaut sur les objectifs par zone tant qu'aucune ADR ne module explicitement la regle. Les seuils inferieurs indiques dans ce cahier des charges sont alors des sous-objectifs d'analyse, pas des seuils de validation CI.

## 6. Modeles metier canoniques

### 6.1 Enumerations principales

```python
class PeriodType(StrEnum):
    HOUR = "hour"
    DAY = "day"
    WEEK = "week"
    MONTH = "month"
    QUARTER = "quarter"
    YEAR = "year"
    CUSTOM = "custom"


class ScopeType(StrEnum):
    SITE = "site"
    AGENT = "agent"


class ImportFileType(StrEnum):
    INCOMING_CALLS = "incoming_calls"
    OUTGOING_CALLS = "outgoing_calls"
    TICKETS = "tickets"
    AGENT_ACTIVITIES = "agent_activities"
    UNKNOWN = "unknown"
```

### 6.2 Referentiel sites

`Site` represente un site de rattachement ou de traitement.

Champs minimaux :

- `id` ;
- `code` ;
- `name` ;
- `normalized_name` ;
- `active` ;
- `created_at` ;
- `updated_at`.

### 6.3 Referentiel agents

`Agent` represente une personne physique normalisee.

Champs minimaux :

- `id` ;
- `first_name` ;
- `last_name` ;
- `display_name` ;
- `normalized_identity` ;
- `active` ;
- `created_at` ;
- `updated_at`.

### 6.4 Alias agents

`AgentAlias` permet de rapprocher les noms observes dans les sources :

- `MAZIERE Pascale` ;
- `Pascale MAZIERE` ;
- variantes avec accents ;
- variantes sans accents ;
- noms mal encodes ;
- tirets et espaces multiples.

Champs minimaux :

- `id` ;
- `agent_id` ;
- `raw_alias` ;
- `normalized_alias` ;
- `source` ;
- `confidence` ;
- `validated_by_user` ;
- `created_at`.

### 6.5 Rattachements agents/sites

`AgentSiteAssignment` doit etre date. Un agent peut changer de site.

Champs minimaux :

- `id` ;
- `agent_id` ;
- `site_id` ;
- `start_date` ;
- `end_date` nullable ;
- `source` ;
- `created_at`.

Regle : lors de l'attribution d'une activite a un site, utiliser le rattachement valide a la date de l'evenement.

### 6.6 Appels

Les exports d'appels comportent plusieurs lignes par appel, notamment une ligne pour la duree de communication et une ligne pour la duree de mise en garde. Un meme identifiant d'appel peut aussi correspondre a plusieurs segments.

`Call` represente l'appel global.

Champs minimaux :

- `id` ;
- `source_system` ;
- `external_call_id` ;
- `direction` : entrant ou sortant ;
- `started_at` ;
- `ended_at` ;
- `caller_hash` ;
- `callee_hash` ;
- `flow` ;
- `service` ;
- `global_result` ;
- `source_import_batch_id` ;
- `created_at` ;
- `updated_at`.

`CallSegment` represente une presentation ou une participation d'agent.

Champs minimaux :

- `id` ;
- `call_id` ;
- `segment_index` ;
- `agent_id` nullable si non rapproche ;
- `raw_agent_name` ;
- `site_id` nullable ;
- `started_at` ;
- `ended_at` ;
- `talk_duration_seconds` ;
- `hold_duration_seconds` ;
- `qualification_category` ;
- `qualification_reason` ;
- `hangup_origin` ;
- `source_row_numbers` ;
- `line_fingerprint` ;
- `created_at`.

Regle obligatoire : ne jamais dedoublonner les appels uniquement sur `ID de l'appel` en supprimant les lignes de mesures. Il faut consolider les mesures.

### 6.7 Tickets

`Ticket` represente un ticket metier.

Champs minimaux :

- `id` ;
- `source_system` ;
- `external_ticket_id` ;
- `form_id` ;
- `form_type` ;
- `created_at` ;
- `taken_at` ;
- `resolved_at` ;
- `closed_at` ;
- `channel` ;
- `nature` ;
- `ticket_type` ;
- `status` ;
- `contact_type` ;
- `contact_identifier_hash` ;
- `creation_domain` ;
- `distribution_site_id` ;
- `resolution_group_level` ;
- `business_domain` ;
- `owner_agent_id` ;
- `qualification_agent_id` ;
- `qualification_site_id` ;
- `resolution_agent_id` ;
- `resolution_site_id` ;
- `closure_agent_id` ;
- `source_import_batch_id` ;
- `line_fingerprint` ;
- `created_at_db` ;
- `updated_at_db`.

Definitions metier initiales :

- tickets recus : rattachement au `Site Repartition Ticket` ;
- tickets qualifies : rattachement au `Site Agent Qualification Ticket` ;
- tickets resolus : rattachement au `Site Agent Resolution Ticket` ;
- tickets clotures : date de cloture et agent/site de cloture si disponible.

### 6.8 Activites agents

`AgentDailyActivity` represente une activite journaliere normalisee.

Champs minimaux :

- `id` ;
- `agent_id` nullable si non rapproche ;
- `raw_agent_name` ;
- `site_id` nullable ;
- `activity_date` ;
- `received_calls` ;
- `answered_calls` ;
- `outgoing_calls` ;
- `transferred_in_calls` ;
- `handled_calls_total` ;
- `transferred_calls` ;
- `hold_count` ;
- `consultation_count` ;
- `login_time_seconds` ;
- `ready_time_seconds` ;
- `not_ready_time_seconds` ;
- `phone_time_seconds` ;
- `incoming_talk_time_seconds` ;
- `outgoing_talk_time_seconds` ;
- `after_call_work_seconds` ;
- `rona_time_seconds` ;
- `hold_duration_seconds` ;
- `answer_rate` ;
- `hold_rate` ;
- `raw_metrics` ;
- `source_import_batch_id` ;
- `line_fingerprint` ;
- `created_at`.

Les formats large et long doivent etre transformes vers ce modele commun.

## 7. Parseurs CSV

### 7.1 Objectif

Le lot de parsing transforme les fichiers CSV en objets metier normalises, sans acces a PostgreSQL.

Resultat attendu :

```python
@dataclass(frozen=True)
class ParseResult:
    file_metadata: ImportedFileMetadata
    detected_type: ImportFileType
    schema_version: str
    records: tuple[DomainModel, ...]
    warnings: tuple[ImportWarning, ...]
    errors: tuple[ImportError, ...]
```

### 7.2 Contraintes observees dans les sources

Les parseurs doivent gerer :

- separateur `;` ;
- guillemets autour des champs dans certains fichiers ;
- encodages UTF-8 et Windows-1252 ;
- caracteres mal decodes dans certains fichiers ;
- dates au format `dd/MM/yyyy HH:mm:ss` ;
- dates au format `dd-MM-yy HH:mm:ss` ;
- dates au format `yyyy/MM/dd` ;
- dates en francais comme `15 juin 2026` ;
- durees au format secondes entieres ;
- durees au format `HH:MM:SS` ;
- pourcentages avec virgule decimale ;
- colonnes dans un ordre variable ;
- fichier avec faute dans le nom, par exemple `appels sotants.csv` ;
- tickets avec schemas d'environ 40 colonnes puis 28 colonnes ;
- activites agents en format large puis format long ;
- appels entrants et sortants au format long par mesures.

### 7.3 Detection du type de fichier

La detection ne doit pas reposer uniquement sur le nom du fichier. Elle doit utiliser :

- les colonnes presentes ;
- les noms de mesures ;
- les types de valeurs ;
- la presence d'identifiants metier ;
- les signatures connues ;
- la version de schema detectee.

Exemples de signatures :

| Type | Colonnes ou indices attendus |
|---|---|
| Appels entrants | `ID de l'appel`, `Numero appelant`, `Numero appele`, `Nom de l'agent`, `Debut d'appel`, `Fin d'appel`, `Flux`, `Service`, `Noms de mesures`, `Valeurs de mesures` |
| Appels sortants | `ID de l'appel`, `Numero appele`, `Nom de l'agent`, `Debut d'appel`, `Fin d'appel`, `Noms de mesures`, `Valeurs de mesures`, absence possible de numero appelant |
| Tickets | `Numero Ticket`, `Date-Heure Creation Ticket`, `Statut Ticket`, `Site Repartition Ticket`, agents de qualification/resolution/cloture |
| Activites large | `Periode`, `Agent / Groupe Agent`, `Appels decroches`, `Appels recus`, `Temps login`, `Temps pret` |
| Activites long | `Periode`, `Agent / Groupe Agent`, `Noms de mesures`, `Valeurs de mesures` |

### 7.4 Consolidation des appels

Pour chaque groupe de lignes d'appel :

1. regrouper par identifiant d'appel, agent, debut, fin et informations de segment ;
2. extraire les mesures `Duree de communication` et `Duree de mise en garde` ;
3. creer ou completer un `Call` global ;
4. creer un ou plusieurs `CallSegment` ;
5. conserver les numeros de lignes sources ;
6. detecter les cas incoherents.

Cas a signaler :

- mesure inconnue ;
- duree negative ;
- fin avant debut ;
- meme segment avec deux valeurs contradictoires ;
- appel sans agent ;
- appel multi-segments ;
- appel avec duree totale nulle ;
- agent non reconnu ;
- flux ou service inconnu.

### 7.5 Parsing des tickets

Le parseur tickets doit supporter au minimum :

- schema long avec colonnes contact, priorite, groupes et domaines ;
- schema reduit sans certaines colonnes ;
- champs vides ;
- dates manquantes ;
- tickets ouverts sans resolution ni cloture ;
- differents canaux, dont telephone et formulaire ;
- sites de repartition, qualification et resolution distincts.

Les adresses email et numeros de telephone ne doivent pas etre stockes en clair dans les modeles analytiques.

### 7.6 Parsing des activites agents

Format large :

- une ligne par agent et par jour ;
- une colonne par indicateur.

Format long :

- une ligne par agent, jour et mesure ;
- colonnes `Noms de mesures` et `Valeurs de mesures`.

Le parseur doit reconstruire un objet `AgentDailyActivity` par agent et par jour.

### 7.7 Normalisation des identites

La normalisation doit :

- supprimer les espaces multiples ;
- uniformiser la casse ;
- retirer ou comparer sans accents ;
- gerer les tirets ;
- reconnaitre `NOM Prenom` et `Prenom NOM` ;
- conserver la valeur brute ;
- produire une valeur normalisee ;
- signaler les rapprochements ambigus.

Les rapprochements automatiques doivent avoir un seuil de confiance configurable. Les cas ambigus doivent etre exposes a l'utilisateur.

### 7.8 Validation du parsing

Chaque parseur doit produire :

- nombre de lignes lues ;
- nombre de lignes acceptees ;
- nombre de lignes rejetees ;
- nombre de lignes ignorees ;
- erreurs bloquantes ;
- avertissements non bloquants ;
- periode detectee ;
- schema detecte ;
- empreinte SHA-256 du fichier ;
- empreinte normalisee des lignes.

## 8. Persistance PostgreSQL idempotente

### 8.1 Objectif

Enregistrer les modeles canoniques dans PostgreSQL sans doublons, meme en cas de reimport d'un fichier identique ou partiellement chevauchant.

### 8.2 Docker PostgreSQL

PostgreSQL doit etre lance via Docker Compose avec :

- volume persistant ;
- utilisateur applicatif dedie ;
- mot de passe fourni par variable d'environnement ou secret ;
- healthcheck ;
- reseau interne ;
- sauvegardes exportables.

### 8.3 Tables de tracabilite

`import_batch` :

- `id` ;
- `original_filename` ;
- `stored_filename` ;
- `sha256` ;
- `detected_type` ;
- `schema_version` ;
- `period_start` ;
- `period_end` ;
- `status` ;
- `started_at` ;
- `completed_at` ;
- `created_by` ;
- `accepted_rows` ;
- `rejected_rows` ;
- `ignored_rows` ;
- `inserted_records` ;
- `updated_records` ;
- `skipped_records` ;
- `error_summary`.

`import_rejected_row` :

- `id` ;
- `import_batch_id` ;
- `row_number` ;
- `severity` ;
- `error_code` ;
- `message` ;
- `masked_payload` ;
- `created_at`.

### 8.4 Contraintes d'unicite

Les contraintes doivent etre portees par PostgreSQL, pas seulement par Python.

| Donnee | Cle d'unicite minimale |
|---|---|
| Fichier | `sha256` |
| Agent alias | `normalized_alias` |
| Site | `normalized_name` |
| Ticket | `source_system`, `external_ticket_id` |
| Appel | `source_system`, `external_call_id` |
| Segment d'appel | `call_id`, `segment_index` ou empreinte de segment |
| Activite agent | `agent_id`, `raw_agent_name`, `activity_date`, `line_fingerprint` |
| Statistique | `scope_type`, `scope_id`, `period_type`, `period_start`, `period_end`, `metric_code`, `calculation_version` |
| Rapport | `report_id`, `revision` |

### 8.5 Stratégie d'ecriture

L'import doit etre transactionnel :

1. creer un `import_batch` en statut `running` ;
2. inserer ou rapprocher les referentiels ;
3. inserer les donnees metier avec `ON CONFLICT` ;
4. enregistrer les rejets ;
5. invalider les statistiques concernees ;
6. passer le lot a `completed`, `completed_with_warnings` ou `failed`.

En cas d'erreur bloquante, la transaction metier doit etre annulee et le lot marque comme echoue.

### 8.6 Politique de mise a jour

Lorsqu'une donnee avec la meme cle metier existe deja :

- si le contenu normalise est identique : ignorer ;
- si le contenu differe : appliquer la politique configuree ;
- conserver l'ancienne et la nouvelle empreinte ;
- tracer les champs modifies ;
- invalider les statistiques impactees.

Politique par defaut : mise a jour autorisee pour les champs evolutifs de tickets, interdite ou manuelle pour les appels historiques, configurable pour les activites agents.

La politique de mise a jour doit etre formalisee dans une configuration applicative versionnee. Les niveaux de configuration autorises sont :

- global : politique par defaut de l'application ;
- type de donnee : tickets, appels, activites agents, referentiels ;
- type d'import : dry-run, import manuel, import planifie ;
- site : uniquement si un besoin metier explicite le justifie ;
- execution ponctuelle : surcharge explicite via CLI ou API avec trace d'audit.

Pour les activites agents, la politique par defaut est :

- meme agent, meme date, meme empreinte normalisee : ignorer ;
- meme agent et meme date avec valeurs differentes : creer une alerte de conflit ;
- remplacement automatique interdit tant qu'une regle de priorite n'est pas definie ;
- remplacement manuel possible par `pilot` ou `functional_admin`, avec justification obligatoire.

Toute politique active doit etre visible dans l'historique d'import afin qu'une IA de revue puisse expliquer pourquoi une donnee a ete inseree, ignoree ou remplacee.

### 8.7 Rollback d'import

Une annulation controlee doit permettre :

- de desactiver un lot ;
- de supprimer ou marquer comme annulees les donnees provenant exclusivement de ce lot ;
- de conserver les donnees egalement apportees par d'autres lots ;
- d'invalider les statistiques ;
- de journaliser l'operation.

## 9. Statistiques

### 9.1 Objectif

Calculer et stocker des indicateurs par :

- site ;
- agent ;
- heure ;
- jour ;
- semaine ISO ;
- mois ;
- trimestre ;
- annee ;
- periode personnalisee.

### 9.2 Principe d'agregation

```text
Donnees metier
    |
    |-- Agregats horaires
    |
    |-- Agregats journaliers
            |
            |-- Hebdomadaires
            |-- Mensuels
            |-- Trimestriels
            |-- Annuels
            |-- Personnalises
```

Les statistiques superieures peuvent etre calculees depuis les statistiques journalieres, mais les donnees finales doivent etre enregistrees pour accelerer les consultations et les rapports.

### 9.3 Tables statistiques

Solution recommandee :

- `statistic_calculation_run` ;
- `statistic_value` ;
- `statistic_invalidation`.

`statistic_value` doit permettre de stocker des valeurs numeriques et JSON :

- `id` ;
- `scope_type` ;
- `scope_id` ;
- `period_type` ;
- `period_start` ;
- `period_end` ;
- `metric_code` ;
- `metric_label` ;
- `metric_family` ;
- `numeric_value` ;
- `text_value` ;
- `json_value` ;
- `unit` ;
- `calculation_version` ;
- `source_data_fingerprint` ;
- `quality_status` ;
- `calculated_at`.

### 9.4 Versionnement des formules

Chaque indicateur doit porter une version :

- `calls.presented.v1` ;
- `calls.answered.v1` ;
- `calls.answer_rate.v1` ;
- `calls.hourly_phone_load.v1` ;
- `tickets.received.v1` ;
- `tickets.resolution_delay.v1` ;
- `activities.login_time.v1`.

Toute modification de formule doit :

- incrementer la version ;
- documenter le changement ;
- permettre le recalcul ;
- ne pas modifier silencieusement les rapports publies.

### 9.5 Indicateurs d'appels

Indicateurs minimaux :

- appels presentes ;
- appels repondus ;
- appels non repondus ;
- taux de decroche ;
- appels sortants ;
- contre-appels ;
- temps total de communication ;
- duree moyenne ;
- duree mediane ;
- duree P90 ;
- temps total de mise en garde ;
- taux de mise en garde ;
- nombre d'appels transferes ;
- nombre de segments ;
- nombre moyen de segments par appel ;
- repartition par heure ;
- repartition par jour ;
- repartition par flux ;
- repartition par service.

Formule de base :

```text
taux_decroche = appels_repondus / appels_presentes
```

Si le denominateur est nul, la valeur doit etre `null` et non `0`.

### 9.6 Indicateurs de tickets

Indicateurs minimaux :

- tickets recus ;
- tickets qualifies ;
- tickets resolus ;
- tickets clotures ;
- tickets ouverts en fin de periode si les donnees le permettent ;
- taux de resolution ;
- taux de cloture ;
- delai moyen de resolution ;
- delai median de resolution ;
- delai P90 de resolution ;
- resolution le jour meme ;
- repartition par canal ;
- repartition par nature ;
- repartition par type ;
- repartition par statut ;
- repartition par domaine metier.

Attention : un backlog exact a une date donnee exige de connaitre tous les tickets encore ouverts a cette date, y compris ceux crees avant la periode analysee. Si cette condition n'est pas remplie, l'application doit afficher une limitation de qualite.

### 9.7 Indicateurs d'activites agents

Indicateurs minimaux :

- temps connecte ;
- temps pret ;
- temps non pret ;
- temps telephone ;
- temps RONA ;
- temps post-appel ;
- appels recus ;
- appels decroches ;
- appels sortants ;
- appels traites ;
- appels transferes ;
- consultations ;
- mises en garde ;
- taux de decroche issu du fichier activite ;
- taux de mise en garde issu du fichier activite.

### 9.8 Charge horaire

La charge telephonique horaire doit etre calculee a partir des appels et segments horodates.

Si un segment traverse plusieurs heures, sa duree doit etre repartie proportionnellement au chevauchement :

```text
part_heure = duree_segment_intersectant_l_heure / duree_totale_segment
```

Les compteurs d'appels peuvent etre :

- rattaches a l'heure de debut ;
- ou proratises selon la duree selon l'indicateur.

Le choix doit etre documente par indicateur.

### 9.9 Occupation horaire complete

Avec les sources actuelles, les fichiers d'activites agents fournissent des totaux journaliers, pas des changements d'etat horodates. L'application ne doit donc pas inventer :

- temps connecte heure par heure ;
- temps pret heure par heure ;
- temps non pret heure par heure ;
- temps RONA heure par heure.

Ces indicateurs horaires complets ne seront disponibles que si un futur fichier source contient des etats agents horodates.

### 9.10 Invalidation et recalcul

Lorsqu'un import ajoute, modifie ou annule des donnees, l'application doit invalider :

- les heures concernees ;
- les jours concernes ;
- les semaines ISO concernees ;
- les mois concernes ;
- les trimestres concernes ;
- les annees concernees ;
- les periodes personnalisees materialisees si elles existent.

Exemple :

```text
Import du 17 juin 2026
-> invalidation du 17 juin
-> invalidation de la semaine ISO correspondante
-> invalidation de juin 2026
-> invalidation du trimestre 2 2026
-> invalidation de l'annee 2026
```

### 9.11 Fuseaux horaires et changements d'heure

Les horodatages metier doivent etre interpretes dans le fuseau local de l'activite, par defaut `Europe/Paris`, sauf indication contraire de la source.

Regles obligatoires :

- conserver en base les instants en UTC pour les colonnes techniques et les comparaisons ;
- conserver le fuseau source ou le fuseau d'interpretation dans les metadonnees d'import ;
- utiliser des objets date/heure conscients du fuseau horaire ;
- gerer explicitement les passages heure d'ete/heure d'hiver ;
- tester les cas de journees de 23 h et 25 h ;
- calculer les semaines, mois, trimestres et annees dans le calendrier local metier ;
- documenter tout fichier source qui ne porte pas d'information de fuseau.

La repartition proportionnelle de la charge horaire doit utiliser les intervalles reels en temps local metier, puis stocker le resultat avec une cle de periode non ambigue.

## 10. Rapports Quarkdown a partir de v0.5.0

### 10.1 Decision d'architecture

A partir de la version `0.5.0`, les rapports doivent etre generes en **Quarkdown**.

Le format source editable et archive est le projet Quarkdown. Les formats produits sont :

- HTML pour la previsualisation Web ;
- PDF pour la diffusion ;
- texte brut uniquement si besoin technique.

Le moteur Python ne doit pas generer directement le PDF final. Il doit produire un projet Quarkdown autonome, puis appeler le compilateur Quarkdown dans un environnement controle.

### 10.2 Capacites Quarkdown a utiliser

Selon la documentation officielle Quarkdown :

- `paged` est adapte aux documents pagines et aux PDF ;
- la compilation standard utilise `quarkdown c main.qd` ;
- l'export PDF utilise `quarkdown c main.qd --pdf` ;
- les projets multi-fichiers sont supportes ;
- les fonctions personnalisees `.function` permettent de creer des composants reutilisables ;
- les options CLI permettent de choisir la sortie, le dossier de sortie, le mode strict, le timeout et les permissions.

References :

- <https://quarkdown.com/wiki/quickstart/>
- <https://quarkdown.com/wiki/cli-options/>

### 10.2.1 Spike technique Quarkdown obligatoire

Quarkdown etant un outil jeune et moins repandu que les chaines classiques de generation documentaire, un spike technique doit etre realise au debut du lot `0.5.0`, avant de construire toute la structure definitive des rapports.

Le spike doit verifier concretement :

- installation reproductible dans une image Docker ;
- compilation HTML d'un document `paged` minimal ;
- compilation PDF ;
- utilisation de fichiers multiples ;
- inclusion de donnees CSV ;
- inclusion d'images ou graphiques generes ;
- theme ou CSS personnalise ;
- fonctionnement du mode strict ;
- parametrage du timeout ;
- comportement des permissions de lecture ;
- execution sans reseau ;
- execution avec utilisateur non-root ;
- recuperation des logs ;
- message d'erreur exploitable en cas d'echec ;
- compatibilite avec les polices Marianne si elles sont disponibles.

Livrables du spike :

- `docs/architecture/adr/ADR-XXXX-quarkdown-reporting.md` ;
- un projet Quarkdown minimal versionne dans les tests ou fixtures ;
- un test CI qui compile HTML et PDF ;
- une decision explicite : continuer avec Quarkdown, restreindre son usage, ou prevoir une solution de secours.

Si le spike invalide une hypothese de ce cahier des charges, la section rapports doit etre corrigee avant la suite du lot `0.5.0`.

### 10.3 Structure d'un projet rapport

Chaque rapport doit etre genere comme un dossier autonome :

```text
report-<uuid>/
├── main.qd
├── report.json
├── data/
│   ├── summary.csv
│   ├── daily_statistics.csv
│   ├── hourly_statistics.csv
│   ├── agent_statistics.csv
│   └── comparisons.csv
├── components/
│   ├── metadata.qd
│   ├── cover.qd
│   ├── executive-summary.qd
│   ├── indicator-card.qd
│   ├── data-quality.qd
│   ├── tables.qd
│   ├── charts.qd
│   └── footer.qd
├── sections/
│   ├── introduction.qd
│   ├── tickets.qd
│   ├── calls.qd
│   ├── occupancy.qd
│   ├── agents.qd
│   ├── comparisons.qd
│   └── conclusion.qd
├── assets/
│   ├── logo.svg
│   ├── charts/
│   └── fonts/
└── output/
    ├── report.html
    └── report.pdf
```

### 10.4 Contenu minimal de `main.qd`

Le fichier racine doit inclure :

- type de document `paged` ;
- nom du document ;
- auteurs ou service emetteur ;
- theme AT Pro ;
- composants ;
- sections ;
- table des matieres si utile ;
- numerotation ;
- pieds de page ;
- references aux donnees figees.

### 10.5 Donnees figees

Un rapport ne doit jamais relire directement PostgreSQL pendant sa compilation Quarkdown.

Le generateur doit creer un instantane comprenant :

- metadonnees du rapport ;
- statistiques utilisees ;
- donnees de qualite ;
- comparaisons ;
- tableaux ;
- chemins des graphiques ;
- version des calculs ;
- empreinte des donnees.

### 10.6 Modeles de rapports

Modeles requis :

- rapport site journalier ;
- rapport site hebdomadaire ;
- rapport site mensuel ;
- rapport site trimestriel ;
- rapport site annuel ;
- rapport site periode personnalisee ;
- rapport agent journalier ;
- rapport agent hebdomadaire ;
- rapport agent mensuel ;
- rapport agent trimestriel ;
- rapport agent annuel ;
- rapport agent periode personnalisee.

Variantes :

- complet ;
- synthetique ;
- avec comparaison ;
- sans comparaison ;
- sans analyse individuelle.

### 10.7 Structure du rapport site

1. Page de couverture.
2. Metadonnees et historique.
3. Synthese executive.
4. Qualite et completude des donnees.
5. Activite tickets.
6. Activite telephonique.
7. Charge horaire.
8. Activite des agents.
9. Comparaisons.
10. Faits marquants.
11. Points de vigilance.
12. Conclusion.
13. Annexes methodologiques.

### 10.8 Structure du rapport agent

1. Page de couverture.
2. Metadonnees.
3. Synthese de periode.
4. Activite telephonique.
5. Activite tickets.
6. Charge journaliere et horaire.
7. Temps d'activite.
8. Evolution par rapport a la periode precedente.
9. Positionnement contextualise dans le collectif.
10. Commentaire editorial.
11. Annexes methodologiques.

### 10.9 Edition des rapports

L'utilisateur fonctionnel peut modifier :

- introduction ;
- faits marquants ;
- commentaires ;
- points de vigilance ;
- conclusion ;
- recommandations.

Il ne peut pas modifier :

- chiffres calcules ;
- tableaux statistiques ;
- graphiques produits depuis les statistiques ;
- version de calcul ;
- empreinte des donnees.

Un mode expert d'edition Quarkdown peut etre envisage apres `1.0.0`, mais il doit etre reserve a un role specifique.

### 10.10 Compilation securisee

La compilation Quarkdown doit etre executee :

- dans un conteneur isole ;
- avec utilisateur non-root ;
- sans acces reseau par defaut ;
- avec acces limite au repertoire du projet rapport ;
- sans permission globale de lecture ;
- avec timeout ;
- avec limite memoire et CPU ;
- en mode strict lorsque possible ;
- avec logs conserves.

Les contenus editoriaux saisis par l'utilisateur doivent etre echappes ou injectes de maniere a empecher l'execution de fonctions Quarkdown arbitraires.

### 10.11 Tables rapports

`report` :

- `id` ;
- `scope_type` ;
- `scope_id` ;
- `period_type` ;
- `period_start` ;
- `period_end` ;
- `template_code` ;
- `template_version` ;
- `calculation_version` ;
- `status` ;
- `project_path` ;
- `html_path` ;
- `pdf_path` ;
- `project_fingerprint` ;
- `generated_at` ;
- `validated_at` ;
- `published_at` ;
- `created_by`.

`report_revision` :

- `id` ;
- `report_id` ;
- `revision_number` ;
- `editorial_content` ;
- `data_fingerprint` ;
- `source_fingerprint` ;
- `compile_logs` ;
- `html_path` ;
- `pdf_path` ;
- `created_by` ;
- `created_at`.

## 11. CLI

### 11.1 Objectif

Le CLI doit permettre d'exploiter toute l'application sans interface Web. Il doit etre utilisable dans Docker.

### 11.2 Commandes fichiers

```bash
atpro file inspect <path>
atpro file validate <path>
atpro file preview <path>
```

### 11.3 Commandes import

```bash
atpro import run <file-or-directory>
atpro import run <file-or-directory> --dry-run
atpro import list
atpro import show <import-id>
atpro import errors <import-id>
atpro import rollback <import-id>
```

### 11.4 Commandes agents et sites

```bash
atpro agent list
atpro agent show <agent-id>
atpro agent aliases <agent-id>
atpro agent add-alias <agent-id> "<alias>"

atpro site list
atpro site show <site-id>
atpro assignment add <agent-id> <site-id> --from 2026-01-01
```

### 11.5 Commandes statistiques

```bash
atpro stats compute --scope site --site <site-id> --period week --date 2026-06-15
atpro stats rebuild --from 2026-01-01 --to 2026-06-30
atpro stats show --scope agent --agent <agent-id> --period month --date 2026-06-01
atpro stats invalidate --from 2026-06-01 --to 2026-06-30
```

### 11.6 Commandes rapports

```bash
atpro report generate --scope site --site <site-id> --period week --date 2026-06-15 --renderer html,pdf
atpro report compile <report-id>
atpro report preview <report-id>
atpro report source <report-id>
atpro report export <report-id> --format qd
atpro report export <report-id> --format pdf
atpro report list
atpro report show <report-id>
atpro report list-templates
atpro report validate-template <template-code>
```

### 11.7 Commandes jobs et maintenance

```bash
atpro job list
atpro job show <job-id>
atpro job retry <job-id>
atpro job cancel <job-id>

atpro db migrate
atpro db status
atpro health
atpro version
```

### 11.8 Exigences CLI

Le CLI doit :

- retourner des codes de sortie coherents ;
- proposer une sortie lisible humaine ;
- proposer une sortie JSON avec `--json` ;
- ne pas contenir de logique metier ;
- appeler les cas d'usage applicatifs ;
- etre documente ;
- fonctionner dans Docker Compose.

## 12. API FastAPI

### 12.1 Objectif

L'API expose les memes cas d'usage que le CLI pour l'interface React et les integrations futures.

### 12.2 Endpoints minimaux

Imports :

```text
POST   /files/inspect
POST   /files/validate
POST   /imports
GET    /imports
GET    /imports/{import_id}
GET    /imports/{import_id}/errors
POST   /imports/{import_id}/rollback
```

Referentiels :

```text
GET    /agents
GET    /agents/{agent_id}
POST   /agents/{agent_id}/aliases
GET    /sites
GET    /sites/{site_id}
POST   /assignments
```

Statistiques :

```text
GET    /statistics
POST   /statistics/compute
POST   /statistics/rebuild
GET    /statistics/catalog
```

Rapports :

```text
POST   /reports
GET    /reports
GET    /reports/{report_id}
PATCH  /reports/{report_id}/editorial-content
POST   /reports/{report_id}/compile
GET    /reports/{report_id}/preview
GET    /reports/{report_id}/source
GET    /reports/{report_id}/exports/pdf
GET    /reports/{report_id}/exports/quarkdown
GET    /report-templates
POST   /report-templates/{template_id}/validate
```

Jobs :

```text
GET    /jobs
GET    /jobs/{job_id}
POST   /jobs/{job_id}/retry
POST   /jobs/{job_id}/cancel
```

### 12.3 Exigences API

L'API doit :

- documenter OpenAPI automatiquement ;
- valider toutes les entrees avec Pydantic ;
- paginer les listes ;
- permettre tri et filtrage ;
- retourner des erreurs fonctionnelles standardisees ;
- inclure un identifiant de correlation ;
- journaliser les erreurs ;
- gerer les uploads volumineux avec limite ;
- ne jamais exposer les donnees personnelles brutes ;
- fournir des tests contractuels ;
- respecter la parite fonctionnelle avec le CLI.

## 13. Interface React

### 13.1 Objectif

Permettre a un utilisateur fonctionnel de realiser les actions metier sans terminal.

### 13.2 Stack front-end

- React ;
- TypeScript strict ;
- Vite ;
- TanStack Query ou equivalent pour les requetes ;
- React Router ;
- ECharts ou Recharts ;
- tests Vitest ;
- tests Playwright.

Objectifs de test front-end :

- couverture Vitest minimale de 80 % sur lignes et branches pour `frontend/src` a partir de `0.8.0` ;
- couverture de 90 % sur les composants critiques : imports, filtres statistiques, edition de rapport, erreurs API ;
- au moins un parcours Playwright par workflow metier majeur : import, consultation tableau de bord, filtrage site/agent/periode, generation rapport, edition contenu editorial, previsualisation HTML, telechargement PDF ;
- tests d'accessibilite automatises sur les pages principales lorsque l'outillage choisi le permet ;
- aucun composant critique ne doit etre livre uniquement avec un test snapshot.

### 13.3 Pages minimales

#### Tableau de bord

- filtre site ;
- filtre agent ;
- filtre periode ;
- indicateurs principaux ;
- tendances ;
- graphiques ;
- charge horaire ;
- comparaison avec periode precedente ;
- alertes qualite donnees.

#### Centre d'import

- glisser-deposer ;
- detection automatique ;
- preview ;
- erreurs et avertissements ;
- validation ;
- historique ;
- rollback ;
- lignes rejetees.

#### Agents et sites

- liste agents ;
- fiches agents ;
- alias ;
- agents inconnus ;
- rapprochement manuel ;
- liste sites ;
- rattachements dates.

#### Statistiques

- vue journaliere ;
- vue hebdomadaire ;
- vue mensuelle ;
- vue trimestrielle ;
- vue annuelle ;
- periode personnalisee ;
- comparaison ;
- export tabulaire.

#### Rapports

- choix du perimetre ;
- choix de la periode ;
- choix du modele ;
- generation ;
- edition des textes ;
- previsualisation HTML ;
- compilation PDF ;
- historique des revisions ;
- telechargement PDF ;
- telechargement source Quarkdown.

#### Traitements

- jobs en attente ;
- jobs en cours ;
- jobs termines ;
- jobs echoues ;
- logs synthetiques ;
- relance.

### 13.4 Exigences UX

L'interface doit etre sobre, dense et orientee pilotage operationnel.

Elle doit :

- eviter les pages marketing ;
- afficher directement l'outil ;
- permettre une lecture rapide des indicateurs ;
- utiliser des tableaux et filtres efficaces ;
- fournir des etats de chargement ;
- fournir des messages d'erreur compréhensibles ;
- etre utilisable sur ordinateur et tablette ;
- respecter les principes d'accessibilite ;
- eviter toute presentation assimilable a un classement individuel brutal des agents.

## 14. Docker et exploitation

### 14.1 Services Docker

```yaml
services:
  postgres:
    image: postgres:17

  backend:
    build:
      context: ./backend
    command: uvicorn atpro.interfaces.api.main:app --host 0.0.0.0 --port 8000

  worker:
    build:
      context: ./backend
    command: atpro-worker

  frontend:
    build:
      context: ./frontend

  nginx:
    image: nginx
```

Un service dedie `report-worker` peut etre cree si l'isolation Quarkdown le justifie.

### 14.2 Volumes

Volumes requis :

- donnees PostgreSQL ;
- fichiers CSV originaux ;
- fichiers d'import normalises ;
- projets Quarkdown ;
- rapports HTML/PDF ;
- sauvegardes ;
- logs applicatifs si non externalises.

### 14.3 Environnements

Prevoir :

- `compose.yml` commun ;
- `compose.dev.yml` pour developpement ;
- `compose.prod.yml` pour production ;
- `.env.example` documente ;
- healthchecks ;
- reseau interne ;
- secrets hors depot.

### 14.4 Jobs asynchrones

Pour rester simple, les jobs peuvent etre stockes dans PostgreSQL et consommes via `FOR UPDATE SKIP LOCKED`.

Types de jobs :

- import CSV ;
- recalcul statistiques ;
- generation projet Quarkdown ;
- compilation HTML ;
- compilation PDF ;
- export archive ;
- purge ;
- sauvegarde.

### 14.5 Exigences non fonctionnelles chiffrees

Les valeurs suivantes sont des cibles initiales pour `1.0.0`. Elles doivent etre confirmees ou ajustees apres mesure sur les fichiers reels.

| Domaine | Exigence cible |
|---|---|
| Taille fichier CSV | 100 Mo par fichier en import manuel |
| Nombre de fichiers par lot | 20 fichiers |
| Volume import hebdomadaire | 500 000 lignes CSV cumulees |
| Import | 100 000 lignes en moins de 5 minutes sur poste standard |
| Reimport identique | detection et rejet en moins de 30 secondes pour 100 Mo |
| Calcul journalier | moins de 2 minutes pour 1 an de donnees d'un site |
| Calcul periodique complet | moins de 15 minutes pour 1 an multi-sites |
| API consultation tableau de bord | P95 inferieur a 800 ms hors generation asynchrone |
| API listes paginees | P95 inferieur a 500 ms pour 50 lignes |
| Generation rapport HTML | moins de 60 secondes |
| Generation rapport PDF | moins de 120 secondes |
| Taille rapport PDF | cible inferieure a 25 Mo |
| Disponibilite locale | redemarrage complet Docker en moins de 5 minutes |
| Sauvegarde | sauvegarde PostgreSQL quotidienne possible |
| Restauration | procedure testee en moins de 30 minutes sur environnement de recette |

Contraintes techniques :

- les operations longues doivent etre asynchrones ;
- l'API ne doit pas bloquer une requete HTTP pendant un import complet ;
- les listes doivent etre paginees ;
- les endpoints de statistiques doivent utiliser les agregats materialises ;
- les seuils doivent etre couverts par au moins un test de performance ou un script de benchmark avant `1.0.0`.

## 15. Securite et donnees personnelles

### 15.1 Donnees sensibles

Les sources peuvent contenir :

- numeros de telephone ;
- emails ;
- identifiants de contact ;
- noms et prenoms d'agents ;
- historiques d'activite.

### 15.2 Regles de protection

Obligatoire :

- ne pas stocker les emails en clair dans les tables analytiques ;
- hacher les numeros de telephone avec sel applicatif ;
- masquer les payloads de lignes rejetees ;
- limiter l'acces aux fichiers bruts ;
- tracer les imports et exports ;
- separer roles lecteur, pilote et administrateur ;
- documenter la duree de conservation ;
- proteger les exports de rapports ;
- ne jamais logger de donnees sensibles brutes.

### 15.3 Roles

Roles minimaux :

- `reader` : consultation ;
- `pilot` : imports, calculs, rapports ;
- `functional_admin` : referentiels, alias, rattachements ;
- `technical_admin` : maintenance, migrations, jobs techniques.

L'authentification complete peut arriver en `0.9.0`, mais l'architecture doit l'anticiper. Des le debut, les cas d'usage doivent accepter un contexte utilisateur minimal, meme si ce contexte est un stub en developpement.

Matrice minimale role/action :

| Action | reader | pilot | functional_admin | technical_admin |
|---|---:|---:|---:|---:|
| Consulter tableaux de bord | Oui | Oui | Oui | Oui |
| Exporter donnees statistiques | Oui | Oui | Oui | Oui |
| Inspecter un fichier | Non | Oui | Oui | Oui |
| Lancer un import | Non | Oui | Oui | Oui |
| Rollback import | Non | Oui | Oui | Oui |
| Lancer calcul statistiques | Non | Oui | Oui | Oui |
| Generer rapport | Non | Oui | Oui | Oui |
| Publier rapport | Non | Oui | Oui | Non par defaut |
| Gerer alias agents | Non | Non | Oui | Oui |
| Gerer sites et rattachements | Non | Non | Oui | Oui |
| Relancer jobs techniques | Non | Non | Non | Oui |
| Migrer la base | Non | Non | Non | Oui |
| Voir logs techniques detailles | Non | Non | Non | Oui |

Avant `0.9.0`, le mode de developpement peut utiliser :

- un utilisateur local configure par variable d'environnement ;
- un role par defaut `technical_admin` uniquement en environnement `dev` ;
- des tests qui verifient deja les decisions d'autorisation ;
- aucune exposition publique sans controle d'acces explicite.

### 15.3.1 Conformite RGPD et gouvernance

Le projet manipule des donnees personnelles. Les protections techniques ne suffisent pas : le volet conformite doit etre traite avant production.

Elements obligatoires avant `1.0.0` :

- identifier le responsable de traitement ;
- identifier le DPO ou referent protection des donnees ;
- documenter la base legale du traitement ;
- inscrire le traitement au registre interne ;
- definir les finalites exactes ;
- definir les categories de donnees ;
- definir les durees de conservation ;
- definir les destinataires ;
- definir les droits applicables aux personnes concernees ;
- documenter les mesures de securite ;
- realiser une analyse d'impact si le DPO la juge necessaire ;
- valider la politique de pseudonymisation des numeros et contacts ;
- valider les conditions d'utilisation des rapports exportes.

Le depot de code doit contenir la documentation technique de protection des donnees, mais ne doit pas contenir de registre RGPD nominatif ou information administrative sensible.

### 15.4 Securite des imports

L'application doit :

- limiter la taille des fichiers ;
- verifier les extensions ;
- verifier le type reel ;
- isoler le stockage des fichiers ;
- refuser les chemins relatifs malveillants ;
- empecher l'ecrasement de fichiers ;
- journaliser les erreurs de parsing ;
- ne pas executer de contenu issu des CSV.

### 15.5 Securite Quarkdown

L'application doit :

- compiler sans reseau ;
- refuser la lecture globale ;
- echapper les textes utilisateurs ;
- limiter les fonctions disponibles ;
- appliquer un timeout ;
- conserver les logs ;
- detecter les erreurs de compilation ;
- ne pas exposer le filesystem dans les messages utilisateur.

## 16. Qualite, tests et couverture

### 16.1 Standards Python

Obligatoire :

- Ruff ;
- Black ou formatage equivalent ;
- mypy strict sur le domaine et l'application ;
- Pytest ;
- coverage ;
- Bandit ;
- SQLAlchemy 2.x type-friendly ;
- docstrings pour les cas d'usage complexes.

Objectif de couverture :

- 95 % sur domaine, parsing, statistiques et reporting ;
- 85 % minimum sur interfaces et infrastructure ;
- tests d'integration obligatoires sur PostgreSQL.

Lorsque le workflow du depot impose un seuil global plus strict, notamment `--cov-fail-under=95`, ce seuil global est la regle de validation. Le seuil de 85 % pour interfaces et infrastructure n'autorise pas a descendre sous la couverture globale exigee ; il sert seulement a identifier les zones moins critiques dans l'analyse de couverture. Toute modulation du seuil global doit etre justifiee par ADR.

### 16.2 Tests parseurs

Cas requis :

- detection de chaque type de fichier ;
- detection des schemas tickets ;
- detection activites large ;
- detection activites long ;
- consolidation appels multi-lignes ;
- dates multiples ;
- durees multiples ;
- pourcentages avec virgule ;
- encodage Windows-1252 ;
- donnees mal encodees ;
- agents non reconnus ;
- lignes invalides ;
- fichier deja importe.

### 16.3 Tests persistance

Cas requis :

- import initial ;
- reimport identique ;
- import chevauchant ;
- conflit avec contenu identique ;
- conflit avec contenu different ;
- rollback ;
- contraintes uniques ;
- transaction annulee sur erreur ;
- invalidation statistiques.

### 16.4 Tests statistiques

Cas requis :

- calcul journalier agent ;
- calcul journalier site ;
- calcul horaire ;
- segment traversant deux heures ;
- semaine ISO ;
- mois ;
- trimestre ;
- annee ;
- periode personnalisee ;
- denominateur nul ;
- mediane ;
- P90 ;
- recalcul apres invalidation.

### 16.5 Tests rapports

Cas requis :

- generation projet Quarkdown ;
- presence des fichiers attendus ;
- compilation HTML ;
- compilation PDF ;
- edition contenu editorial ;
- chiffres non modifiables ;
- snapshot donnees fige ;
- rapport publie inchange apres recalcul ;
- logs de compilation ;
- erreur Quarkdown lisible ;
- tentative d'injection de fonction dans contenu utilisateur ;
- export source.

### 16.6 Tests front-end

Cas requis :

- rendu des pages principales ;
- upload fichier ;
- affichage preview import ;
- affichage erreurs ;
- consultation statistiques ;
- filtre site/agent/periode ;
- generation rapport ;
- edition texte ;
- previsualisation HTML ;
- telechargement PDF ;
- etats loading/error/empty ;
- tests Playwright des parcours principaux.

## 17. CI/CD

### 17.1 Pipeline minimal

A chaque pull request :

1. lint Python ;
2. format check Python ;
3. typage Python ;
4. tests unitaires Python ;
5. tests integration PostgreSQL ;
6. scan securite Python ;
7. lint TypeScript ;
8. tests front-end ;
9. build React ;
10. build images Docker ;
11. tests smoke Docker Compose ;
12. generation d'un rapport Quarkdown de test ;
13. conservation des artefacts de test.

Si le depot commence comme une librairie Python mono-package, le pipeline peut etre progressif, mais chaque nouvelle zone ajoutee au depot doit ajouter ses controles dans la CI dans la meme pull request :

- ajout de `frontend/` implique TypeScript, lint, tests et build ;
- ajout de `docker/` ou `compose.yml` implique build image et smoke test ;
- ajout de Quarkdown implique compilation HTML/PDF de test ;
- ajout d'endpoints API implique tests contractuels ou OpenAPI.

Une fonctionnalite ne doit pas etre consideree livree si sa zone de code n'est pas couverte par la commande de validation racine.

### 17.2 Pipeline release

A chaque tag `vX.Y.Z` :

- build images versionnees ;
- scan images ;
- generation changelog ;
- publication artefacts ;
- sauvegarde schema Alembic ;
- generation documentation utilisateur ;
- generation documentation API ;
- smoke test complet.

### 17.3 Regles de merge

Une pull request ne peut etre fusionnee que si :

- pipeline vert ;
- migrations presentes si schema modifie ;
- tests ajoutes ou justification ;
- documentation mise a jour ;
- aucun secret ;
- aucune modification des fichiers sources de reference ;
- revue humaine ou IA realisee.

## 18. Documentation attendue

Documents minimaux :

- `README.md` ;
- `docs/architecture.md` ;
- `docs/repository-workflow.md` ;
- `docs/domain-model.md` ;
- `docs/imports.md` ;
- `docs/statistics-catalog.md` ;
- `docs/reports-quarkdown.md` ;
- `docs/cli.md` ;
- `docs/api.md` ;
- `docs/docker.md` ;
- `docs/security.md` ;
- `docs/operations.md` ;
- `docs/architecture/adr/ADR-0001-*.md`.

La documentation doit expliquer les limites fonctionnelles, notamment la difference entre charge telephonique horaire et occupation horaire complete.

## 19. Roadmap versionnee

### 19.1 Version 0.1.0 - Modele canonique et parseurs CSV

Objectif : transformer les CSV en modeles metier sans base de donnees.

Contenu :

- ADR sur la structure effective du depot et le perimetre de `AGENTS.md` ;
- nettoyage du squelette template si present ;
- remplacement de `example_package` par `atpro` ;
- initialisation du backlog ou de `queue.yaml` si le workflow du depot l'utilise ;
- fixtures ou echantillons anonymises lorsque les CSV reels ne sont pas versionnes ;
- modeles metier ;
- value objects ;
- detection encodage ;
- detection separateur ;
- detection type fichier ;
- detection version schema ;
- parseurs appels entrants ;
- parseurs appels sortants ;
- parseurs tickets ;
- parseurs activites large ;
- parseurs activites long ;
- normalisation agents/sites/dates/durees ;
- consolidation appels multi-lignes ;
- rapport de parsing ;
- CLI `file inspect`, `file validate`, `file preview` ;
- tests sur fichiers de reference.

Critere de sortie : tous les formats connus sont detectes et transformes en objets metier, avec erreurs et avertissements exploitables.

### 19.2 Version 0.2.0 - PostgreSQL et imports idempotents

Objectif : enregistrer les donnees sans doublons.

Contenu :

- ADR definitive sur `src/atpro` racine ou `backend/src/atpro` ;
- Docker PostgreSQL ;
- SQLAlchemy ;
- Alembic ;
- repositories ;
- unit of work ;
- tables metier ;
- tables imports ;
- SHA-256 fichiers ;
- empreintes lignes ;
- contraintes uniques ;
- import transactionnel ;
- gestion donnees nouvelles, identiques, modifiees ;
- lignes rejetees ;
- rollback ;
- agents, sites, alias, rattachements ;
- CLI import et referentiels.

Critere de sortie : le reimport d'un fichier identique ne cree aucune donnee supplementaire.

### 19.3 Version 0.3.0 - Statistiques journalieres et horaires

Objectif : produire les premieres statistiques operationnelles.

Contenu :

- statistiques appels journalieres ;
- statistiques tickets journalieres ;
- statistiques activites agents journalieres ;
- charge telephonique horaire ;
- tables statistiques ;
- catalogue indicateurs ;
- versionnement formules ;
- invalidation ;
- recalcul cible ;
- CLI stats minimal.

Critere de sortie : une journee de reference est calculable et verifiable.

### 19.4 Version 0.4.0 - Statistiques periodiques et comparaisons

Objectif : couvrir toutes les periodes de pilotage.

Contenu :

- semaines ISO ;
- mois ;
- trimestres ;
- annees ;
- periodes personnalisees ;
- periode precedente ;
- meme periode annee precedente ;
- moyenne glissante ;
- cumuls ;
- recalcul cascade ;
- non-regression sur periode de reference.

Critere de sortie : les statistiques necessaires au rapport hebdomadaire de reference sont disponibles.

### 19.5 Version 0.5.0 - Rapports Quarkdown

Objectif : generer des rapports sources Quarkdown, HTML et PDF.

Contenu :

- spike technique Quarkdown valide par ADR ;
- moteur de rapports ;
- generation projet `.qd` ;
- structure multi-fichiers ;
- theme AT Pro/DGFIP ;
- rapports site ;
- rapports agent ;
- tableaux ;
- graphiques ;
- textes deterministes ;
- edition editoriale ;
- chiffres non modifiables ;
- snapshot donnees ;
- compilation HTML ;
- compilation PDF ;
- logs compilation ;
- export source Quarkdown ;
- export PDF ;
- tests securite Quarkdown.

Critere de sortie : un rapport site hebdomadaire peut etre genere, previsualise et exporte en PDF depuis un projet Quarkdown reproductible.

### 19.6 Version 0.6.0 - CLI complet et MVP technique

Objectif : permettre l'exploitation complete sans interface Web.

Contenu :

- finalisation CLI ;
- sorties humaines et JSON ;
- codes retour ;
- scripts sauvegarde/restauration ;
- diagnostics ;
- jobs ;
- documentation exploitation.

Critere de sortie : le cycle complet importer, calculer, consulter et generer un rapport fonctionne au CLI.

### 19.7 Version 0.7.0 - API FastAPI

Objectif : exposer les cas d'usage au front-end.

Contenu :

- endpoints imports ;
- endpoints referentiels ;
- endpoints statistiques ;
- endpoints rapports ;
- endpoints jobs ;
- upload multi-fichiers ;
- OpenAPI ;
- pagination ;
- filtrage ;
- erreurs standardisees ;
- tests contractuels ;
- parite CLI/API.

Critere de sortie : chaque action metier importante du CLI possede un equivalent API.

### 19.8 Version 0.8.0 - Interface React

Objectif : livrer une beta fonctionnelle utilisable par les pilotes.

Contenu :

- centre d'import ;
- referentiels agents/sites ;
- tableaux de bord ;
- statistiques par periode ;
- rapports ;
- previsualisation HTML ;
- telechargement PDF et Quarkdown ;
- suivi jobs ;
- tests front-end ;
- parcours Playwright.

Critere de sortie : toutes les actions metier destinees aux utilisateurs fonctionnels sont disponibles dans le navigateur.

### 19.9 Version 0.9.0 - Securite, audit et recette

Objectif : preparer la production.

Contenu :

- authentification ;
- roles ;
- restrictions par site ;
- audit ;
- retention ;
- purge ;
- sauvegarde ;
- restauration testee ;
- durcissement Docker ;
- secrets ;
- tests performance ;
- recette metier ;
- correction des ecarts ;
- gel des regles de calcul.

Critere de sortie : aucun blocage critique ou majeur en recette.

### 19.10 Version 1.0.0 - Production

Objectif : livrer une version stable.

Contenu :

- reprise historique ;
- validation definitive formules ;
- validation rapports ;
- documentation utilisateur ;
- documentation administrateur ;
- procedures exploitation ;
- supervision ;
- release taguee ;
- images Docker versionnees ;
- changelog ;
- donnees demo anonymisees ;
- migrations depuis versions precedentes.

Critere de sortie : l'application peut etre deployee, administree et utilisee en fonctionnement courant.

### 19.11 Versions post-1.0

| Version | Theme | Contenu principal |
|---|---|---|
| `1.1.0` | Qualite donnees avancee | completude, schemas changeants, fichiers manquants, anomalies |
| `1.2.0` | Tableaux de bord personnalisables | vues sauvegardees, filtres favoris, exports |
| `1.3.0` | Automatisation | imports planifies, rapports programmes, notifications |
| `1.4.0` | Comparaison sites | inter-sites, normalisation par effectif ou temps connecte |
| `1.5.0` | Pilotage agent contextualise | historique agent, comparaison a soi-meme, distribution collective |
| `1.6.0` | Connecteurs | SFTP, stockage documentaire, API sources |
| `1.7.0` | Alertes | seuils, objectifs, acquittement, suivi |
| `1.8.0` | Rapports avances | editeur de modeles Quarkdown, workflow validation |
| `1.9.0` | Performance | partitionnement, cache, gros volumes |
| `2.0.0` | Plateforme elargie | multi-organisations, sources multiples, previsions |

## 20. Critères d'acceptation globaux

L'application est acceptable lorsque :

1. les CSV de reference sont detectes automatiquement ;
2. les variations de schema sont gerees ;
3. les appels multi-lignes sont consolides correctement ;
4. les agents et sites sont normalises ;
5. les cas ambigus sont presentes a l'utilisateur ;
6. PostgreSQL empeche les doublons ;
7. un reimport identique est idempotent ;
8. les statistiques site et agent sont disponibles par periode ;
9. la charge horaire telephonique est calculee sans inventer l'occupation complete ;
10. les rapports Quarkdown sont generes, compilables et exportables ;
11. les chiffres des rapports sont traces et non modifiables manuellement ;
12. le CLI permet le cycle complet ;
13. l'API offre la parite fonctionnelle ;
14. React permet les actions metier ;
15. les tests critiques sont automatises ;
16. les donnees personnelles sont protegees ;
17. Docker permet de lancer l'ensemble ;
18. la documentation est suffisante pour installer, utiliser et maintenir ;
19. la CI/CD bloque les regressions ;
20. les limites metier sont affichees et documentees.
21. le workflow du depot est reconcilie avec l'architecture cible par ADR ;
22. les exigences non fonctionnelles sont mesurees ou explicitement ajustees ;
23. le traitement RGPD est documente avant production ;
24. le spike Quarkdown a valide la chaine HTML/PDF ou documente une alternative.

## 21. Risques

| Risque | Impact | Probabilite | Mitigation |
|---|---:|---:|---|
| Variation non anticipee des CSV | Eleve | Elevee | Detecteur de schema, tests, rapport d'anomalies |
| Mauvais rapprochement agent | Eleve | Moyenne | Alias, confiance, validation manuelle |
| Doublons mal controles | Eleve | Moyenne | Contraintes PostgreSQL, fingerprints, tests idempotence |
| Statistiques contestees | Eleve | Moyenne | Catalogue formules, versionnement, jeux de reference |
| Occupation horaire surestimee | Eleve | Moyenne | Ne pas reconstituer les etats horaires absents |
| Rapport PDF non fidele | Moyen | Moyenne | Tests visuels, theme Quarkdown, reference Word |
| Injection dans Quarkdown | Eleve | Moyenne | Echappement, sandbox, permissions, tests securite |
| Quarkdown moins mature que les outils classiques | Moyen | Moyenne | Spike obligatoire, ADR, solution de secours documentee |
| Performance imports volumineux | Moyen | Moyenne | Polars, batch inserts, indexes |
| Donnees personnelles exposees | Eleve | Moyenne | Hash, masquage, roles, audit |
| Projet trop large pour MVP | Eleve | Elevee | Roadmap stricte, criteres par version |
| Contradiction entre workflow librairie et application | Eleve | Elevee au demarrage | ADR depot, regles par zone, CI progressive |

## 22. Questions ouvertes

Les points suivants doivent etre valides avant ou pendant les premieres versions :

1. Liste officielle des sites et codes de sites.
2. Regle de rattachement d'un agent a un site en cas d'absence d'affectation connue.
3. Politique exacte de mise a jour d'un ticket deja importe mais modifie.
4. Definition officielle d'un appel presente, repondu, abandonne et transfere.
5. Definition officielle d'un contre-appel.
6. Definition exacte des tickets recus, qualifies, resolus et clotures.
7. Statut des tickets annules ou hors perimetre.
8. Methode de calcul du backlog si les historiques incomplets persistent.
9. Liste des indicateurs obligatoires pour le premier rapport.
10. Charte graphique precise a appliquer dans Quarkdown.
11. Logo ou assets officiels autorises.
12. Format final de diffusion en plus du PDF si necessaire.
13. Duree de conservation des fichiers bruts.
14. Niveau de granularite des droits utilisateurs.
15. Source future eventuelle pour les etats horaires agents.
16. Structure finale du depot : `src/atpro` racine ou `backend/src/atpro`.
17. Perimetre exact de `AGENTS.md` et fichiers de workflow complementaires pour front-end et Docker.
18. Emplacement et statut des CSV de reference : versionnes anonymises, volume externe ou stockage documentaire.
19. Politique de mise a jour des activites agents : globale, par type d'import, par site ou manuelle.
20. Fuseau horaire officiel des sources et regles de gestion des changements d'heure.
21. Volumetrie cible reelle : taille des CSV, nombre de lignes, historique a reprendre.
22. Objectifs de latence API et temps maximal acceptable pour imports/calculs.
23. Mode d'authentification cible et statut du stub d'autorisation avant `0.9.0`.
24. Validation RGPD : responsable de traitement, DPO, base legale, conservation.
25. Resultat du spike Quarkdown et solution de secours si une hypothese est invalidee.

## 23. Instructions pour une IA de developpement

L'IA chargee du developpement doit :

1. commencer par lire ce cahier des charges ;
2. inspecter les sources CSV sans les modifier ;
3. creer une architecture minimale conforme ;
4. livrer par versions successives ;
5. ecrire les tests en meme temps que les modules ;
6. documenter toute decision non evidente ;
7. ne pas avancer vers React avant d'avoir les cas d'usage back-end utilisables ;
8. ne pas dupliquer la logique entre CLI, API et Web ;
9. verifier l'idempotence des imports ;
10. produire un journal clair de ce qui est termine, partiel ou bloque.

Chaque version doit inclure :

- code ;
- migrations si necessaire ;
- tests ;
- documentation ;
- exemples de commandes ;
- notes de version ;
- limites connues.

## 24. Instructions pour une IA de revue

L'IA de revue doit verifier :

- conformite au present cahier des charges ;
- separation domaine/application/infrastructure ;
- robustesse des parseurs ;
- idempotence reelle ;
- contraintes uniques en base ;
- exactitude des statistiques ;
- absence de reconstitution abusive ;
- securite des donnees personnelles ;
- securite de compilation Quarkdown ;
- qualite des tests ;
- couverture des cas sources ;
- clarte de la documentation ;
- coherence de l'UX ;
- maintenabilite du code.

La revue doit lister :

1. anomalies bloquantes ;
2. risques majeurs ;
3. corrections recommandees ;
4. ameliorations optionnelles ;
5. questions a arbitrer.

## 25. Definition of Done

Une fonctionnalite est terminee si :

- elle respecte les exigences du cahier des charges ;
- elle est testee ;
- elle est documentee ;
- elle fonctionne via le canal prevu ;
- elle gere les erreurs ;
- elle journalise les evenements importants ;
- elle ne degrade pas les tests existants ;
- elle ne modifie pas les sources de reference ;
- elle n'expose pas de donnees sensibles ;
- elle a ete verifiee dans Docker si elle depend de l'infrastructure.

Une version est terminee si :

- toutes les fonctionnalites prevues sont terminees ;
- les migrations sont reproductibles ;
- la CI est verte ;
- les criteres d'acceptation de version sont satisfaits ;
- les limites connues sont documentees ;
- les notes de version sont redigees.

## 26. Annexes techniques

### 26.1 Exemple de configuration `.env`

```dotenv
ATPRO_ENV=dev
ATPRO_DATABASE_URL=postgresql+psycopg://atpro:atpro@postgres:5432/atpro
ATPRO_STORAGE_ROOT=/var/lib/atpro
ATPRO_REPORTS_ROOT=/var/lib/atpro/reports
ATPRO_HASH_SECRET=change-me
ATPRO_LOG_LEVEL=INFO
ATPRO_QUARKDOWN_TIMEOUT_SECONDS=60
```

### 26.2 Exemple de sortie JSON CLI

```json
{
  "status": "completed_with_warnings",
  "import_id": "uuid",
  "detected_type": "incoming_calls",
  "schema_version": "calls-long-v1",
  "accepted_rows": 1240,
  "rejected_rows": 3,
  "warnings": [
    {
      "code": "UNKNOWN_AGENT",
      "message": "Agent non reconnu",
      "count": 2
    }
  ]
}
```

### 26.3 Exemple de metadonnees rapport

```json
{
  "report_id": "uuid",
  "title": "Rapport hebdomadaire AT Pro",
  "scope_type": "site",
  "scope_name": "Montpellier",
  "period_type": "week",
  "period_start": "2026-06-15",
  "period_end": "2026-06-21",
  "generated_at": "2026-07-25T10:00:00+02:00",
  "calculation_version": "statistics-v1",
  "template_version": "site-weekly-v1"
}
```

### 26.4 Exemple de commandes Quarkdown

```bash
quarkdown c main.qd --out output --strict --timeout 60
quarkdown c main.qd --pdf --out output --strict --timeout 60
```

### 26.5 Structure cible du depot

```text
atpro-pilotage/
├── backend/
├── frontend/
├── docker/
├── docs/
├── samples/
├── compose.yml
├── compose.dev.yml
├── compose.prod.yml
├── .env.example
├── README.md
└── CHANGELOG.md
```

Si le depot existant impose provisoirement un package Python a la racine, la structure transitoire acceptee est :

```text
atpro-pilotage/
├── src/
│   └── atpro/
├── tests/
├── docs/
├── samples/
├── pyproject.toml
├── Makefile
├── queue.yaml
├── AGENTS.md
└── README.md
```

Cette structure transitoire doit rester compatible avec la trajectoire applicative. Elle ne doit pas empecher l'ajout ulterieur de `frontend/`, `docker/`, `compose.yml` et des tests d'orchestration.

## 27. Conclusion

Le coeur du projet est le modele metier canonique. Les CSV, PostgreSQL, le CLI, FastAPI, React et Quarkdown sont des adaptateurs autour de ce coeur.

La reussite du projet depend principalement de quatre points :

- robustesse du parsing ;
- idempotence de la persistance ;
- explicabilite des statistiques ;
- reproductibilite des rapports.

La roadmap doit rester progressive : `0.6.0` constitue le MVP technique, `0.8.0` la beta metier, `0.9.0` la release candidate et `1.0.0` la premiere version de production.
