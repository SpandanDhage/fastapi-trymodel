from passlib.context import CryptContext

pwd_cxt = CryptContext(schemes=['bcrypt'], deprecated="auto")


class Hash():
    def bcrypt(plpass: str):
        return pwd_cxt.hash(plpass)

    def verify(normalPassword: str, hashedPassword: str):
        return pwd_cxt.verify(secret=normalPassword, hash=hashedPassword)
