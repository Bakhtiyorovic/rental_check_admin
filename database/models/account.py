from sqlalchemy import String

from sqlalchemy.orm import Mapped
from sqlalchemy.orm import mapped_column
from sqlalchemy.orm import relationship
from datetime import datetime
from database.base import Base


class Account(Base):

    __tablename__ = "accounts"

    id: Mapped[int] = mapped_column(
        primary_key=True
    )

    account_number: Mapped[int] = mapped_column(
        unique=True
    )

    busy_until: Mapped[datetime | None]
    status: Mapped[str] = mapped_column(
        String(20),
        default="free"
    )

    owners = relationship(
        "AccountOwner",
        back_populates="account",
        cascade="all, delete"
    )

    reports = relationship(
        "Report",
        back_populates="account",
        cascade="all, delete-orphan"
    )