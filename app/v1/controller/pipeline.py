from fastapi import Depends, UploadFile, File
from sqlalchemy.orm import Session
from app.db.session import db_session
from app.v1.service.pipeline import PipelineService
from app.schemas.pipeline import CreatePipeline


class PipelineController:
    def __init__(self):
        self.service = PipelineService()

    def create_pipeline(
        self,
        payload: CreatePipeline = Depends(CreatePipeline.as_form),
        files: list[UploadFile] = File(...),
        db: Session = Depends(db_session),
    ):

        return self.service.create_pipeline(payload, files, db)
