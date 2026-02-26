from app.db.session import db_session
from sqlalchemy.orm import Session
from fastapi import Depends
from app.v1.repository.pipeline import PipelineRepository
from app.schemas.pipeline import CreatePipeline
from typing import List
from fastapi import UploadFile


class PipelineService:
    def __init__(self):
        self.repository = PipelineRepository()

    def create_pipeline(
        self,
        payload: CreatePipeline,
        files: List[UploadFile],
        db: Session = Depends(db_session),
    ):
        return self.repository.create_pipeline(payload, files, db)
