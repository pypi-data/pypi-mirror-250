"""Config services composed by other config services"""


import re
from typing import Any

from copy import deepcopy
from cfgsrv.core import ConfigService


class StackedConfigService(ConfigService):
    """Find a variable value within a stack of config services"""

    def __init__(self, *config_services: ConfigService):
        self._services = tuple(reversed(config_services))

    def get(self, key: str, default: Any | None = None) -> Any:
        """Return value of key in any of the injected service configs."""
        dict_var = []
        for service in self._services:
            value = service.get(key)
            if value:
                if type(value) is list:
                    return deepcopy(value)
                elif type(value) is dict:
                    dict_var.append(value)
                else:
                    return value

        if dict_var:
            result = dict_var.pop()
            for value in dict_var:
                result.update(value)
            return result

        return default


class InterpolationConfigService(ConfigService):
    """Service with capacity of interpolation in variables."""

    _pattern = re.compile(r"\$\{(.+?)\}")

    def __init__(self, config_service: ConfigService):
        self._config = config_service

    def get(self, key: str, default: Any | None = None) -> Any:
        """Return value, if there are variables, they will be replaced."""
        value = self._config.get(key)
        if value is None:
            return default

        return self._construct_value(value)

    def _construct_value(self, value: Any):
        if type(value) is dict:
            result = {}
            for key, value_ in value.items():
                result[key] = self._construct_value(value_)
            return result

        if type(value) is str:
            if not self._pattern.search(value):
                return value

            value = self._pattern.sub(self._replacement, value)
            if value == "":
                return

            return value

        return value

    def _replacement(self, match):
        key = match.group(1)
        if self.get(key) is not None:
            return str(self.get(key))
