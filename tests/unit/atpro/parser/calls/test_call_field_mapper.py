"""Tests de CallFieldMapper et PhoneHasher."""

from __future__ import annotations

from atpro.parser.calls.call_field_mapper import CallFieldMapper
from atpro.parser.calls.phone_hasher import PhoneHasher


class TestCallFieldMapper:
    def test_FEAT_005_4_maps_normalized_columns(self) -> None:
        row = CallFieldMapper().map_row(
            2,
            {
                "ID de l'appel": "A1",
                "Numero appelant": "0612345678",
                "Numero appele": "0142000000",
                "Nom de l'agent": "Alice DUPONT",
                "Debut d'appel": "15/06/2026 10:00:00",
                "Fin d'appel": "15/06/2026 10:05:00",
                "Flux": "F1",
                "Service": "S1",
                "Noms de mesures": "Duree de communication",
                "Valeurs de mesures": "120",
            },
        )
        assert row.external_call_id == "A1"
        assert row.measure_name == "Duree de communication"
        assert row.caller == "0612345678"


class TestPhoneHasher:
    def test_FEAT_005_4_hashes_phone(self) -> None:
        digest = PhoneHasher().hash("0612345678")
        assert digest is not None
        assert len(digest) == 64
        assert PhoneHasher().hash(" ") is None
