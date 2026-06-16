from sqlalchemy import select
from database.db import SessionLocal
from database.models import Owner, OwnerReport, UserOwner

async def get_my_reports(telegram_id: int):
    async with SessionLocal() as session:
        # 1. Telegram ID orqali ushbu foydalanuvchiga biriktirilgan Owner ID larni olamiz
        links = (
            await session.scalars(
                select(UserOwner).where(UserOwner.telegram_id == telegram_id)
            )
        ).all()

        # Agar foydalanuvchi hali ro'yxatdan (login) o'tmagan bo'lsa
        if not links:
            return "Avval 4 xonali kodingizni kiriting."

        owner_ids = [link.owner_id for link in links]

        # 2. Ushbu owner_ids larga tegishli barcha hisobotlarni olamiz
        reports = (
            await session.scalars(
                select(OwnerReport)
                .where(OwnerReport.owner_id.in_(owner_ids))
                .order_by(OwnerReport.id.desc())
            )
        ).all()

        if not reports:
            return "Hisobotlar mavjud emas."

        # 3. Agar owner ismini chiqarmoqchi bo'lsak, birinchi owner_id orqali nomini olamiz
        # (Yoki har bir report ichida owner ma'lumotini chiqarish ham mumkin)
        first_owner = await session.scalar(
            select(Owner).where(Owner.id == owner_ids[0])
        )
        owner_name = first_owner.name if first_owner else "Kompaniya"

        text = f"{owner_name} hisobotlari\n\n"

        for report in reports:
            text += (
                f"📌 {report.account_number}\n"
                f"💰 {report.amount:,}\n"
                f"⏱ {report.hours} soat\n\n"
            )

        return text


async def login_owner(code: int, telegram_id: int):
    async with SessionLocal() as session:
        # Maxfiy kod orqali ownerni topamiz
        owner = await session.scalar(
            select(Owner).where(Owner.secret_id == code)
        )

        if not owner:
            return None

        # Foydalanuvchi allaqachon bu ownerga bog'langanmi yo'qmi tekshiramiz
        exists = await session.scalar(
            select(UserOwner).where(
                UserOwner.telegram_id == telegram_id,
                UserOwner.owner_id == owner.id
            )
        )

        # Agar bog'lanmagan bo'lsa, yangi bog'liqlik yaratamiz
        if not exists:
            session.add(
                UserOwner(
                    telegram_id=telegram_id,
                    owner_id=owner.id
                )
            )
            await session.commit()

        return owner