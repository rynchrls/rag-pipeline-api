from passlib.context import CryptContext

pwd_cxt = CryptContext(schemes=["bcrypt"], deprecated="auto")


class Hash:
    def bcrypt(self, password: str) -> str:
        hashedPassword = pwd_cxt.hash(password)
        return hashedPassword

    def verify(
        self,
        password: str,
        hashedPass: str,
    ) -> bool:
        return pwd_cxt.verify(password, hashedPass)
