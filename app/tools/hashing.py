"""
Never save the password in plain text in the DB again.
Use `bcrypt` for the encryption
"""
from passlib.context import CryptContext

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


class Hasher:
    """You can Hash and check a Hashed string with this class"""

    @staticmethod
    def verify_password(plain_password: str, hashed_password: str) -> bool:
        """Check if the password are the same. Uses a safe way to verify to avoid hacks.

        Args:
            plain_password (str): Plain text password
            hashed_password (str): Hashed password from `get_password_hash`

        Returns:
            bool: true or fales if the password is the same
        """
        return pwd_context.verify(plain_password, hashed_password)

    @staticmethod
    def get_password_hash(password: str) -> str:
        """Get a hashed value of a string

        Args:
            password (str): Password to hash

        Returns:
            str: Hashed value
        """
        return pwd_context.hash(password)
