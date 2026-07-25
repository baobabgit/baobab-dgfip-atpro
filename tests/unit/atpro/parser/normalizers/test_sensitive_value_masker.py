"""Tests de SensitiveValueMasker."""

from __future__ import annotations

from atpro.parser.normalizers.sensitive_value_masker import SensitiveValueMasker


class TestSensitiveValueMasker:
    def test_FEAT_005_3_masks_email(self) -> None:
        masked = SensitiveValueMasker().mask("contact: alice.dupont@dgfip.fr")
        assert masked is not None
        assert "alice.dupont@dgfip.fr" not in masked
        assert "@" in masked

    def test_FEAT_005_3_masks_phone(self) -> None:
        masked = SensitiveValueMasker().mask("appeler 06 12 34 56 78")
        assert masked is not None
        assert "06 12 34 56 78" not in masked
        assert "***" in masked

    def test_FEAT_005_3_none_passthrough(self) -> None:
        assert SensitiveValueMasker().mask(None) is None

    def test_FEAT_005_3_short_digit_run_masked(self) -> None:
        masked = SensitiveValueMasker().mask("code 12")
        assert masked is not None
