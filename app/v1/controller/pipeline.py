from fastapi import Depends, UploadFile, File, Query
from sqlalchemy.orm import Session
from app.db.session import db_session
from app.v1.service.pipeline import PipelineService
from app.schemas.pipeline import CreatePipeline, GetAllPipelines
from typing import List, Optional


class PipelineController:
    def __init__(self):
        self.service = PipelineService()

    def create_pipeline(
        self,
        payload: CreatePipeline = Depends(CreatePipeline.as_form),
        files: Optional[List[UploadFile]] = File(None),
        db: Session = Depends(db_session),
    ):

        return self.service.create_pipeline(payload, files, db)

    def get_pipeline(
        self,
        id: int = Query(...),
        author_id: int = Query(...),
        db: Session = Depends(db_session),
    ):
        return self.service.get_pipeline(id, author_id, db)

    def update_pipeline(
        self,
        payload: CreatePipeline = Depends(CreatePipeline.as_form),
        files: Optional[List[UploadFile]] = File(None),
        db: Session = Depends(db_session),
    ):

        return self.service.update_pipeline(payload, files, db)

    def get_all_pipelines(
        self,
        payload: GetAllPipelines = Depends(),
        db: Session = Depends(db_session),
    ):
        return self.service.get_all_pipelines(payload, db)

    def delete_pipeline(
        self,
        id: int = Query(...),
        author_id: int = Query(...),
        agent_name: str = Query(...),
        email: str = Query(...),
        db: Session = Depends(db_session),
    ):
        return self.service.delete_pipeline(id, author_id, agent_name, email, db)
