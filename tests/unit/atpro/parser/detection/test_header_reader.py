"""Tests du lecteur d'en-tetes."""

from __future__ import annotations

from atpro.parser.detection.header_reader import HeaderReader


class TestHeaderReader:
    def test_FEAT_002_2_quoted_fields(self) -> None:
        text = '"ID de l\'appel";"Nom de l\'agent"\n1;Alice\n'
        columns = HeaderReader().read(text, ";")
        assert columns == ("ID de l'appel", "Nom de l'agent")

    def test_FEAT_002_2_skips_blank_lines(self) -> None:
        text = "\n\nA;B\n1;2\n"
        assert HeaderReader().read(text, ";") == ("A", "B")

    def test_FEAT_002_2_no_header_line(self) -> None:
        assert HeaderReader().read("\n\n", ";") == ()
