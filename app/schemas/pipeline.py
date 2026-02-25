from pydantic import BaseModel
from datetime import datetime


class Pipeline(BaseModel):
    id: str
    title: str
    description: str
    pipeline: str
    files: list[str]
    updatedAt: datetime
    createdAt: datetime
    user_id: str
