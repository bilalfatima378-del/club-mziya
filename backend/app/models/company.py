import uuid
from typing import TYPE_CHECKING

from sqlalchemy import Enum as SAEnum, ForeignKey, String, Text
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.core.database import Base
from app.models.base import (
    SoftDeleteMixin,
    SubscriptionStatus,
    TimestampMixin,
    uuid_pk,
)

if TYPE_CHECKING:
    from app.models.subscription_plan import SubscriptionPlan
    from app.models.user import User


class Company(Base, TimestampMixin, SoftDeleteMixin):
    __tablename__ = "companies"

    id: Mapped[uuid.UUID] = uuid_pk()
    plan_id: Mapped[uuid.UUID | None] = mapped_column(
        ForeignKey("subscription_plans.id", ondelete="SET NULL"), nullable=True
    )
    name: Mapped[str] = mapped_column(String(255), nullable=False)
    ice_number: Mapped[str] = mapped_column(String(50), nullable=False, unique=True)
    address: Mapped[str | None] = mapped_column(Text, nullable=True)
    subscription_status: Mapped[SubscriptionStatus] = mapped_column(
        SAEnum(SubscriptionStatus, name="subscription_status"),
        default=SubscriptionStatus.TRIAL,
        nullable=False,
    )

    plan: Mapped["SubscriptionPlan | None"] = relationship(back_populates="companies")
    users = relationship("User", back_populates="company")
    invitations = relationship("UserInvitation", back_populates="company")
    invoices = relationship("Invoice", back_populates="company")
