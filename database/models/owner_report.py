from datetime import datetime

from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped
from sqlalchemy.orm import mapped_column

from database.base import Base


class OwnerReport(Base):

    __tablename__ = "owner_reports"

    id: Mapped[int] = mapped_column(
        primary_key=True
    )

    owner_id: Mapped[int] = mapped_column(
        ForeignKey("owners.id")
    )

    account_number: Mapped[int]

    amount: Mapped[int]

    hours: Mapped[int]

    created_at: Mapped[datetime] = mapped_column(
        default=datetime.utcnow
    )