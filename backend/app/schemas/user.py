from datetime import datetime
from typing import Literal
from uuid import UUID

from pydantic import BaseModel, ConfigDict, EmailStr, Field


class UserCreate(BaseModel):
    company_id: UUID | None = None
    merchant_id: UUID | None = None
    role: Literal["SUPER_ADMIN", "HR_ADMIN", "EMPLOYEE", "MERCHANT_ADMIN"] = "EMPLOYEE"
    first_name: str = Field(min_length=1, max_length=100)
    last_name: str = Field(min_length=1, max_length=100)
    email: EmailStr
    password: str = Field(min_length=8, max_length=128)


class UserUpdate(BaseModel):
    company_id: UUID | None = None
    merchant_id: UUID | None = None
    role: Literal["SUPER_ADMIN", "HR_ADMIN", "EMPLOYEE", "MERCHANT_ADMIN"] | None = None
    first_name: str | None = Field(default=None, min_length=1, max_length=100)
    last_name: str | None = Field(default=None, min_length=1, max_length=100)
    email: EmailStr | None = None
    password: str | None = Field(default=None, min_length=8, max_length=128)
    is_active: bool | None = None


class UserRead(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: UUID
    company_id: UUID | None
    merchant_id: UUID | None
    role: str
    first_name: str
    last_name: str
    email: EmailStr
    is_active: bool
    created_at: datetime
    updated_at: datetime
