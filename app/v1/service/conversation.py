from sqlalchemy.orm import Session
from fastapi import Depends
from app.db.session import db_session
from app.v1.repository.conversation import ConversationRepository
from app.schemas.conversation import (
    CreateConversation,
    GetAllConversations,
    GetConversation,
)


class ConversationService:
    def __init__(self):
        self.repository = ConversationRepository()

    def create_conversation(
        self, payload: CreateConversation, db: Session = Depends(db_session)
    ):
        return self.repository.create_conversation(payload, db)

    def get_all_conversations(
        self, payload: GetAllConversations, db: Session = Depends(db_session)
    ):
        return self.repository.get_all_conversations(payload, db)

    def get_conversation(
        self, payload: GetConversation, db: Session = Depends(db_session)
    ):
        return self.repository.get_conversation(payload, db)
