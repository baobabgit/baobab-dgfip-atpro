"""Configuration centralisee de connexion PostgreSQL.

:spec: FEAT-015.2
"""

from __future__ import annotations

from pydantic import Field, field_validator
from pydantic_settings import BaseSettings, SettingsConfigDict

from atpro.infrastructure.config.database_configuration_error import (
    DatabaseConfigurationError,
)
from atpro.infrastructure.config.database_url_masker import DatabaseUrlMasker


class DatabaseSettings(BaseSettings):
    """Source unique de configuration PostgreSQL pour atpro.

    Priorite : ``ATPRO_DATABASE_URL`` si fournie, sinon assemblage depuis
    host / port / name / user / password.

    :spec: FEAT-015.2
    """

    model_config = SettingsConfigDict(
        env_prefix="ATPRO_",
        env_file=".env",
        env_file_encoding="utf-8",
        extra="ignore",
    )

    database_url: str | None = Field(default=None)
    database_host: str = Field(default="localhost")
    database_port: int = Field(default=5432)
    database_name: str = Field(default="atpro")
    database_user: str = Field(default="atpro")
    database_password: str = Field(default="atpro")
    database_driver: str = Field(default="postgresql+psycopg")

    @field_validator("database_url", mode="before")
    @classmethod
    def _empty_url_as_none(cls, value: object) -> object:
        """Normalise une URL vide en ``None``.

        :param value: Valeur brute issue de l'environnement.
        :returns: ``None`` si chaine vide, sinon la valeur.
        """
        if isinstance(value, str) and not value.strip():
            return None
        return value

    def sqlalchemy_url(self) -> str:
        """Construit l'URL SQLAlchemy sans ouvrir de connexion.

        :returns: URL de connexion PostgreSQL.
        :rtype: str
        :raises DatabaseConfigurationError: Si la configuration est incomplete.
        """
        if self.database_url is not None:
            return self.database_url
        missing = [
            name
            for name, value in (
                ("ATPRO_DATABASE_HOST", self.database_host),
                ("ATPRO_DATABASE_NAME", self.database_name),
                ("ATPRO_DATABASE_USER", self.database_user),
                ("ATPRO_DATABASE_PASSWORD", self.database_password),
            )
            if not str(value).strip()
        ]
        if missing:
            raise DatabaseConfigurationError(
                "Configuration PostgreSQL incomplete : variables manquantes "
                f"{', '.join(missing)}. Fournissez ATPRO_DATABASE_URL ou les "
                "composants de connexion."
            )
        password = self.database_password
        return (
            f"{self.database_driver}://{self.database_user}:{password}"
            f"@{self.database_host}:{self.database_port}/{self.database_name}"
        )

    def masked_sqlalchemy_url(self) -> str:
        """Retourne l'URL SQLAlchemy avec mot de passe masque.

        :returns: URL masquee pour logs et diagnostics.
        :rtype: str
        :raises DatabaseConfigurationError: Si la configuration est incomplete.
        """
        return DatabaseUrlMasker().mask(self.sqlalchemy_url())

    def __repr__(self) -> str:
        """Representation sans secret en clair.

        :returns: Representation sure.
        :rtype: str
        """
        try:
            url = self.masked_sqlalchemy_url()
        except DatabaseConfigurationError:
            url = "<unconfigured>"
        return f"DatabaseSettings(url={url!r})"
