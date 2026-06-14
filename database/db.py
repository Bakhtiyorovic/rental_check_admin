from config import (
    DB_HOST,
    DB_PORT,
    DB_NAME,
    DB_USER,
    DB_PASSWORD
)

DATABASE_URL = (
    f"postgresql+asyncpg://"
    f"{DB_USER}:{DB_PASSWORD}"
    f"@{DB_HOST}:{DB_PORT}/{DB_NAME}"
)


from sqlalchemy.ext.asyncio import (
    create_async_engine,
    async_sessionmaker
)


engine = create_async_engine(
    DATABASE_URL,
    echo=True
)

SessionLocal = async_sessionmaker(   # <-- nomini SessionLocal qildik
    engine,
    expire_on_commit=False
)
