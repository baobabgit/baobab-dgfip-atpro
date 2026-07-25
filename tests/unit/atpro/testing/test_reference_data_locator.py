"""Tests de ReferenceDataLocator.

:spec: FEAT-013.1
"""

from __future__ import annotations

from pathlib import Path

import pytest

from atpro.testing.reference_data_locator import ReferenceDataLocator


class TestReferenceDataLocator:
    """Comportement du localisateur sans marqueur reference.

    :spec: FEAT-013.1
    """

    def test_FEAT_013_1_unset_env_not_configured(self) -> None:
        locator = ReferenceDataLocator(env={})
        assert locator.is_configured() is False
        assert locator.resolve_dir() is None
        assert locator.is_empty() is True
        assert list(locator.iter_csv_files()) == []

    def test_FEAT_013_1_blank_env_not_configured(self) -> None:
        locator = ReferenceDataLocator(env={ReferenceDataLocator.ENV_VAR: "  "})
        assert locator.is_configured() is False
        assert locator.resolve_dir() is None

    def test_FEAT_013_1_configured_empty_dir(
        self, tmp_path: Path, monkeypatch: pytest.MonkeyPatch
    ) -> None:
        monkeypatch.setenv(ReferenceDataLocator.ENV_VAR, str(tmp_path))
        locator = ReferenceDataLocator()
        assert locator.is_configured() is True
        assert locator.resolve_dir() == tmp_path.resolve()
        assert locator.is_empty() is True
        assert list(locator.iter_csv_files()) == []

    def test_FEAT_013_1_configured_missing_dir(
        self, tmp_path: Path, monkeypatch: pytest.MonkeyPatch
    ) -> None:
        missing = tmp_path / "absent"
        monkeypatch.setenv(ReferenceDataLocator.ENV_VAR, str(missing))
        locator = ReferenceDataLocator()
        assert locator.is_configured() is True
        assert locator.is_empty() is True
        assert list(locator.iter_csv_files()) == []

    def test_FEAT_013_1_lists_csv_only(
        self, tmp_path: Path, monkeypatch: pytest.MonkeyPatch
    ) -> None:
        (tmp_path / "a.csv").write_text("x\n", encoding="utf-8")
        (tmp_path / "b.csv").write_text("y\n", encoding="utf-8")
        (tmp_path / "readme.txt").write_text("no\n", encoding="utf-8")
        monkeypatch.setenv(ReferenceDataLocator.ENV_VAR, str(tmp_path))
        locator = ReferenceDataLocator()
        files = list(locator.iter_csv_files())
        assert locator.is_empty() is False
        assert [p.name for p in files] == ["a.csv", "b.csv"]

    def test_FEAT_013_1_injected_env_mapping(self, tmp_path: Path) -> None:
        (tmp_path / "ref.csv").write_text("h\n", encoding="utf-8")
        locator = ReferenceDataLocator(
            env={ReferenceDataLocator.ENV_VAR: str(tmp_path)}
        )
        assert locator.is_configured() is True
        assert [p.name for p in locator.iter_csv_files()] == ["ref.csv"]
