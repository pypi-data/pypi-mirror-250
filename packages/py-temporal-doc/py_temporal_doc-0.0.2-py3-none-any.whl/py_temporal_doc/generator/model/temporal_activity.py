from typing import Optional

from pydantic import BaseModel


class TemporalActivity(BaseModel):
    docstring: Optional[str]
    path: str
