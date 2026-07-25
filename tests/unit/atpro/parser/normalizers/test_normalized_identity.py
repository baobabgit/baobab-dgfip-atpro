"""Tests de NormalizedIdentity."""

from __future__ import annotations

from atpro.parser.normalizers.normalized_identity import NormalizedIdentity


class TestNormalizedIdentity:
    def test_FEAT_010_1_to_dict(self) -> None:
        identity = NormalizedIdentity(
            raw_value="Caroline CORBIER",
            normalized_value="caroline corbier",
            first_name_hint="Caroline",
            last_name_hint="CORBIER",
            confidence=0.9,
        )
        data = identity.to_dict()
        assert data["normalized_value"] == "caroline corbier"
        assert data["first_name_hint"] == "Caroline"
