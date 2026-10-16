from datetime import datetime
from services.account_service import get_all_accounts


async def generate_status_text():
    accounts = await get_all_accounts()
    now = datetime.utcnow()

    if not accounts:
        return "Akkountlar mavjud emas."

    text = "🎮 Akkount statuslari\n\n"

    for account in accounts:
        if (
            account.status == "busy"
            and account.busy_until
            and account.busy_until > now
        ):
            remaining = account.busy_until - now
            total_minutes = int(remaining.total_seconds() // 60)
            hours = total_minutes // 60
            minutes = total_minutes % 60

            text += (
                f"🔴 Akkount {account.account_number}\n"
                f"⏳ {hours} soat {minutes} daqiqa qoldi\n\n"
            )
        else:
            text += (
                f"🟢 Akkount {account.account_number}\n"
                f"Bo'sh\n\n"
            )

    return text