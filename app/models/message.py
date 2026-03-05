from sqlalchemy import Column, DateTime, String, func, Integer, ForeignKey
from ..db.session import Base


class Message(Base):
    __tablename__ = "messages"
    id = Column(Integer, primary_key=True, index=True)
    role = Column(String)
    content = Column(String)
    pipeline_id = Column(Integer, ForeignKey("pipelines.id"), index=True)
    author_id = Column(Integer, ForeignKey("users.id"), index=True)
    conversation_id = Column(Integer, ForeignKey("conversations.id"), index=True)
    agent_name = Column(String, index=True)
    createdAt = Column(DateTime, default=func.now())
    updatedAt = Column(DateTime, default=func.now(), onupdate=func.now())
