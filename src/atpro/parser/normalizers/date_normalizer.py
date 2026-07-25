"""Parsing des dates CSV AT Pro.

:spec: FEAT-005.3
"""

from __future__ import annotations

import re
from datetime import datetime
from zoneinfo import ZoneInfo

from atpro.parser.normalizers.normalization_error import NormalizationError

_PARIS = ZoneInfo("Europe/Paris")

_MONTHS_FR: dict[str, int] = {
    "janvier": 1,
    "fevrier": 2,
    "février": 2,
    "mars": 3,
    "avril": 4,
    "mai": 5,
    "juin": 6,
    "juillet": 7,
    "aout": 8,
    "août": 8,
    "septembre": 9,
    "octobre": 10,
    "novembre": 11,
    "decembre": 12,
    "décembre": 12,
}

_FR_DATE = re.compile(
    r"^(?P<day>\d{1,2})\s+(?P<month>[A-Za-zÀ-ÿ]+)\s+(?P<year>\d{4})"
    r"(?:\s+(?P<hour>\d{1,2}):(?P<minute>\d{2})(?::(?P<second>\d{2}))?)?$"
)

_FORMATS: tuple[str, ...] = (
    "%d/%m/%Y %H:%M:%S",
    "%d-%m-%y %H:%M:%S",
    "%Y/%m/%d",
    "%Y/%m/%d %H:%M:%S",
    "%d/%m/%Y",
    "%d-%m-%y",
)


class DateNormalizer:
    """Parse les dates vers ``datetime`` aware ``Europe/Paris``.

    :spec: FEAT-005.3
    """

    def parse(self, value: str, *, column: str | None = None) -> datetime | None:
        """Convertit une date brute.

        Une chaine vide retourne ``None`` (contexte reader).

        :param value: Valeur CSV.
        :param column: Colonne pour le diagnostic.
        :returns: Datetime timezone-aware ou ``None``.
        :raises NormalizationError: Si le format est invalide.
        """
        text = value.strip()
        if text == "":
            return None

        for fmt in _FORMATS:
            try:
                naive = datetime.strptime(text, fmt)
            except ValueError:
                continue
            return naive.replace(tzinfo=_PARIS)

        french = self._parse_french(text)
        if french is not None:
            return french

        raise NormalizationError(
            "DATE_INVALID",
            f"date invalide: {value!r}",
            raw_value=value,
            column=column,
        )

    def _parse_french(self, text: str) -> datetime | None:
        """Parse une date litterale francaise.

        :param text: Ex. ``15 juin 2026`` ou avec heure.
        :returns: Datetime ou ``None`` si non reconnu.
        """
        match = _FR_DATE.fullmatch(text)
        if match is None:
            return None
        month_name = match.group("month").lower()
        month = _MONTHS_FR.get(month_name)
        if month is None:
            return None
        day = int(match.group("day"))
        year = int(match.group("year"))
        hour = int(match.group("hour") or 0)
        minute = int(match.group("minute") or 0)
        second = int(match.group("second") or 0)
        try:
            return datetime(year, month, day, hour, minute, second, tzinfo=_PARIS)
        except ValueError:
            return None
