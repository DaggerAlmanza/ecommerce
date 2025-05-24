from typing import Optional
from pydantic import BaseModel, Field, EmailStr
from enum import Enum


class UserRole(str, Enum):
    user = "USER"
    admin = "ADMIN"


class User(BaseModel):
    username: str = Field(..., description="Username")
    email: EmailStr = Field(..., description="Email")
    password_hash: str = Field(..., description="Password hash")
    role: UserRole = Field(..., description="Role")
    adress: Optional[str] = Field(
        None,
        description="Adress"
    )


class UserAuthentication(BaseModel):
    username: str = Field(..., description="Username")
    email: EmailStr = Field(..., description="Email")
    role: str
    adress: Optional[str] = Field(
        None,
        description="Adress"
    )
