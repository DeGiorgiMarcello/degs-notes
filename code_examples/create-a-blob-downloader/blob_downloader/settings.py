from pydantic_settings import BaseSettings, SettingsConfigDict
from pydantic.types import SecretStr
from enum import Enum
from pydantic import field_validator
from os import makedirs
from pathlib import Path
from os.path import expanduser, exists


class LogLevels(str, Enum):
    TRACE = "TRACE"
    DEBUG = "DEBUG"
    INFO = "INFO"
    WARNING = "WARNING"
    ERROR = "ERROR"
    CRITICAL = "CRITICAL"


class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=Path("~/.env").expanduser(), env_file_encoding="utf-8", extra="ignore"
    )


    AZURE_BLOB_CONNECTION_STRING: SecretStr = ""
    "Azure Blob Storage connection string"

    AZURE_CONTAINER: str = ""
    "Container from/to pull/push blobs"

    LOG_LEVEL: LogLevels = LogLevels.WARNING
    "Log level. Default to 'WARNING' "

    OUTPUT_FOLDER: str = "~/output"
    "Output folder to save the downloaded blobs"


    @field_validator("OUTPUT_FOLDER")
    @classmethod
    def check_output_folder(cls, v):
        v = expanduser(v)
        if not exists(v):
            makedirs(v, exist_ok=True)
        return v


S = Settings()
