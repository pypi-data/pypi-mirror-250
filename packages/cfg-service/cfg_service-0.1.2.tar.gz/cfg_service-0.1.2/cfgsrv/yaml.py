"""Loader of yaml files to get config data"""

from .core import ConfigService
from typing import Any
import yaml
import re


def _camel_to_snake(name):
    name = re.sub("(.)([A-Z][a-z]+)", r"\1_\2", name)
    return re.sub("([a-z0-9])([A-Z])", r"\1_\2", name).lower()


def _process_value(var):
    tvar = type(var)
    if tvar is dict:
        result = {}
        for key, value in var.items():
            result[_camel_to_snake(key)] = _process_value(value)
        return result
    elif tvar is list:
        return list([_process_value(item) for item in var])
    return str(var)


class YamlConfigService(ConfigService):
    """Configuration service using yaml file."""

    def __init__(self, filename: str):
        self._data = {}
        with open(filename, "r") as f:
            self._data = _process_value(yaml.load(f, Loader=yaml.FullLoader))

    def get(self, key: str, default: Any | None = None) -> Any:
        """Return the value of a parameter by its key, None if is not found."""
        if "." in key and key not in self._data:
            keys = key.split(".")
            value = None
            for key_ in keys:
                if value is None:
                    value = self._data.get(key_)
                elif type(value) is dict:
                    value = value.get(key_)
                else:
                    return None
        else:
            value = self._data.get(key, default)

        return value
