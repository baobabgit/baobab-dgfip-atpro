"""Masquage des mots de passe dans les URL SQLAlchemy.

:spec: FEAT-015.2
"""

from __future__ import annotations

from urllib.parse import urlsplit, urlunsplit


class DatabaseUrlMasker:
    """Masque le mot de passe present dans une URL de connexion.

    :spec: FEAT-015.2
    """

    def mask(self, url: str) -> str:
        """Retourne une URL avec mot de passe remplace.

        :param url: URL SQLAlchemy ou PostgreSQL.
        :type url: str
        :returns: URL avec mot de passe masque.
        :rtype: str
        """
        parts = urlsplit(url)
        if parts.hostname is None and "@" not in parts.netloc:
            return url
        user = parts.username or ""
        host = parts.hostname or ""
        port = f":{parts.port}" if parts.port is not None else ""
        auth = f"{user}:***" if user else "***"
        netloc = f"{auth}@{host}{port}"
        return urlunsplit(
            (parts.scheme, netloc, parts.path, parts.query, parts.fragment)
        )
