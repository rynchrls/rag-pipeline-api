from app.db.session import db_session
from sqlalchemy.orm import Session
from fastapi import Depends
from app.schemas.message import CreateMessage, GetAllMessages
from app.models.message import Message
from app.models.pipeline import Pipeline
from fastapi import HTTPException, status
from app.rag.embedding.embed import Embedding
from app.rag.vector_search.vdb_search import VectorSearch
from app.rag.augmentation.augment import Augmentation
from app.rag.generate.generate import GenerateResponse
from app.rag.vector_database.vector_db import VectorDatabase
from pathlib import Path
from app.utils.pagination import paginate
from fastapi.responses import StreamingResponse
import json


class MessageRepository:
    def __init__(self):
        self.embedding = Embedding()
        self.vector_search = VectorSearch()
        self.augmentation = Augmentation()
        self.generate = GenerateResponse()
        self.vector_db = VectorDatabase()

    def save_llm_message(
        self, payload: CreateMessage, db: Session = Depends(db_session)
    ):
        try:
            new_message = Message(
                role="system",
                content=payload.content,
                pipeline_id=payload.pipeline_id,
                author_id=payload.author_id,
                agent_name=payload.agent_name,
                conversation_id=payload.conversation_id,
            )
            db.add(new_message)
            db.commit()
            db.refresh(new_message)
            return {"message": "Message created successfully", "data": new_message}
        except Exception as e:
            db.rollback()
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"Creating Message Failed! {str(e)}",
            )

    def create_message(self, payload: CreateMessage, db: Session = Depends(db_session)):
        try:
            # ── 1. Save user message ──────────────────────────────────
            new_message = Message(
                role=payload.role,
                content=payload.content,
                pipeline_id=payload.pipeline_id,
                author_id=payload.author_id,
                agent_name=payload.agent_name,
                conversation_id=payload.conversation_id,
            )
            db.add(new_message)
            db.commit()
            db.refresh(new_message)

            # ── 2. Fetch pipeline to get email (needed for file path) ─
            pipeline = (
                db.query(Pipeline).filter(Pipeline.id == payload.pipeline_id).first()
            )
            if not pipeline:
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail="Pipeline not found",
                )

            # ── 3. Load ChromaDB collection ───────────────────────────
            collection_path = Path(
                f"./app/rag_files/rag_{pipeline.email}/{payload.agent_name}/chroma_db"
            )
            collection = self.vector_db.fetch_collection(collection_path)

            # ── 4. Embed query ────────────────────────────────────────
            query_embedding = self.embedding.process_user_query(payload.content)

            # ── 5. Vector search ──────────────────────────────────────
            search_results = self.vector_search.search(collection, query_embedding)

            # ── 6. Augment prompt ─────────────────────────────────────
            instruction_prompt, context = self.augmentation.augment_prompt_with_context(
                search_results, payload.agent_name
            )

            # ── 7. Generate response ──────────────────────────────────
            def generate_stream():
                full_response = ""
                provider = "ollama"

                yield (
                    json.dumps(
                        {
                            "type": "start",
                            "message": "Message created successfully",
                            "data": {
                                "role": "system",
                                "content": "",
                                "pipeline_id": payload.pipeline_id,
                                "author_id": payload.author_id,
                                "agent_name": payload.agent_name,
                                "conversation_id": payload.conversation_id,
                            },
                        }
                    )
                    + "\n"
                )

                response = self.generate.generate(
                    provider=provider,
                    instruction_prompt=instruction_prompt,
                    context=context,
                    query=payload.content,
                    prev_messages=payload.messages,
                )

                for content in self.generate.stream_text(provider, response):
                    if content:
                        full_response += content
                        yield (
                            json.dumps(
                                {
                                    "type": "chunk",
                                    "content": content,
                                }
                            )
                            + "\n"
                        )

                data = {
                    "role": "system",
                    "content": full_response,
                    "pipeline_id": payload.pipeline_id,
                    "author_id": payload.author_id,
                    "agent_name": payload.agent_name,
                    "conversation_id": payload.conversation_id,
                }

                yield (
                    json.dumps(
                        {
                            "type": "done",
                            "message": "Message created successfully",
                            "data": data,
                        }
                    )
                    + "\n"
                )

            return StreamingResponse(
                generate_stream(),
                media_type="application/x-ndjson",
            )

        except Exception as e:
            db.rollback()
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"Creating Message Failed! {str(e)}",
            )

    def get_all_messages(
        self, payload: GetAllMessages, db: Session = Depends(db_session)
    ):
        try:
            page = max(payload.page, 1) - 1
            limit = min(payload.limit, 100)  # prevent abuse
            author_id = payload.author_id
            pipeline_id = payload.pipeline_id
            conversation_id = payload.conversation_id

            query = db.query(Message)

            if author_id:
                query = query.filter(Message.author_id == author_id)

            if pipeline_id:
                query = query.filter(Message.pipeline_id == pipeline_id)
            if conversation_id:
                query = query.filter(Message.conversation_id == conversation_id)

            total = query.count()

            messages = (
                query.order_by(Message.createdAt.asc())
                .offset(page * limit)
                .limit(limit)
                .all()
            )

            pagination = paginate(total, page, limit, len(messages))

            return {
                "message": "Messages fetched successfully",
                "data": messages,
                "pagination": pagination,
            }

        except Exception as e:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"Getting All Messages Failed! {str(e)}",
            )
