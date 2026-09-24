from sqlalchemy.orm import Mapped
from sqlalchemy.orm import mapped_column
from sqlalchemy import BigInteger, ForeignKey  # ForeignKey qo'shildi
from database.base import Base


class UserOwner(Base):
    __tablename__ = "user_owners"

    id: Mapped[int] = mapped_column(primary_key=True)
    telegram_id: Mapped[int] = mapped_column(BigInteger)

    # O'ZGARISH: ForeignKey qo'shildi
    owner_id: Mapped[int] = mapped_column(ForeignKey("owners.id", ondelete="CASCADE"))