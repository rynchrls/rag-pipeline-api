from app.db.session import db_session
from sqlalchemy.orm import Session
from fastapi import Depends
from app.schemas.auth import UserCreate, UserLogin
from app.v1.repository.user import UserRepository


class UserService:
    def __init__(self):
        self.repository = UserRepository()

    def create_user(self, user: UserCreate, db: Session = Depends(db_session)):
        return self.repository.create_user(user, db)

    def login_user(self, user: UserLogin, db: Session = Depends(db_session)):
        return self.repository.login_user(user, db)
