from datetime import datetime, timedelta

from sqlalchemy import select
from sqlalchemy.orm import selectinload

from database.db import SessionLocal

from database.models import (
    ReportShare,
    Report
)


async def get_owner_daily_report():

    async with SessionLocal() as session:

        date_from = (
            datetime.utcnow()
            - timedelta(hours=24)
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

        owner_stats = {}
        total_profit = 0

        for share in shares:

            owner_name = share.owner.name

            owner_stats.setdefault(owner_name, 0)
            owner_stats[owner_name] += share.amount

            total_profit += share.amount

        return owner_stats, total_profit


async def get_account_daily_report():

    async with SessionLocal() as session:

        date_from = (
            datetime.utcnow()
            - timedelta(hours=24)
        )

        result = await session.execute(
            select(Report)
            .options(
                selectinload(Report.account)
            )
            .where(
                Report.created_at >= date_from
            )
        )

        reports = result.scalars().all()

        account_stats = {}
        total_profit = 0

        for report in reports:

            acc_number = report.account.account_number

            account_stats.setdefault(acc_number, 0)
            account_stats[acc_number] += report.total_price

            total_profit += report.total_price

        return account_stats, total_profit