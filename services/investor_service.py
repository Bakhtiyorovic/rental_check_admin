from sqlalchemy import select

from database.db import SessionLocal
from database.models import (
    Account,
    Owner,
    Report,
    ReportShare,
    UserOwner
)


async def get_my_reports(telegram_id: int):

    async with SessionLocal() as session:

        links = (
            await session.scalars(
                select(UserOwner).where(
                    UserOwner.telegram_id == telegram_id
                )
            )
        ).all()

        if not links:
            return "Avval 4 xonali kodingizni kiriting."

        owner_ids = [
            link.owner_id
            for link in links
        ]

        result = await session.execute(
            select(
                Report,
                ReportShare,
                Owner,
                Account
            )
            .join(
                ReportShare,
                ReportShare.report_id == Report.id
            )
            .join(
                Owner,
                Owner.id == ReportShare.owner_id
            )
            .join(
                Account,
                Account.id == Report.account_id
            )
            .where(
                ReportShare.owner_id.in_(owner_ids)
            )
            .order_by(
                Report.created_at.desc(),
                Report.id.desc()
            )
        )

        rows = result.all()

        if not rows:
            return "Hisobotlar mavjud emas."

        text = "📊 Hisobotlar\n\n"

        for report, share, owner, account in rows:

            text += (
                f"👤 {owner.name}\n"
                f"📌 Akkount {account.account_number}\n"
                f"💰 Sizning ulushingiz: "
                f"{share.amount:,} so'm\n"
                f"⏱ {report.hours} soat\n\n"
            )

        return text


async def notify_investors(bot, report_id: int):

    async with SessionLocal() as session:

        result = await session.execute(
            select(
                Report,
                ReportShare,
                Owner,
                Account,
                UserOwner.telegram_id
            )
            .join(
                ReportShare,
                ReportShare.report_id == Report.id
            )
            .join(
                Owner,
                Owner.id == ReportShare.owner_id
            )
            .join(
                Account,
                Account.id == Report.account_id
            )
            .join(
                UserOwner,
                UserOwner.owner_id == Owner.id
            )
            .where(
                Report.id == report_id
            )
        )

        rows = result.all()

        sent = 0

        for (
            report,
            share,
            owner,
            account,
            telegram_id
        ) in rows:

            text = (
                "📊 Yangi hisobot\n\n"
                f"👤 {owner.name}\n"
                f"📌 Akkount {account.account_number}\n"
                f"💰 Sizning ulushingiz: "
                f"{share.amount:,} so'm\n"
                f"⏱ {report.hours} soat"
            )

            try:

                await bot.send_message(
                    chat_id=telegram_id,
                    text=text
                )

                sent += 1

            except Exception as e:

                print(
                    f"Investor xabar yuborishda xato: "
                    f"{telegram_id} -> {e}"
                )

        return sent


async def login_owner(
    code: int,
    telegram_id: int
):

    async with SessionLocal() as session:

        owner = await session.scalar(
            select(Owner).where(
                Owner.secret_id == code
            )
        )

        if not owner:
            return None

        exists = await session.scalar(
            select(UserOwner).where(
                UserOwner.telegram_id == telegram_id,
                UserOwner.owner_id == owner.id
            )
        )

        if not exists:

            session.add(
                UserOwner(
                    telegram_id=telegram_id,
                    owner_id=owner.id
                )
            )

            await session.commit()

        return owner