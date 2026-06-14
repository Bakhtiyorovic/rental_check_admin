class Account(Base):
    __tablename__ = "accounts"

    id: Mapped[int] = mapped_column(primary_key=True)

    account_number: Mapped[int] = mapped_column(unique=True)

    status: Mapped[str] = mapped_column(
        String(20),
        default="free"
    )