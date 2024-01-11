from dependency_injector.containers import DeclarativeContainer
from dependency_injector.providers import Factory, Singleton

from py_temporal_doc.generator.consts import DecoratorTargets
from py_temporal_doc.generator.model.response import Response
from py_temporal_doc.generator.parser import Parser
from py_temporal_doc.generator.processor.doc_workflow_caller_processor import DocWorkflowCallerProcessor
from py_temporal_doc.generator.processor.doc_workflow_schedule_processor import DocWorkflowScheduleProcessor
from py_temporal_doc.generator.processor.doc_workflow_sequence_processor import DocWorkflowSequenceProcessor
from py_temporal_doc.generator.processor.temporal_activity_processor import TemporalActivityProcessor
from py_temporal_doc.generator.processor.temporal_workflow_processor import TemporalWorkflowProcessor


class Container(DeclarativeContainer):
    # Processors
    doc_workflow_caller_processor = Singleton(DocWorkflowCallerProcessor)
    doc_workflow_schedule_processor = Singleton(DocWorkflowScheduleProcessor)
    doc_workflow_sequence_processor = Singleton(DocWorkflowSequenceProcessor)
    temporal_activity_processor = Singleton(TemporalActivityProcessor)
    temporal_workflow_processor = Singleton(TemporalWorkflowProcessor)

    # Response data
    response = Singleton(Response)

    parser = Factory(
        Parser,
        doc_workflow_caller_processor=doc_workflow_caller_processor,
        doc_workflow_schedule_processor=doc_workflow_schedule_processor,
        doc_workflow_sequence_processor=doc_workflow_sequence_processor,
        temporal_activity_processor=temporal_activity_processor,
        temporal_workflow_processor=temporal_workflow_processor,
        response=response,
    )
