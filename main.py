import asyncio
from datetime import datetime
from aiogram import Bot, Dispatcher
from aiogram.fsm.storage.memory import MemoryStorage
from db import engine, Base, SessionLocal
from sqlalchemy import select
from middleware.subscription import SubscriptionMiddleware
from models import Client, Company, Subscription
from config import BOT_TOKEN
from handlers import start, lead, form, admin, payment, message, menu, statistics
from tasks.subscription_notify import subscription_notifier

async def trial_watcher(bot: Bot):
    while True:
        async with SessionLocal() as session:
            result = await session.execute(
                select(Subscription).where(
                    Subscription.tariff == "trial"
                )
            )
            trials = result.scalars().all()

            now = datetime.utcnow()

            for trial in trials:
                remaining = trial.expires_at - now

                if remaining.total_seconds() == 259200:
                    await bot.send_message(
                        trial.user_id,
                        "⏳ Ваша подписка скоро истекает.\n\n"
                        f"Тариф: {trial.tariff}\n"
                        f"Дата окончания: {trial.expires_at.date()}\n\n"
                        "Продлите подписку, чтобы сохранить доступ."
                    )

        await asyncio.sleep(60)

async def start_bot(bot_token: str):
    bot = Bot(bot_token)
    dp = Dispatcher(storage=MemoryStorage())
    
    dp.include_router(admin.router)
    dp.include_router(start.router)
    dp.include_router(statistics.router)
    dp.include_router(menu.router)
    dp.include_router(lead.router)
    dp.include_router(form.router)
    dp.include_router(payment.router)
    # dp.include_router(message.router)
    
    # asyncio.create_task(subscription_notifier(bot))
    asyncio.create_task(trial_watcher(bot))
    
    await dp.start_polling(bot)

async def main():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
        
    bots = []
    
    # Start favorite bots
    bots.append(start_bot(BOT_TOKEN))
    
    # Start client bots
    async with SessionLocal() as session:
        result = await session.execute(select(Client))
        clients = result.scalars().all()
        
        for client in clients:
            if client.bot_token:
                bots.append(start_bot(client.bot_token))
        
    await asyncio.gather(*bots)

if __name__ == "__main__":
    asyncio.run(main())