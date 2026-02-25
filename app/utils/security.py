from datetime import datetime, timedelta, timezone
from typing import Any
from jose import jwt, JWTError
from fastapi import HTTPException
from app.schemas.auth import TokenData
from app.config import settings


class JWTToken:
    __SECRET_KEY: str = settings.SC
    __ALGORITHM: str = settings.ALGORITHM
    __ACCESS_TOKEN_EXPIRE_MINUTES: int = settings.ACCESS_TOKEN_EXPIRE_MINUTES

    def create_access_token(self, data: dict[str, Any]):
        to_encode = data.copy()
        expire = datetime.now(timezone.utc) + timedelta(
            minutes=self.__ACCESS_TOKEN_EXPIRE_MINUTES
        )
        to_encode.update({"exp": expire})
        encoded_token = jwt.encode(
            to_encode, self.__SECRET_KEY, algorithm=self.__ALGORITHM
        )
        return encoded_token

    def verify_token(self, token: str, credentials_exception: HTTPException):
        try:
            payload = jwt.decode(
                token, self.__SECRET_KEY, algorithms=[self.__ALGORITHM]
            )
            username = payload.get("sub")
            if username is None:
                raise credentials_exception
            token_data = TokenData(
                username=username,
                sub=payload.get("sub"),
                id=payload.get("id"),
                exp=payload.get("exp"),
            )
            return token_data
        except JWTError:
            raise credentials_exception
