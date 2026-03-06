from app.db.session import db_session
from sqlalchemy.orm import Session
from fastapi import Depends
from app.schemas.auth import UserCreate, UserLogin
from app.utils.hash import Hash
from app.models.user import User
from sqlalchemy.exc import IntegrityError
from fastapi import HTTPException, status
from app.utils.security import JWTToken


class UserRepository:
    def __init__(self):
        self.hash = Hash()
        self.jwt_token = JWTToken()

    def create_user(self, user: UserCreate, db: Session = Depends(db_session)):
        try:
            hashed_password = self.hash.bcrypt(user.password)
            new_user = User(
                full_name=user.full_name,
                email=user.email,
                password=hashed_password,
            )
            db.add(new_user)
            db.commit()
            db.refresh(new_user)
            del new_user.password
            return new_user
        except IntegrityError as e:
            db.rollback()
            raise HTTPException(status_code=400, detail=str(e))
        except Exception as e:
            db.rollback()
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=str(e),
            )

    def login_user(self, user: UserLogin, db: Session = Depends(db_session)):
        try:
            existing_user = db.query(User).filter(User.email == user.email).first()
            if not existing_user:
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail="User not found",
                )
            if not self.hash.verify(user.password, existing_user.password):
                raise HTTPException(
                    status_code=status.HTTP_401_UNAUTHORIZED,
                    detail="Invalid credentials",
                )
            token = self.jwt_token.create_access_token(
                {"sub": existing_user.email, "id": existing_user.id}
            )
            return {"access_token": token, "token_type": "bearer"}
        except Exception as e:
            print(e)
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=str(e),
            )
