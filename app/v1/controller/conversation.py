from fastapi import Depends
from sqlalchemy.orm import Session
from app.db.session import db_session
from app.v1.service.conversation import ConversationService
from app.schemas.conversation import (
    CreateConversation,
    GetAllConversations,
    GetConversation,
    DeleteConversation,
)


class ConversationController:
    def __init__(self):
        self.service = ConversationService()

    def create_conversation(
        self,
        payload: CreateConversation,
        db: Session = Depends(db_session),
    ):
        return self.service.create_conversation(payload, db)

    def get_all_conversations(
        self,
        payload: GetAllConversations = Depends(),
        db: Session = Depends(db_session),
    ):
        return self.service.get_all_conversations(payload, db)

    def get_conversation(
        self,
        payload: GetConversation = Depends(),
        db: Session = Depends(db_session),
    ):
        return self.service.get_conversation(payload, db)

    def delete_conversation(
        self,
        conversation_id: int,
        author_id: int,
        db: Session = Depends(db_session),
    ):
        payload = DeleteConversation(
            conversation_id=conversation_id,
            author_id=author_id,
        )
        return self.service.delete_conversation(payload, db)
