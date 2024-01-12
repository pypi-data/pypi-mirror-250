from configparser import ConfigParser
from typing import Any

from .core import ConfigService


class IniConfigService(ConfigService):
    """Credentials are stored in a confi.ini file."""

    def __init__(self, filename: str):
        self._config = ConfigParser()
        with open(filename, "r") as f:
            self._config.read_file(f)

    def get(self, key: str, default: str | None = None) -> str | dict[str, Any] | None:
        try:
            values = key.split(".")
            if len(values) == 1:
                return default
            section, key = values
            return self._config[section][key]
        except KeyError:
            return default
        except ValueError:
            return default
