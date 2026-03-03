from app.db.session import db_session
from sqlalchemy.orm import Session
from fastapi import Depends
from app.schemas.pipeline import CreatePipeline
from app.models.pipeline import Pipeline
from typing import List
from fastapi import UploadFile
from fastapi import HTTPException, status
from pathlib import Path
from app.utils.file_handling import HandleFile
from app.rag.load_documents.load import LoadDocuments
from app.rag.chunking.service import ChunkingService
from app.rag.vector_database.vector_db import VectorDatabase


class PipelineRepository:
    file = HandleFile()
    load_doc = LoadDocuments()
    vector_db = VectorDatabase()

    def create_pipeline(
        self,
        payload: CreatePipeline,
        files: List[UploadFile],
        db: Session = Depends(db_session),
    ):
        try:
            exist_pipeline = (
                db.query(Pipeline)
                .filter(
                    Pipeline.id == payload.id,
                    Pipeline.author_id == payload.author_id,
                )
                .first()
            )
            if exist_pipeline:
                return self.update_pipeline(payload, files, db)
            # ---------------------------
            # 1️⃣ Create DB Record First
            # ---------------------------
            new_pipeline = Pipeline(
                title=payload.title,
                agent_name=payload.agent_name,
                description=payload.description,
                author_id=payload.author_id,
                email=payload.email,
                file_names=payload.file_names,
                file_count=payload.file_count,
                stage=payload.stage,
            )

            db.add(new_pipeline)
            db.commit()
            db.refresh(new_pipeline)

            # ---------------------------
            # 2️⃣ Prepare Folder Path
            # ---------------------------
            base_path = Path("app/rag_files")  # updated folder path
            agent_folder = base_path / f"rag_{payload.email}" / payload.agent_name

            # Create folder if it doesn't exist
            agent_folder.mkdir(parents=True, exist_ok=True)

            # ---------------------------
            # 3️⃣ Save Uploaded Files
            # ---------------------------
            self.file.save_files(agent_folder=agent_folder, files=files)

            return {"message": "Pipeline created successfully", "data": new_pipeline}

        except Exception as e:
            db.rollback()
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"Creating Pipeline Failed! {str(e)}",
            )

    def get_pipeline(self, id: int, author_id: int, db: Session = Depends(db_session)):
        try:
            # ✅ Exclude file_names column from query
            pipeline = (
                db.query(Pipeline)
                .filter(Pipeline.id == id, Pipeline.author_id == author_id)
                .first()
            )

            if not pipeline:
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail="Pipeline not found",
                )

            # ✅ Build folder path
            base_path = Path("app/rag_files")
            agent_folder = base_path / f"rag_{pipeline.email}" / pipeline.agent_name

            # ✅ Get all file names inside folder
            files = self.file.get_files(agent_folder=agent_folder)

            # ✅ Attach dynamically (not from DB)
            pipeline.files = files

            collection_path = agent_folder / "chroma_db"
            collection = self.vector_db.get_collection(collection_path)
            data = collection.get()
            chunks = []
            for i in range(len(data["ids"])):
                chunks.append(
                    {
                        "chunk_id": data["ids"][i],
                        "document_id": data["metadatas"][i].get("document_id"),
                        "title": data["metadatas"][i].get("title"),
                        "content": data["documents"][i],
                    }
                )
            pipeline.chunks = chunks

            return pipeline

        except Exception as e:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"Getting Pipeline Failed! {str(e)}",
            )

    def update_pipeline(
        self,
        payload: CreatePipeline,
        files: List[UploadFile],
        db: Session = Depends(db_session),
    ):
        try:
            # ✅ Fetch the existing record
            pipeline = (
                db.query(Pipeline)
                .filter(
                    Pipeline.id == payload.id,
                    Pipeline.author_id == payload.author_id,
                )
                .first()
            )

            if not pipeline:
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail="Pipeline not found",
                )

            # ✅ Update fields from payload
            update_data = payload.dict(exclude_unset=True)
            for key, value in update_data.items():
                setattr(pipeline, key, value)

            db.commit()
            db.refresh(pipeline)

            # ---------------------------
            # 2️⃣ Prepare Folder Path
            # ---------------------------
            base_path = Path("app/rag_files")  # updated folder path
            agent_folder = base_path / f"rag_{payload.email}" / payload.agent_name

            # Create folder if it doesn't exist
            agent_folder.mkdir(parents=True, exist_ok=True)

            # ---------------------------
            # 3️⃣ Save Uploaded Files
            # ---------------------------
            if files:
                self.file.save_files(agent_folder=agent_folder, files=files)

            return {"message": "Pipeline updated successfully", "data": pipeline}
        except Exception as e:
            db.rollback()
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"Updating Pipeline Failed! {str(e)}",
            )

    def chunking_pipeline(
        self,
        payload: CreatePipeline,
        files: List[UploadFile],
        db: Session = Depends(db_session),
    ):
        try:
            pipeline = self.update_pipeline(payload=payload, files=files, db=db)
            if not pipeline:
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail="Pipeline not found",
                )

            documents = self.load_doc.load_documents(
                folder_path=f"./app/rag_files/rag_{payload.email}/{payload.agent_name}"
            )

            metadata = payload.rp_metadata or {}
            strategy = metadata.get("strategy", "sentence")
            chunk_size = metadata.get("size", 500)
            chunk_overlap = metadata.get("overlap", 50)

            chunker = ChunkingService(
                strategy=strategy,
                chunk_size=chunk_size,
                chunk_overlap=chunk_overlap,
            )

            chunks = chunker.chunk_documents(documents)

            self.vector_db.setup_vector_database(
                chunks=chunks,
                collection_path=f"./app/rag_files/rag_{payload.email}/{payload.agent_name}/chroma_db",
            )

            return {
                "message": "Pipeline chunked successfully",
                "data": pipeline["data"],
                "chunks": chunks,
            }
        except Exception as e:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"Chunking Pipeline Failed! {str(e)}",
            )
