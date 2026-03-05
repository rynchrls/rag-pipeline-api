from sqlalchemy import Column, DateTime, String, func, Integer, ForeignKey, ARRAY, JSON
from ..db.session import Base


class Pipeline(Base):
    __tablename__ = "pipelines"
    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, index=True)
    agent_name = Column(String, index=True)
    description = Column(String)
    author_id = Column(Integer, ForeignKey("users.id"), index=True)
    stage = Column(Integer)
    file_names = Column(ARRAY(String))
    file_count = Column(Integer)
    email = Column(String)
    rp_metadata = Column(JSON)
    chunks_count = Column(Integer)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
