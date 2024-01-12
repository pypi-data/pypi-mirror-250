from . import ConfigService
from typing import Any
import os


class _NestedVariable:
    def __init__(self, get_var, list_var):
        self._get_var = get_var
        self._list_var = list_var

    def get(self, key):
        value = self._get_var(key)
        if value:
            return value

        nested_par = {}
        for key_ in self._list_var():
            if len(key_) > len(key) + 1 and key_[: len(key) + 1] == key + ".":
                sub_key = key_[len(key) + 1 :]
                if sub_key.count(".") > 0:
                    sub_key = sub_key.split(".")[0]
                    value = self.get(f"{key}.{sub_key}")
                else:
                    value = self._get_var(key_)
                nested_par[sub_key] = value

        if nested_par:
            return nested_par


class OsEnvironmentConfigService(ConfigService):
    """Service values from keys inside os environment."""

    def __init__(self):
        self._nested = _NestedVariable(os.environ.get, os.environ.keys)

    def get(self, key: str, default=None):
        """Return value of key or default if not found."""
        value = self._nested.get(key)
        if value:
            return value

        return default


class ConfigMapService(ConfigService):
    """Kubernetes ConfigMap item implementing a ConfigService."""

    def __init__(self, volume: str):
        self._volume = volume
        self._nested = _NestedVariable(self._read_file, self._list_files)

    def _read_file(self, key):
        try:
            with open(os.path.join(self._volume, key), "r") as f:
                return f.read()
        except FileNotFoundError:
            return

    def _list_files(self):
        return [
            f
            for f in os.listdir(self._volume)
            if os.path.isfile(os.path.join(self._volume, f))
        ]

    def get(self, key: str, default: Any | None = None) -> Any:
        """Return value of any variable."""
        value = self._nested.get(key)
        if value:
            return value

        return default
