import uuid
from datetime import datetime
from typing import TYPE_CHECKING

from sqlalchemy import DateTime, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.core.database import Base
from app.models.base import SoftDeleteMixin, TimestampMixin, uuid_pk

if TYPE_CHECKING:
    from app.models.offer import Offer
    from app.models.product_service import ProductService
    from app.models.user import User


class OfferRedemption(Base, TimestampMixin, SoftDeleteMixin):
    __tablename__ = "offer_redemptions"

    id: Mapped[uuid.UUID] = uuid_pk()
    offer_id: Mapped[uuid.UUID | None] = mapped_column(
        ForeignKey("offers.id", ondelete="SET NULL"), nullable=True, index=True
    )
    product_id: Mapped[uuid.UUID | None] = mapped_column(
        ForeignKey("products_services.id", ondelete="SET NULL"), nullable=True, index=True
    )
    user_id: Mapped[uuid.UUID] = mapped_column(
        ForeignKey("users.id", ondelete="CASCADE"), nullable=False, index=True
    )
    redeemed_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), nullable=False)

    offer: Mapped["Offer | None"] = relationship(back_populates="redemptions")
    product: Mapped["ProductService | None"] = relationship(back_populates="redemptions")
    user: Mapped["User"] = relationship(back_populates="redemptions")
