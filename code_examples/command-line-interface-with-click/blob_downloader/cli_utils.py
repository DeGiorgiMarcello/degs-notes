from blob_downloader.settings import S
from dotenv import dotenv_values, set_key
from os.path import expanduser
from typing import Any

def read_settings_file() -> dict[str, Any]:
    """Read the settings dotenv file. If no env_path has been found, returns an empty dict."""
    return dotenv_values(S.model_config.get("env_path"))

def update_settings_file(name:str, value: Any):
    """Update the settings dotenv file.

    Args:
        name (str): name of the value to be updated
        value (Any): value to be set
    """
    set_key(S.model_config.get("env_file"), name, value)

