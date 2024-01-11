from abc import ABC, abstractmethod
from typing import AnyStr


class Parser(ABC):
    @abstractmethod
    def parse(self, file_str: AnyStr, path: str):
        pass

    @abstractmethod
    def get_json(self) -> str:
        pass
