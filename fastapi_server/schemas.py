from pydantic import BaseModel, Field
from typing import Optional


class TaskDTO(BaseModel):
    id: Optional[int] = Field(default=None)
    text: str
    date: str
