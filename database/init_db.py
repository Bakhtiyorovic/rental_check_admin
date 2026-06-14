from database.db import engine
from database.base import Base
from database.models import (
    Account,
    Owner,
    AccountOwner,
    Report
)


async def init_db():

    async with engine.begin() as conn:
        await conn.run_sync(
            Base.metadata.create_all
        )