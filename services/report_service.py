from sqlalchemy import select, delete
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
                .selectinload(AccountOwner.owner)
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
                total_price * relation.percent
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

        await session.commit()

        return shares_text


async def cancel_report_and_free_account(
    account_number: int
):
    async with SessionLocal() as session:

        account = await session.scalar(
            select(Account)
            .where(
                Account.account_number == account_number
            )
        )

        if not account:
            return False

        if account.status != "busy":
            return False

        last_report = await session.scalar(
            select(Report)
            .where(
                Report.account_id == account.id
            )
            .order_by(
                Report.created_at.desc()
            )
        )

        if last_report:
            await session.delete(last_report)

        account.status = "free"
        account.busy_until = None

        await session.commit()

        return True

from services.account_service import get_accounts


async def report_accounts_keyboard():

    accounts = await get_accounts()

    kb = InlineKeyboardBuilder()

    for account in accounts:

        kb.button(
            text=f"Akkount {account.account_number}",
            callback_data=(
                f"report_{account.account_number}"
            )
        )

    kb.adjust(1)

    return kb.as_markup()