from _ast import ClassDef, AsyncFunctionDef, FunctionDef, expr
from abc import ABC, abstractmethod
from typing import Any

from py_temporal_doc.generator.model.response import Response


class BaseProcessor(ABC):
    @abstractmethod
    def build(self, response: Response, node: ClassDef | AsyncFunctionDef | FunctionDef, decorator: expr, path: str) -> None:
        pass
