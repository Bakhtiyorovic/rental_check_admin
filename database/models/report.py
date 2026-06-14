from datetime import datetime

from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped
from sqlalchemy.orm import mapped_column
from sqlalchemy.orm import relationship

from database.base import Base


class Report(Base):

    __tablename__ = "reports"

    id: Mapped[int] = mapped_column(
        primary_key=True
    )

    account_id: Mapped[int] = mapped_column(
        ForeignKey("accounts.id")
    )

    hours: Mapped[int]

    total_price: Mapped[int]

    created_at: Mapped[datetime] = mapped_column(
        default=datetime.utcnow
    )

    account = relationship(
        "Account",
        back_populates="reports"
    )

    shares = relationship(
        "ReportShare",
        back_populates="report",
        cascade="all, delete"
    )


class ReportShare(Base):

    __tablename__ = "report_shares"

    id: Mapped[int] = mapped_column(
        primary_key=True
    )

    report_id: Mapped[int] = mapped_column(
        ForeignKey("reports.id")
    )

    owner_id: Mapped[int] = mapped_column(
        ForeignKey("owners.id")
    )

    percent: Mapped[int]

    amount: Mapped[int]

    report = relationship(
        "Report",
        back_populates="shares"
    )

    owner = relationship("Owner")