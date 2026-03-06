from pydantic import BaseModel
from typing import Optional, Any


class CreateMessage(BaseModel):
    id: Optional[int] = None
    role: str
    content: str
    pipeline_id: int
    author_id: int
    agent_name: str
    conversation_id: int
    messages: Optional[list[dict[str, Any]]] = None


class GetAllMessages(BaseModel):
    pipeline_id: int
    author_id: int
    conversation_id: int
    page: int
    limit: int
