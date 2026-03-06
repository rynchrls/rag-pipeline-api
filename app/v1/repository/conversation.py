from sqlalchemy.orm import Session
from fastapi import Depends, HTTPException, status
from app.db.session import db_session
from app.schemas.conversation import (
    CreateConversation,
    GetAllConversations,
    GetConversation,
    DeleteConversation,
)
from app.models.conversation import Conversation
from app.models.message import Message
from app.utils.pagination import paginate


class ConversationRepository:
    def create_conversation(
        self, payload: CreateConversation, db: Session = Depends(db_session)
    ):
        try:
            new_conversation = Conversation(
                name=payload.name,
                author_id=payload.author_id,
            )
            db.add(new_conversation)
            db.commit()
            db.refresh(new_conversation)
            return {
                "message": "Conversation created successfully",
                "data": new_conversation,
            }
        except Exception as e:
            db.rollback()
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"Creating Conversation Failed! {str(e)}",
            )

    def get_all_conversations(
        self, payload: GetAllConversations, db: Session = Depends(db_session)
    ):
        try:
            page = max(payload.page, 1) - 1
            limit = min(payload.limit, 100)  # prevent abuse

            query = db.query(Conversation)

            if payload.author_id:
                query = query.filter(Conversation.author_id == payload.author_id)

            total = query.count()

            conversations = (
                query.order_by(Conversation.createdAt.desc())
                .offset(page * limit)
                .limit(limit)
                .all()
            )

            pagination = paginate(total, page, limit, len(conversations))

            return {
                "message": "Conversations fetched successfully",
                "data": conversations,
                "pagination": pagination,
            }

        except Exception as e:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"Getting All Conversations Failed! {str(e)}",
            )

    def get_conversation(
        self, payload: GetConversation, db: Session = Depends(db_session)
    ):
        try:
            page = max(payload.page, 1) - 1
            limit = min(payload.limit, 100)

            query = db.query(Message).filter(
                Message.conversation_id == payload.conversation_id,
                Message.author_id == payload.author_id,
            )

            total = query.count()

            messages = (
                query.order_by(Message.createdAt.desc())
                .offset(page * limit)
                .limit(limit)
                .all()
            )

            pagination = paginate(total, page, limit, len(messages))

            return {
                "message": "Conversation fetched successfully",
                "data": messages,
                "pagination": pagination,
            }

        except Exception as e:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"Getting Conversation Failed! {str(e)}",
            )

    def delete_conversation(
        self, payload: DeleteConversation, db: Session = Depends(db_session)
    ):
        try:
            conversation = (
                db.query(Conversation)
                .filter(
                    Conversation.id == payload.conversation_id,
                    Conversation.author_id == payload.author_id,
                )
                .first()
            )

            if not conversation:
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail="Conversation not found",
                )

            # Cascade delete all messages in the conversation
            db.query(Message).filter(
                Message.conversation_id == payload.conversation_id
            ).delete(synchronize_session=False)

            db.delete(conversation)
            db.commit()

            return {"message": "Conversation deleted successfully"}

        except HTTPException:
            raise
        except Exception as e:
            db.rollback()
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"Deleting Conversation Failed! {str(e)}",
            )
