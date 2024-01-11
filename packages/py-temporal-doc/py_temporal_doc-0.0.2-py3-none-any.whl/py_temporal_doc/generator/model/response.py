from typing import Dict, Optional

from pydantic import BaseModel

from py_temporal_doc.generator.model.temporal_activity import TemporalActivity
from py_temporal_doc.generator.model.workflow import Workflow
from py_temporal_doc.generator.model.workflow_caller import WorkflowCaller


class Response(BaseModel):
    callers: Dict[str, WorkflowCaller] = {}
    workflows: Dict[str, Workflow] = {}
    activities: Dict[str, TemporalActivity] = {}
