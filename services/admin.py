from sqlalchemy import select
from datetime import datetime, timedelta
from db import SessionLocal
from models import Subscription

async def get_active_subscriptions(company_id: int):
    async with SessionLocal() as session:
        result = await session.execute(
            select(Subscription).where(Subscription.company_id == company_id, Subscription.expires_at > datetime.utcnow())
        )
        return result.scalars().all()

async def get_user_subscription(user_id: int):
    async with SessionLocal() as session:
        result = await session.execute(
            select(Subscription).where(
                Subscription.user_id == user_id
            )
        )
        return result.scalar_one_or_none()

async def extend_subscription(user_id: int, days: int):
    async with SessionLocal() as session:
        sub = await session.scalar(
            select(Subscription).where(Subscription.user_id == user_id)
        )
        if not sub:
            return False
        
        sub.expires_at += timedelta(days=days)
        sub.notified = False  # Сброс флага уведомления при продлении
        await session.commit()
        return True
    
async def disable_subscription(user_id: int):
    async with SessionLocal() as session:
        sub = await session.scalar(
            select(Subscription).where(Subscription.user_id == user_id)
        )
        if not sub:
            return False
        
        sub.expires_at = datetime.utcnow()  # Устанавливаем дату окончания на текущую
        await session.commit()
        return True
    
async def create_subscription(user_id: int, company_id: int, tariff: str, expires_at: datetime):
    async with SessionLocal() as session:
        sub = Subscription(
            user_id=user_id,
            company_id=company_id,
            tariff=tariff,
            expires_at=expires_at
        )
        session.add(sub)
        await session.commit()