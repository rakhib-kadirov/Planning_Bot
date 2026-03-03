from aiogram import Router
from aiogram.types import Message
from aiogram.fsm.context import FSMContext
from sqlalchemy import select, func
from datetime import datetime, timedelta
from db import SessionLocal
from models import Lead

router = Router()

@router.message(lambda m: m.text == "💳 Statistics")
async def statistics_handler(msg: Message, state: FSMContext):
    data = await state.get_data()
    
    if data.get("role") != "owner":
        # await msg.answer("⚠️ Access denied. This section is only for company owners.")
        return
    
    company_id = data.get("company_id")
    
    one_month_ago = datetime.utcnow() - timedelta(days=30)
    
    if not company_id:
        await msg.answer("❌ Error: Company ID not found.")
        return
    
    # Получаем количество лидов за последние 7 дней
    seven_days_ago = datetime.utcnow() - timedelta(days=30)
    
    async with SessionLocal() as session:
        # Всего заявок
        result_total = await session.execute(
            select(func.count()).where(
                Lead.company_id == company_id,
                Lead.created_at >= seven_days_ago
            )
        )
        total_leads = result_total.scalars().all()
        
        # Повторные клиенты
        result_repeat = await session.execute(
            select(Lead.user_id, func.count(Lead.id))
            .where(
                Lead.company_id == company_id,
                Lead.created_at >= seven_days_ago
            )
            .group_by(Lead.user_id)
            .having(func.count(Lead.id) > 1)
        )
        
        repeat_users = result_repeat.all()
        repeat_count = len(repeat_users)
    
    await msg.answer(
        f"📊 Statistics for the last 30 days:\n\n"
        f"Total leads: {total_leads}\n"
        f"Repeat customers: {repeat_count}"
    )