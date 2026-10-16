from sqlalchemy import select
from sqlalchemy.orm import selectinload
from datetime import datetime
from database.db import SessionLocal
from database.models import (
    Account,
    Owner,
    AccountOwner
)


async def account_exists(account_number: int):
    async with SessionLocal() as session:
        result = await session.scalar(
            select(Account).where(Account.account_number == account_number)
        )
        return result is not None


async def create_account(account_number: int, owners_data: list):
    async with SessionLocal() as session:
        account = Account(
            account_number=account_number,
            status="free"
        )
        session.add(account)
        await session.flush()

        for owner_data in owners_data:
            owner = Owner(
                name=owner_data["name"],
                secret_id=owner_data["secret_id"]
            )
            session.add(owner)
            await session.flush()

            relation = AccountOwner(
                account_id=account.id,
                owner_id=owner.id,
                percent=owner_data["percent"]
            )
            session.add(relation)

        await session.commit()


async def delete_account(account_number: int):
    async with SessionLocal() as session:
        account = await session.scalar(
            select(Account).where(Account.account_number == account_number)
        )
        if not account:
            return False

        await session.delete(account)
        await session.commit()
        return True


async def get_accounts():
    await free_expired_accounts()
    async with SessionLocal() as session:
        result = await session.execute(
            select(Account)
            .order_by(Account.account_number)
            .options(
                selectinload(Account.owners).selectinload(AccountOwner.owner)
            )
        )
        return result.scalars().all()


async def generate_accounts_text():
    accounts = await get_accounts()
    if not accounts:
        return "Akkountlar mavjud emas."

    text = ""
    for account in accounts:
        text += f"Akkount {account.account_number}\n"
        for relation in account.owners:
            owner = relation.owner
            if owner.secret_id:
                text += f"{owner.name}({owner.secret_id}) {relation.percent}%\n"
            else:
                text += f"{owner.name} {relation.percent}%\n"
        text += "\n"

    return text


async def free_expired_accounts():
    """Muddati o'tgan akkountlarni hisobotlarni o'chirmasdan bo'shatish"""
    async with SessionLocal() as session:
        now = datetime.utcnow()
        result = await session.execute(
            select(Account).where(Account.status == "busy")
        )
        accounts = result.scalars().all()

        changed = False
        for account in accounts:
            # Agar busy_until vaqti tugagan bo'lsa yoki None bo'lib qolgan bo'lsa
            if account.busy_until is None or account.busy_until <= now:
                account.status = "free"
                account.busy_until = None
                changed = True

        if changed:
            await session.commit()


async def get_free_accounts():
    # Avval muddati o'tganlarni bazada rasman bo'shatib olamiz
    await free_expired_accounts()

    async with SessionLocal() as session:
        result = await session.execute(
            select(Account)
            .where(Account.status == "free")
            .order_by(Account.account_number)
        )
        return result.scalars().all()


async def get_all_accounts():
    # Statuslarni ko'rishdan oldin muddati o'tganlarni yangilab olamiz
    await free_expired_accounts()

    async with SessionLocal() as session:
        result = await session.execute(
            select(Account).order_by(Account.account_number)
        )
        return result.scalars().all()


async def set_account_free(account_number: int):
    async with SessionLocal() as session:
        account = await session.scalar(
            select(Account).where(Account.account_number == account_number)
        )
        if not account:
            return False

        account.status = "free"
        account.busy_until = None
        await session.commit()
        return True


async def get_account_by_number(account_number: int):
    await free_expired_accounts()
    async with SessionLocal() as session:
        return await session.scalar(
            select(Account).where(Account.account_number == account_number)
        )