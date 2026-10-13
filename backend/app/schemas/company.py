from datetime import datetime
from typing import Literal
from uuid import UUID

from pydantic import BaseModel, ConfigDict, Field


class CompanyCreate(BaseModel):
    name: str = Field(min_length=2, max_length=255)
    ice_number: str = Field(min_length=5, max_length=50)
    address: str | None = None
    plan_id: UUID | None = None
    subscription_status: Literal["TRIAL", "ACTIVE", "PAST_DUE", "CANCELED"] = "TRIAL"


class CompanyUpdate(BaseModel):
    name: str | None = Field(default=None, min_length=2, max_length=255)
    ice_number: str | None = Field(default=None, min_length=5, max_length=50)
    address: str | None = None
    plan_id: UUID | None = None
    subscription_status: Literal["TRIAL", "ACTIVE", "PAST_DUE", "CANCELED"] | None = None
    is_active: bool | None = None


class CompanyRead(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: UUID
    plan_id: UUID | None
    name: str
    ice_number: str
    address: str | None
    subscription_status: str
    is_active: bool
    created_at: datetime
    updated_at: datetime
