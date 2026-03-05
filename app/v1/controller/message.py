from fastapi import Depends
from sqlalchemy.orm import Session
from app.db.session import db_session
from app.v1.service.message import MessageService
from app.schemas.message import CreateMessage, GetAllMessages


class MessageController:
    def __init__(self):
        self.service = MessageService()

    def create_message(
        self,
        payload: CreateMessage,
        db: Session = Depends(db_session),
    ):
        return self.service.create_message(payload, db)

    def save_llm_message(
        self,
        payload: CreateMessage,
        db: Session = Depends(db_session),
    ):
        return self.service.save_llm_message(payload, db)

    def get_all_messages(
        self,
        payload: GetAllMessages = Depends(),
        db: Session = Depends(db_session),
    ):
        return self.service.get_all_messages(payload, db)
