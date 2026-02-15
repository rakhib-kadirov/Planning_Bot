from datetime import datetime, timedelta
from sqlalchemy import select
from db import SessionLocal
from models import Company, Subscription
from config import SUBSCRIPTION_DAYS

TRIAL_DAYS = 3  # количество дней пробного периода

async def get_subscription(user_id: int) -> Subscription | None:
    async with SessionLocal() as session:
        result = await session.execute(
            select(Subscription).where(Subscription.user_id == user_id)
        )
        return result.scalar_one_or_none()


async def has_active_subscription(user_id: int) -> bool:
    async with SessionLocal() as session:
        result = await session.execute(
            select(Subscription).where(
                Subscription.user_id == user_id,
                Subscription.expires_at > datetime.utcnow()
            )
        )
        return result.scalar_one_or_none() is not None


async def get_user_tariff(user_id: int) -> str | None:
    sub = await get_subscription(user_id)
    if not sub or sub.expires_at <= datetime.utcnow():
        return None
    return sub.tariff


async def activate_subscription(user_id: int, tariff: str, days: int = SUBSCRIPTION_DAYS):    
    print("USER ID:", user_id)
    
    # async with SessionLocal() as session:
    #     result = await session.execute(
    #         select(Company).where(Company.owner_tg_id == user_id)
    #     )
    #     company = result.scalar_one_or_none()
        
    #     if not company:
    #         print(f"Company not found for user_id: {user_id}")
    #         return
        
    #     result = await session.execute(
    #         select(Subscription).where(Subscription.user_id == user_id)
    #     )
    #     sub = result.scalar_one_or_none()
        
    #     expires_at = datetime.utcnow() + timedelta(days=days)
        
    #     if sub:
    #         sub.tariff = tariff
    #         sub.expires_at = expires_at
    #         sub.company_id = company.id
    #         sub.notified = False  # Сброс флага уведомления при продлении
    #     else:
    #         sub = Subscription(
    #             user_id=user_id,
    #             company_id=company.id,
    #             tariff=tariff, 
    #             expires_at=expires_at
    #         )
    #         session.add(sub)
        
    #     await session.commit()
    
    async with SessionLocal() as session:

        # 1️⃣ Ищем компанию владельца
        result = await session.execute(
            select(Company).where(Company.owner_tg_id == user_id)
        )
        company = result.scalar_one_or_none()

        print("FOUND COMPANY:", company)
        
        if not company:
            raise Exception("Company ID not found")

        # 2️⃣ Ищем подписку компании
        result = await session.execute(
            select(Subscription).where(
                Subscription.company_id == company.id
            )
        )
        subscription = result.scalar_one_or_none()

        now = datetime.utcnow()
        new_expiry = now + timedelta(days=days)

        if subscription:
            if subscription.expires_at > now:
                subscription.expires_at += timedelta(days=days)
            else:
                subscription.expires_at = new_expiry

            subscription.tariff = tariff

        else:
            subscription = Subscription(
                user_id=user_id,
                company_id=company.id,
                tariff=tariff,
                expires_at=new_expiry
            )
            session.add(subscription)

        await session.commit()

        return subscription
    
    await print(f"Activated subscription for user_id: {user_id}, tariff: {tariff}, expires_at: {expires_at}")
        
        
def activate_company_trial(company):
    company.trial_expires_at = datetime.utcnow() + timedelta(days=TRIAL_DAYS)
    
def company_has_access(company):
    return company.trial_expires_at and company.trial_expires_at > datetime.utcnow()