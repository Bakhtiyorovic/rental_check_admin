from sqlalchemy import select
from sqlalchemy.orm import selectinload
from aiogram.utils.keyboard import InlineKeyboardBuilder
from datetime import datetime, timedelta
from database.db import SessionLocal
from database.models import (
    Account,
    AccountOwner,
    Report,
    ReportShare
)



async def create_report(
    account_number: int,
    hours: int,
    total_price: int
):
    async with SessionLocal() as session:

        account = await session.scalar(
            select(Account)
            .where(
                Account.account_number
                == account_number
            )
            .options(
                selectinload(Account.owners)
                .selectinload(
                    AccountOwner.owner
                )
            )
        )

        report = Report(
            account_id=account.id,
            hours=hours,
            total_price=total_price
        )

        session.add(report)

        account.status = "busy"

        account.busy_until = (
                datetime.utcnow()
                + timedelta(hours=hours)
        )

        await session.flush()

        shares_text = []

        for relation in account.owners:

            amount = (
                total_price *
                relation.percent
            ) // 100

            share = ReportShare(
                report_id=report.id,
                owner_id=relation.owner.id,
                percent=relation.percent,
                amount=amount
            )

            session.add(share)

            shares_text.append(
                f"{relation.owner.name}: "
                f"{amount:,} so'm"
            )

        # account.status = "busy"

        await session.commit()

        return shares_text


from services.account_service import (
    get_accounts
)


async def report_accounts_keyboard():

    accounts = await get_accounts()

    kb = InlineKeyboardBuilder()

    for account in accounts:

        kb.button(
            text=f"Akkount {account.account_number}",
            callback_data=(
                f"report_"
                f"{account.account_number}"
            )
        )

    kb.adjust(1)

    return kb.as_markup()