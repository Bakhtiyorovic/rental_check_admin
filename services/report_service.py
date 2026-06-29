from sqlalchemy import select
from sqlalchemy.orm import selectinload
from datetime import datetime, timedelta
from database.db import SessionLocal
from database.models import (
    Account,
    AccountOwner,
    Report,
    ReportShare,
    OwnerReport,
    UserOwner,
)
from services.notification_service import send_report

async def create_report(
    account_number: int,
    hours: int,
    total_price: int
):
    async with SessionLocal() as session:

        # 1. Akkountni bazadan qidiramiz
        account = await session.scalar(
            select(Account)
            .where(Account.account_number == account_number)
            .options(
                selectinload(Account.owners)
                .selectinload(AccountOwner.owner)
            )
        )

        # Agar akkount topilmasa, jarayonni to'xtatamiz
        if not account:
            print(f"Xatolik: {account_number} raqamli akkount topilmadi!")
            return []

        # Agar account.id kutilmaganda None bo'lsa, xato bermasligi uchun tekshiruv
        if account.id is None:
            print(f"Xatolik: Akkount topildi, lekin uning ID si yo'q (None)!")
            return []

        # 2. Yangi Report yaratamiz (account_id ni aniq int ko'rinishida beramiz)
        report = Report(
            account_id=int(account.id),
            hours=hours,
            total_price=total_price
        )
        session.add(report)

        # 3. Akkount statusini yangilaymiz
        account.status = "busy"
        account.busy_until = datetime.utcnow() + timedelta(hours=hours)

        # O'zgarishlarni bazaga vaqtincha yozamiz (report.id va statuslar aniq bo'lishi uchun)
        await session.flush()
        # Flushdan keyin obyekti yangilab olamiz (Mabodo sessiyada chalkashlik bo'lsa)
        await session.refresh(report)

        shares_text = []

        for relation in account.owners:
            amount = (total_price * relation.percent) // 100

            owner_report = OwnerReport(
                owner_id=relation.owner.id,
                account_number=account.account_number,
                amount=amount,
                hours=hours
            )
            session.add(owner_report)

            share = ReportShare(
                report_id=report.id,
                owner_id=relation.owner.id,
                percent=relation.percent,
                amount=amount
            )
            session.add(share)

            shares_text.append(f"{relation.owner.name}: {amount:,} so'm")

            # Xabar yuborish qismi
            users = (
                await session.scalars(
                    select(UserOwner)
                    .where(UserOwner.owner_id == relation.owner.id)
                )
            ).all()

            owner_text = (
                f"📊 Yangi hisobot\n\n"
                f"Akkount: {account.account_number}\n"
                f"Soat: {hours}\n"
                f"Umumiy summa: {total_price:,} so'm\n\n"
                f"Sizning foizingiz: {relation.percent}%\n"
                f"Sizning ulushingiz: {amount:,} so'm"
            )

            for user in users:
                await send_report(user.telegram_id, owner_text)

        await session.commit()
        return shares_text