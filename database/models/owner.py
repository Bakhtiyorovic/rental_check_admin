from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped
from sqlalchemy.orm import mapped_column
from sqlalchemy.orm import relationship
from database.base import Base


class Owner(Base):

    __tablename__ = "owners"

    id: Mapped[int] = mapped_column(
        primary_key=True
    )

    name: Mapped[str]

    secret_id: Mapped[int | None]

    accounts = relationship(
        "AccountOwner",
        back_populates="owner",
        cascade="all, delete"
    )


class AccountOwner(Base):

    __tablename__ = "account_owners"

    id: Mapped[int] = mapped_column(
        primary_key=True
    )

    account_id: Mapped[int] = mapped_column(
        ForeignKey("accounts.id")
    )

    owner_id: Mapped[int] = mapped_column(
        ForeignKey("owners.id")
    )

    percent: Mapped[int]

    account = relationship(
        "Account",
        back_populates="owners"
    )

    owner = relationship(
        "Owner",
        back_populates="accounts"
    )