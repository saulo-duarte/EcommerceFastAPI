import re
from typing import ClassVar

from passlib.context import CryptContext
from pydantic import BaseModel

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


class Password(BaseModel):
    raw: str

    MIN_LENGTH: ClassVar[int] = 8
    PASSWORD_REGEX: ClassVar[re.Pattern] = re.compile(
        r"^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*[!@#$%^&*(),.?\":{}|<>]).{8,}$"
    )

    def validate(self) -> None:
        if not self.PASSWORD_REGEX.match(self.raw):
            raise ValueError(
                "Password must be at least 8 characters and include uppercase, lowercase, digit, and special char."
            )

    def hash(self) -> str:
        self.validate()
        return pwd_context.hash(self.raw)

    def verify(self, hashed_password: str) -> bool:
        return pwd_context.verify(self.raw, hashed_password)

    class Config:
        arbitrary_types_allowed = True
