from re import match as re_match
from typing import Any, Dict, List, Type, Union

from pydantic import AnyHttpUrl, PostgresDsn, field_validator, model_validator
from pydantic_settings import BaseSettings


class CoreSettings(BaseSettings):
    """
    Common collection of settings, kept as simple as possible.

    """

    SERVER_NAME: str
    BACKEND_CORS_ORIGINS: List[AnyHttpUrl] = []

    @field_validator("BACKEND_CORS_ORIGINS")
    def assemble_cors_origins(cls, v: Union[str, List[str]]) -> Union[List[str], str]:
        if isinstance(v, str) and not v.startswith("["):
            return [i.strip() for i in v.split(",")]
        elif isinstance(v, (list, str)):
            return v
        raise ValueError(v)

    POSTGRES_SERVER: str
    POSTGRES_USER: str
    POSTGRES_PASSWORD: str
    POSTGRES_DB: str
    SQLALCHEMY_DATABASE_URI: PostgresDsn | None = None

    @model_validator(mode="before")
    def assemble_db_connection(cls, values: Dict[str, Any]) -> Any:
        if values.get("SQLALCHEMY_DATABASE_URI"):
            return values
        values["SQLALCHEMY_DATABASE_URI"] = PostgresDsn.build(
            scheme="postgresql",
            username=values.get("POSTGRES_USER"),
            password=values.get("POSTGRES_PASSWORD"),
            host=values.get("POSTGRES_SERVER"),
            port=values.get("POSTGRES_PORT"),
            path=f"{values.get('POSTGRES_DB') or ''}",
        )
        return values

    # If using AWS as a backend platform, we recomend using role-scoped permissions
    # The IAM account specified here should be able to assume the given role
    # when required
    AWS_ACCESS_KEY: str | None = None
    AWS_SECRET_KEY: str | None = None
    AWS_REGION_NAME: str | None = None
    AWS_ROLE_ARN: str | None = None
    AWS_ROLE_SESSION_NAME: str | None = None

    @field_validator("AWS_ROLE_ARN")
    def validate_arn(cls, v):
        if not v:
            return v

        pattern = r"^arn:aws:iam::[0-9]{12}:role\/[\w+=,.@-]+$"

        if not re_match(pattern, v):
            raise ValueError(f"Invalid AWS role ARN: {v} (required format: {pattern})")

        return v


_settings_class: Type[CoreSettings] | None = None


def register_settings(settings: Type[CoreSettings]):
    """
    Register a client settings object with the lassen application.

    """
    global _settings_class
    _settings_class = settings


def get_settings():
    global _settings
    if _settings_class is None:
        raise ValueError(
            "No settings registered at runtime by client application.\n"
            "To register, wrap your CoreSettings subclass with @register_settings"
        )
    return _settings_class()
