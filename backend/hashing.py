from passlib.context import CryptContext

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


class Hash:
    def bcrypt(password: str) -> str:
        """Kthen password e enkriptuar."""
        return pwd_context.hash(password)

    def verify(plain_password: str, hashed_password: str) -> bool:
        """E shikon nëse passwordi i dhënë përputhet me atë të enkriptuar."""
        return pwd_context.verify(plain_password, hashed_password)
