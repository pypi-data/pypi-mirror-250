from enum import Enum


class DecoratorTargets (Enum):
    TEMPORAL_WORKFLOW = "workflow.defn"  # Provided by temporal python plugin
    TEMPORAL_ACTIVITY = "activity.defn"  # Provided by temporal python plugin
    DOC_WORKFLOW_SCHEDULE = "doc_workflow_schedule"  # Schedule workflows for documentation
    DOC_WORKFLOW_CALLER = "doc_workflow_caller"  # Workflow caller for documentation
    DOC_WORKFLOW_SEQUENCE = "doc_workflow_sequence"  # Workflow sequence for documentation


DECORATOR_TARGET_SET = {
    DecoratorTargets.TEMPORAL_WORKFLOW.value,
    DecoratorTargets.TEMPORAL_ACTIVITY.value,
    DecoratorTargets.DOC_WORKFLOW_SCHEDULE.value,
    DecoratorTargets.DOC_WORKFLOW_CALLER.value,
    DecoratorTargets.DOC_WORKFLOW_SEQUENCE.value,
}