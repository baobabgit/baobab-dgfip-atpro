"""Check AT Pro Pilotage documentation traceability.

Canonical layout (AGENTS / ADR-0001):

- CDC: docs/specifications/000_cahier-des-charges/
- US / FEAT / BL: docs/backlog/{user_stories,features,backlogs}

It must fail loudly when expected files cannot be found. Silent success on an
empty tree is considered a bug.
"""

from __future__ import annotations

import re
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]

US_ID = re.compile(r"\bUS-\d{3}\b")
FEAT_ID = re.compile(r"\bFEAT-\d{3}\.\d+\b")
BL_ID = re.compile(r"\bBL-\d{3}\b")


def first_existing_file(candidates: list[Path]) -> Path | None:
    for candidate in candidates:
        if candidate.exists() and candidate.is_file():
            return candidate
    return None


def collect_ids(directory: Path, pattern: str) -> set[str]:
    return {path.stem for path in directory.glob(pattern)}


def read(path: Path) -> str:
    return path.read_text(encoding="utf-8")


def require(condition: bool, message: str, errors: list[str]) -> None:
    if not condition:
        errors.append(message)


def main() -> int:
    errors: list[str] = []

    cahier = first_existing_file(
        [
            ROOT / "docs/specifications/000_cahier-des-charges/000_specifications.md",
            ROOT / "docs/specifications/000_cahier-des-charges/index.md",
        ]
    )

    us_dir = ROOT / "docs/backlog/user_stories"
    feat_dir = ROOT / "docs/backlog/features"
    bl_dir = ROOT / "docs/backlog/backlogs"

    require(cahier is not None, "Cahier des charges introuvable", errors)
    require(us_dir.is_dir(), "Dossier US introuvable: docs/backlog/user_stories", errors)
    require(feat_dir.is_dir(), "Dossier FEAT introuvable: docs/backlog/features", errors)
    require(bl_dir.is_dir(), "Dossier BL introuvable: docs/backlog/backlogs", errors)

    if errors:
        for error in errors:
            print(f"TRACEABILITY ERROR: {error}", file=sys.stderr)
        return 1

    assert cahier is not None

    us_ids = collect_ids(us_dir, "US-*.md")
    feat_ids = collect_ids(feat_dir, "FEAT-*.md")
    bl_ids = collect_ids(bl_dir, "BL-*.md")

    require(bool(us_ids), f"Aucune US trouvee dans {us_dir}", errors)
    require(bool(feat_ids), f"Aucune FEAT trouvee dans {feat_dir}", errors)
    require(bool(bl_ids), f"Aucun BL trouve dans {bl_dir}", errors)

    adr_0001 = ROOT / "docs/architecture/adr/ADR-0001-structure-depot-v010.md"
    require(adr_0001.exists(), "ADR-0001 manquante dans docs/architecture/adr", errors)

    adr_0002 = ROOT / "docs/architecture/adr/ADR-0002-persistance-postgresql-v020.md"
    require(adr_0002.exists(), "ADR-0002 manquante dans docs/architecture/adr", errors)

    queue = ROOT / "docs/ai_workflow/state/queue.yaml"
    require(queue.exists(), "docs/ai_workflow/state/queue.yaml manquant", errors)

    for version in ("v0.1.0", "v0.2.0"):
        version_required = [
            ROOT / f"docs/ai_workflow/versions/{version}/version.yaml",
            ROOT / f"docs/ai_workflow/versions/{version}/scope.md",
            ROOT / f"docs/ai_workflow/versions/{version}/validation.md",
            ROOT / f"docs/ai_workflow/versions/{version}/integration_matrix.yaml",
            ROOT / f"docs/ai_workflow/versions/{version}/release_report.md",
        ]
        for required in version_required:
            require(
                required.exists(),
                f"Fichier de version manquant: {required}",
                errors,
            )

    persistence = ROOT / "docs/contracts/persistence_contract.md"
    require(persistence.exists(), "Contrat de persistance manquant", errors)

    for path in feat_dir.glob("FEAT-*.md"):
        text = read(path)
        refs = set(US_ID.findall(text))
        require(bool(refs), f"{path.name} ne reference aucune US", errors)
        for ref in refs:
            require(ref in us_ids, f"{path.name} reference une US inexistante: {ref}", errors)

    for path in bl_dir.glob("BL-*.md"):
        text = read(path)
        us_refs = set(US_ID.findall(text))
        feat_refs = set(FEAT_ID.findall(text))
        require(bool(feat_refs), f"{path.name} ne reference aucune FEAT", errors)
        for ref in us_refs:
            require(ref in us_ids, f"{path.name} reference une US inexistante: {ref}", errors)
        for ref in feat_refs:
            require(ref in feat_ids, f"{path.name} reference une FEAT inexistante: {ref}", errors)

    queue_text = read(queue) if queue.exists() else ""
    for ref in set(BL_ID.findall(queue_text)):
        require(ref in bl_ids, f"queue.yaml reference un BL inexistant: {ref}", errors)

    forbidden_patterns = [
        "FEAT-0.1-",
        "BL-0.1-",
        "docs/decisions",
        "docs/specifications/cahier-des-charges",
        "docs/specifications/us",
        "docs/specifications/001_us",
        "docs/specifications/002_feat",
        "docs/specifications/003_bl",
    ]
    active_text_paths = [
        *us_dir.glob("*.md"),
        *feat_dir.glob("*.md"),
        *bl_dir.glob("*.md"),
        ROOT / "docs/backlog/index.rst",
        ROOT / "docs/ai_workflow/state/queue.yaml",
        ROOT / "docs/ai_workflow/state/dependency_graph.yaml",
        cahier,
    ]
    for path in active_text_paths:
        if not path.exists():
            continue
        text = read(path)
        for forbidden in forbidden_patterns:
            require(
                forbidden not in text,
                f"{path} contient une ancienne convention: {forbidden}",
                errors,
            )

    contracts = (
        list((ROOT / "docs/contracts").glob("*.md"))
        if (ROOT / "docs/contracts").exists()
        else []
    )
    require(bool(contracts), "Contrats publics manquants dans docs/contracts", errors)
    for path in contracts:
        text = read(path)
        for forbidden in ["example_package", "Greeter", "Repository"]:
            require(
                forbidden not in text,
                f"{path.name} contient encore une reference template: {forbidden}",
                errors,
            )

    if errors:
        for error in errors:
            print(f"TRACEABILITY ERROR: {error}", file=sys.stderr)
        return 1

    print("Traçabilité OK")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
