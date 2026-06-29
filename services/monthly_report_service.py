from datetime import datetime
from datetime import timedelta

from sqlalchemy import select, delete
from sqlalchemy.orm import selectinload

from database.db import SessionLocal

from database.models import (
    ReportShare,
    Report,
    Owner,
    Account
)


async def get_owner_monthly_report():

    async with SessionLocal() as session:

        date_from = (
            datetime.utcnow()
            - timedelta(days=30)
        )

        result = await session.execute(
            select(ReportShare)
            .join(Report)
            .options(
                selectinload(
                    ReportShare.owner
                )
            )
            .where(
                Report.created_at >= date_from
            )
        )

        shares = result.scalars().all()

        # { owner_name: {"profit": 0, "id": owner_id} }
        owner_stats = {}
        total_profit = 0

        for share in shares:

            owner_name = share.owner.name
            owner_id = share.owner.id

            if owner_name not in owner_stats:
                owner_stats[owner_name] = {
                    "profit": 0,
                    "id": owner_id
                }

            owner_stats[owner_name]["profit"] += share.amount
            total_profit += share.amount

        return owner_stats, total_profit


async def clear_owner_shares(owner_id: int):

    async with SessionLocal() as session:

        await session.execute(
            delete(ReportShare)
            .where(
                ReportShare.owner_id == owner_id
            )
        )

        await session.commit()


async def get_account_monthly_report():

    async with SessionLocal() as session:

        date_from = (
            datetime.utcnow()
            - timedelta(days=30)
        )

        result = await session.execute(
            select(Report)
            .options(
                selectinload(
                    Report.account
                )
            )
            .where(
                Report.created_at >= date_from
            )
        )

        reports = result.scalars().all()

        account_stats = {}
        total_profit = 0

        for report in reports:

            acc_number = (
                report.account.account_number
            )

            account_stats.setdefault(acc_number, 0)
            account_stats[acc_number] += report.total_price
            total_profit += report.total_price

        return account_stats, total_profit


async def delete_old_reports():

    async with SessionLocal() as session:

        date_limit = (
            datetime.utcnow()
            - timedelta(days=30)
        )

        await session.execute(
            delete(Report)
            .where(
                Report.created_at < date_limit
            )
        )

        await session.commit()