import ast
import json
from typing import AnyStr

from py_temporal_doc.base_types.cls.parser import Parser
from py_temporal_doc.generator.consts import (DECORATOR_TARGET_SET,
                                              DecoratorTargets)
from py_temporal_doc.generator.model.response import Response
from py_temporal_doc.generator.processor.base_processor import BaseProcessor


class Parser(Parser):
    def __init__(
        self,
        doc_workflow_caller_processor: BaseProcessor,
        doc_workflow_schedule_processor: BaseProcessor,
        doc_workflow_sequence_processor: BaseProcessor,
        temporal_activity_processor: BaseProcessor,
        temporal_workflow_processor: BaseProcessor,
        response: Response,
    ):
        self.__decorator_target_processor_mapper: dict[str, BaseProcessor] = {
            DecoratorTargets.DOC_WORKFLOW_CALLER.value: doc_workflow_caller_processor,
            DecoratorTargets.DOC_WORKFLOW_SCHEDULE.value: doc_workflow_schedule_processor,
            DecoratorTargets.DOC_WORKFLOW_SEQUENCE.value: doc_workflow_sequence_processor,
            DecoratorTargets.TEMPORAL_ACTIVITY.value: temporal_activity_processor,
            DecoratorTargets.TEMPORAL_WORKFLOW.value: temporal_workflow_processor,
        }
        self.__response: Response = response

    def parse(self, file_str: AnyStr, path: str):
        """
        Builds the mapping

        Returns:

        """
        ast_tree = ast.parse(file_str)

        for node in ast.walk(ast_tree):
            if (
                isinstance(node, ast.FunctionDef)
                or isinstance(node, ast.AsyncFunctionDef)
                or isinstance(node, ast.ClassDef)
            ):
                for decorator in node.decorator_list:
                    complete_decorator_name: str = ""

                    try:
                        if isinstance(decorator, ast.Name):
                            complete_decorator_name = decorator.id
                        elif isinstance(decorator, ast.Call):
                            complete_decorator_name = decorator.func.id
                        elif isinstance(decorator, ast.Attribute):
                            complete_decorator_name = (
                                f"{decorator.value.id}.{decorator.attr}"
                            )
                    except Exception:
                        continue

                    if complete_decorator_name != "" and (
                        complete_decorator_name in DECORATOR_TARGET_SET
                    ):
                        if (
                            complete_decorator_name
                            in self.__decorator_target_processor_mapper
                        ):
                            self.__decorator_target_processor_mapper[
                                complete_decorator_name
                            ].build(self.__response, node, decorator, path)

    def get_json(self) -> str:
        return self.__response.json()
