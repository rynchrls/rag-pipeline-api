from pydantic import BaseModel
from typing import Optional


class CreateConversation(BaseModel):
    id: Optional[int] = None
    name: Optional[str] = None
    author_id: int


class GetAllConversations(BaseModel):
    id: Optional[int] = None
    name: Optional[str] = None
    author_id: int
    page: int = 1
    limit: int = 10


class GetConversation(BaseModel):
    conversation_id: int
    author_id: int
    page: int = 1
    limit: int = 10
