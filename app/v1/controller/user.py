from fastapi import Depends
from sqlalchemy.orm import Session
from app.schemas.auth import UserCreate, UserLogin
from app.db.session import db_session
from app.v1.service.user import UserService


class UserController:
    def __init__(self):
        self.service = UserService()

    def create_user(self, user: UserCreate, db: Session = Depends(db_session)):
        return self.service.create_user(user, db)

    def login_user(self, user: UserLogin, db: Session = Depends(db_session)):
        return self.service.login_user(user, db)
