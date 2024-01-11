from _ast import AST, AsyncFunctionDef, ClassDef, FunctionDef, expr
from typing import Any

from py_temporal_doc.generator.model.response import Response
from py_temporal_doc.generator.processor.base_processor import BaseProcessor


class DocWorkflowScheduleProcessor(BaseProcessor):
    def build(
        self,
        response: Response,
        node: ClassDef | AsyncFunctionDef | FunctionDef,
        decorator: expr,
        path: str,
    ) -> None:
        pass
