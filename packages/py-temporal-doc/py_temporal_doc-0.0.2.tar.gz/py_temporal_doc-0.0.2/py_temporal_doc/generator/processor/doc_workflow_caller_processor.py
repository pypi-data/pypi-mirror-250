import ast
from _ast import AST, AsyncFunctionDef, ClassDef, FunctionDef, expr
from typing import List

from py_temporal_doc.generator.model.response import Response
from py_temporal_doc.generator.model.workflow_caller import WorkflowCaller
from py_temporal_doc.generator.processor.base_processor import BaseProcessor


class DocWorkflowCallerProcessor(BaseProcessor):
    def build(
        self,
        response: Response,
        node: ClassDef | AsyncFunctionDef | FunctionDef,
        decorator: expr,
        path: str,
    ) -> None:
        workflow_list: List[str] = (
            [arg.id for arg in decorator.args] if decorator.args else []
        )

        response.callers[node.name] = WorkflowCaller(
            data=workflow_list,
            docstring=ast.get_docstring(node),
            path=path,
        )
