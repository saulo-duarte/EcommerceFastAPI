import uuid
from datetime import datetime
from typing import Optional
from pydantic import BaseModel, EmailStr, Field
from app.models.value_objects import Password


class UserBase(BaseModel):
   id: uuid.UUID
   email: EmailStr
   hashed_password: str
   full_name: str
   is_active: bool
   is_superuser: bool
   created_at: datetime
   updated_at: datetime

   model_config = {
      "from_attributes": True,
   }


class UserCreate(BaseModel):
   email: EmailStr
   full_name: str = Field(..., min_length=2, max_length=50)
   password: Password

   model_config = {
      "from_attributes": True,
   }


class UserUpdate(BaseModel):
   full_name: Optional[str] = Field(None, min_length=2, max_length=50)
   password: Optional[Password] = None
   is_active: Optional[bool] = None
   is_superuser: Optional[bool] = None

   model_config = {
      "from_attributes": True,
   }

