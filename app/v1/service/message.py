from app.db.session import db_session
from sqlalchemy.orm import Session
from fastapi import Depends
from app.v1.repository.message import MessageRepository
from app.schemas.message import CreateMessage, GetAllMessages


class MessageService:
    def __init__(self):
        self.repository = MessageRepository()

    def create_message(
        self,
        payload: CreateMessage,
        db: Session = Depends(db_session),
    ):
        return self.repository.create_message(payload, db)

    def save_llm_message(
        self,
        payload: CreateMessage,
        db: Session = Depends(db_session),
    ):
        return self.repository.save_llm_message(payload, db)

    def get_all_messages(
        self,
        payload: GetAllMessages = Depends(),
        db: Session = Depends(db_session),
    ):
        return self.repository.get_all_messages(payload, db)
