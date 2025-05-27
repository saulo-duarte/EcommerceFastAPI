import re

import bcrypt
from pydantic import BaseModel, field_validator


class Password(BaseModel):
    raw: str

    @field_validator("raw")
    @classmethod
    def validate_password(cls, v: str) -> str:
        pattern = re.compile(r"^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*[!@#$%^&*(),.?\":{}|<>]).{8,}$")
        if not pattern.match(v):
            raise ValueError("Password must be at least 8 characters and include uppercase, lowercase, digit, and special char.")
        return v

    def hash(self) -> str:
        salt = bcrypt.gensalt()
        hashed = bcrypt.hashpw(self.raw.encode(), salt)
        return hashed.decode()

    def verify(self, hashed_password: str) -> bool:
        return bcrypt.checkpw(self.raw.encode(), hashed_password.encode())
