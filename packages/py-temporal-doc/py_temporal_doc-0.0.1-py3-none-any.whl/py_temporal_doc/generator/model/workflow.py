from typing import List, Optional

from pydantic import BaseModel

class Workflow(BaseModel):
    data: List[str]
    docstring: Optional[str]
    path: str
