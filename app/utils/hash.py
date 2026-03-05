from passlib.context import CryptContext

pwd_context = CryptContext(schemes=["argon2"], deprecated="auto")


class Hash:
    def bcrypt(self, password: str) -> str:
        hashedPassword = pwd_context.hash(password)
        return hashedPassword

    def verify(
        self,
        password: str,
        hashedPass: str,
    ) -> bool:
        return pwd_context.verify(password, hashedPass)
