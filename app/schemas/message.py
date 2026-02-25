from pydantic import BaseModel
from datetime import datetime


class Message(BaseModel):
    id: str
    role: str
    content: str
    pipeline_id: str
    user_id: str
    createdAt: datetime
    updatedAt: datetime
