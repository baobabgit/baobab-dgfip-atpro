"""Tests de KnownActivityMeasure."""

from __future__ import annotations

from atpro.parser.activities.known_activity_measure import KnownActivityMeasure


class TestKnownActivityMeasure:
    def test_FEAT_009_1_resolve_answered_calls(self) -> None:
        assert KnownActivityMeasure.resolve("appels_decroches") == (
            "answered_calls",
            "count",
        )

    def test_FEAT_009_1_outgoing_aliases(self) -> None:
        assert KnownActivityMeasure.resolve("nombre_d_appels_sortants") == (
            "outgoing_calls",
            "count",
        )
        assert KnownActivityMeasure.resolve("appels_sortants") == (
            "outgoing_calls",
            "count",
        )

    def test_FEAT_009_1_rona_aliases(self) -> None:
        assert KnownActivityMeasure.resolve("temps_total_dans_l_etat_rona") == (
            "rona_time_seconds",
            "duration",
        )
        assert KnownActivityMeasure.resolve("temps_total_dans_letat_rona") == (
            "rona_time_seconds",
            "duration",
        )

    def test_FEAT_009_1_unknown_returns_none(self) -> None:
        assert KnownActivityMeasure.resolve("mesure_inconnue_xyz") is None

    def test_FEAT_008_1_meta_columns(self) -> None:
        assert KnownActivityMeasure.is_meta_column("periode")
        assert KnownActivityMeasure.is_meta_column("agent_groupe_agent")
        assert not KnownActivityMeasure.is_meta_column("appels_decroches")
