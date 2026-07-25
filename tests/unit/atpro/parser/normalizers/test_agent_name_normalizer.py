"""Tests de AgentNameNormalizer."""

from __future__ import annotations

from atpro.parser.normalizers.agent_name_normalizer import AgentNameNormalizer


class TestAgentNameNormalizer:
    def test_FEAT_010_1_prenom_nom(self) -> None:
        result = AgentNameNormalizer().normalize("Caroline CORBIER")
        assert result.raw_value == "Caroline CORBIER"
        assert result.normalized_value == "caroline corbier"
        assert result.first_name_hint == "Caroline"
        assert result.last_name_hint == "CORBIER"
        assert result.is_ambiguous is False

    def test_FEAT_010_1_nom_prenom(self) -> None:
        result = AgentNameNormalizer().normalize("CORBIER Caroline")
        assert result.last_name_hint == "CORBIER"
        assert result.first_name_hint == "Caroline"

    def test_FEAT_010_1_hyphenated_first_name(self) -> None:
        result = AgentNameNormalizer().normalize("Jean-Pierre DUPONT")
        assert result.first_name_hint == "Jean-Pierre"
        assert result.last_name_hint == "DUPONT"

    def test_FEAT_010_1_compound_first_name(self) -> None:
        result = AgentNameNormalizer().normalize("Marie Claire MARTIN")
        assert result.first_name_hint == "Marie Claire"
        assert result.last_name_hint == "MARTIN"

    def test_FEAT_010_1_accents(self) -> None:
        result = AgentNameNormalizer().normalize("Éléonore DURAND")
        assert result.normalized_value == "eleonore durand"

    def test_FEAT_010_1_degraded_encoding_still_normalized(self) -> None:
        # Accents partiellement corrompus : on conserve le brut, on normalise le reste.
        result = AgentNameNormalizer().normalize("ElÃ©onore DURAND")
        assert result.raw_value == "ElÃ©onore DURAND"
        assert "durand" in result.normalized_value

    def test_FEAT_010_1_empty_value(self) -> None:
        result = AgentNameNormalizer().normalize("   ")
        assert result.normalized_value == ""
        assert result.is_ambiguous is True
        assert "empty_value" in result.ambiguity_reasons

    def test_FEAT_010_1_ambiguous_same_case(self) -> None:
        result = AgentNameNormalizer().normalize("alice dupont")
        assert result.is_ambiguous is True
        assert "case_pattern_unclear" in result.ambiguity_reasons

    def test_FEAT_010_1_single_token(self) -> None:
        result = AgentNameNormalizer().normalize("DUPONT")
        assert result.last_name_hint == "DUPONT"
        assert result.is_ambiguous is True
        assert "single_token" in result.ambiguity_reasons
