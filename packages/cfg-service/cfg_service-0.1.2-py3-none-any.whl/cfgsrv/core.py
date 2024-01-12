import abc
from typing import Any


class ParameterNotFound(Exception):
    """Exception if not found parameter in config service."""

    def __init__(self, key: str):
        self.key = key
        super().__init__(f'Parameter with key "{key}" not found in config service')


class ConfigService(abc.ABC):
    def __getitem__(self, key: str) -> Any:
        value = self.get(key)
        if value is None:
            raise ParameterNotFound(key)
        return value

    def __contains__(self, key: str) -> bool:
        return self.get(key) is not None

    @abc.abstractmethod
    def get(self, key: str) -> Any:
        ...
