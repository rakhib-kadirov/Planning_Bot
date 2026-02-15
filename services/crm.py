from db import SessionLocal
from models import Lead
from aiogram import Bot
from config import ADMIN_IDS, BOT_TOKEN

from sqlalchemy import select
from models import Lead, Company
from db import SessionLocal

bot = Bot(BOT_TOKEN)


async def save_lead(company_id: int, user_id: int, data: dict):
    async with SessionLocal() as session:
        lead = Lead(
            company_id=company_id,
            user_id=user_id,
            name=data.get("name"),
            phone=data.get("phone"),
            comment=data.get("comment"),
        )

        session.add(lead)
        await session.commit()
        
        company = await session.get(Company, company_id)

        # уведомление админов
        text = (
            "📥 New application\n\n"
            f"👤 Company ID: {data['company_id']}\n"
            # f"👤 User ID: {data['user_id']}\n"
            f"👤 Name: {data['name']}\n"
            f"📞 Phone: {data['phone']}\n"
            f"💬 Comment: {data['comment']}"
        )

        if company:
            await bot.send_message(company.owner_tg_id, text)
        
        # for admin_id in ADMIN_IDS:
        #     await bot.send_message(admin_id, text)


async def get_company_telegram_id(company_id: int) -> int | None:
    async with SessionLocal() as session:
        result = await session.execute(
            select(Company).where(Company.id == company_id)
        )
        telegram_id = result.scalar_one_or_none()
        return telegram_id.owner_tg_id if telegram_id else None