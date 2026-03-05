from pydantic import BaseModel
from typing import Optional


class CreateMessage(BaseModel):
    id: Optional[int] = None
    role: str
    content: str
    pipeline_id: int
    author_id: int
    agent_name: str
    conversation_id: int


class GetAllMessages(BaseModel):
    pipeline_id: int
    author_id: int
    conversation_id: int
    page: int
    limit: int
