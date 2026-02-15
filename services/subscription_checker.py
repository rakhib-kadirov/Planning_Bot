from datetime import datetime, timedelta
from sqlalchemy import select
from db import SessionLocal
from models import Subscription

async def get_expiring_subscriptions(days_before: int = 3):
    now = datetime.utcnow()
    threshold = now + timedelta(days=days_before)
    
    async with SessionLocal() as session:
        result = await session.execute(
            select(Subscription).where(
                Subscription.expires_at <= threshold,
                Subscription.expires_at > now,
                Subscription.notified == False
            )
        )
        return result.scalars().all()
    
async def mark_as_notified(sub: Subscription):
    async with SessionLocal() as session:
        db_sub = await session.get(Subscription, sub.id)
        if db_sub:
            db_sub.notified = True
            await session.commit()