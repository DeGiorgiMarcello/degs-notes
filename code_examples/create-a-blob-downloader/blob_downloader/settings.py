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
    model_config = SettingsConfigDict(env_file=Path("~/.env").expanduser(), env_file_encoding="utf-8")

    AZURE_ACCOUNT_NAME: str = ""
    "Azure Blob Storage account name"

    AZURE_ACCOUNT_KEY: SecretStr = ""
    "Azure Blob Storage account key"

    AZURE_CONTAINER: str = ""
    "Container from/to pull/push blobs"

    LOG_LEVEL: LogLevels = LogLevels.WARNING
    "Log level. Default to 'WARNING' "

    OUTPUT_FOLDER: str = "~/output"
    "Output folder to save the downloaded blobs"

    @property
    def AZURE_BLOB_CONNECTION_STRING(self):
        conn_str = {
            "DefaultEndpointsProtocol": "https",
            "AccountName": self.AZURE_ACCOUNT_NAME,
            "AccountKey": self.AZURE_ACCOUNT_KEY.get_secret_value(),
            "BlobEndpoint": f"https://{self.AZURE_ACCOUNT_NAME}.blob.core.windows.net/",
            "QueueEndpoint": f"https://{self.AZURE_ACCOUNT_NAME}.queue.core.windows.net/",
            "TableEndpoint": f"https://{self.AZURE_ACCOUNT_NAME}.table.core.windows.net/",
            "FileEndpoint": f"https://{self.AZURE_ACCOUNT_NAME}.file.core.windows.net/",
        }
        return SecretStr(";".join([f"{k}={v}" for k, v in conn_str.items()]))

    @field_validator("OUTPUT_FOLDER")
    @classmethod
    def check_output_folder(cls, v):
        v = expanduser(v)
        if not exists(v):
            makedirs(v, exist_ok=True)
        return v


S = Settings()
