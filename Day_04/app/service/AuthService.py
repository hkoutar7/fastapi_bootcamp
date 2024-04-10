from passlib.context import CryptContext

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def get_password_hash(password : str) -> str:
    hashed_password = pwd_context.hash(password)
    return hashed_password


