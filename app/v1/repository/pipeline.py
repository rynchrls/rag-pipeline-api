from app.db.session import db_session
from sqlalchemy.orm import Session
from fastapi import Depends
from app.schemas.pipeline import CreatePipeline
from app.models.pipeline import Pipeline
from typing import List
from fastapi import UploadFile
from fastapi import HTTPException, status
from pathlib import Path
import shutil


class PipelineRepository:
    def create_pipeline(
        self,
        payload: CreatePipeline,
        files: List[UploadFile],
        db: Session = Depends(db_session),
    ):
        try:
            # ---------------------------
            # 1️⃣ Create DB Record First
            # ---------------------------
            new_pipeline = Pipeline(
                title=payload.title,
                agent_name=payload.agent_name,
                description=payload.description,
                author_id=payload.author_id,
            )

            db.add(new_pipeline)
            db.commit()
            db.refresh(new_pipeline)

            # ---------------------------
            # 2️⃣ Prepare Folder Path
            # ---------------------------
            base_path = Path("app/rag_files")  # updated folder path
            user_folder = base_path / f"rag_{payload.email}"

            # Create folder if it doesn't exist
            user_folder.mkdir(parents=True, exist_ok=True)

            # ---------------------------
            # 3️⃣ Save Uploaded Files
            # ---------------------------
            for file in files:
                file_path = user_folder / file.filename
                with file_path.open("wb") as buffer:
                    shutil.copyfileobj(file.file, buffer)

            return new_pipeline

        except Exception as e:
            db.rollback()
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"Creating Pipeline Failed! {str(e)}",
            )
