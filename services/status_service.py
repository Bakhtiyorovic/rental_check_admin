from sqlalchemy import select

from database.db import SessionLocal
from database.models import Account

account.status = "busy"

async def make_busy(
    account_number: int
):

    async with SessionLocal() as session:

        account = await session.scalar(
            select(Account)
            .where(
                Account.account_number
                == account_number
            )
        )
        report = Report(
            account_id=account.id,
            hours=hours,
            total_price=total_price
        )

        session.add(report)

        account.status = "busy"

        await session.commit()