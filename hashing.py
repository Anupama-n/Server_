from passlib.context import CryptContext

# Password hashing context
bcrypt_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def get_password_hash(password: str) -> str:
    return bcrypt_context.hash(password)
