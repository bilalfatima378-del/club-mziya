import uuid
from decimal import Decimal

from sqlalchemy import Integer, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.core.database import Base
from app.models.base import SoftDeleteMixin, TimestampMixin, uuid_pk


class SubscriptionPlan(Base, TimestampMixin, SoftDeleteMixin):
    __tablename__ = "subscription_plans"

    id: Mapped[uuid.UUID] = uuid_pk()
    name: Mapped[str] = mapped_column(String(100), nullable=False, unique=True)
    price_per_employee: Mapped[Decimal] = mapped_column(nullable=False)
    max_employees: Mapped[int] = mapped_column(Integer, nullable=False)

    companies = relationship("Company", back_populates="plan")
