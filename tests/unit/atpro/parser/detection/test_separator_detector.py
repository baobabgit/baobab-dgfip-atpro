"""Tests du detecteur de separateur."""

from __future__ import annotations

from atpro.parser.detection.separator_detector import SeparatorDetector


class TestSeparatorDetector:
    def test_FEAT_002_2_semicolon(self) -> None:
        text = "a;b;c\n1;2;3\n4;5;6\n"
        result = SeparatorDetector().detect(text)
        assert result.separator == ";"
        assert result.confidence > 0.5

    def test_FEAT_002_2_comma(self) -> None:
        text = "a,b,c\n1,2,3\n"
        result = SeparatorDetector().detect(text)
        assert result.separator == ","

    def test_FEAT_002_2_tab(self) -> None:
        text = "a\tb\tc\n1\t2\t3\n"
        result = SeparatorDetector().detect(text)
        assert result.separator == "\t"

    def test_FEAT_002_2_empty_defaults_semicolon(self) -> None:
        result = SeparatorDetector().detect("\n\n")
        assert result.separator == ";"
