import asyncio
from aiogram import Bot, Dispatcher
from aiogram.fsm.storage.memory import MemoryStorage
from db import engine, Base, SessionLocal
from sqlalchemy import select
from middleware.subscription import SubscriptionMiddleware
from models import Client
from config import BOT_TOKEN
from handlers import start, lead, form, admin, payment, message, menu, statistics
from tasks.subscription_notify import subscription_notifier

async def start_bot(bot_token: str):
    bot = Bot(bot_token)
    dp = Dispatcher(storage=MemoryStorage())
    # dp.message.middleware(SubscriptionMiddleware())
    # dp.callback_query.middleware(SubscriptionMiddleware())
    
    dp.include_router(admin.router)
    dp.include_router(start.router)
    dp.include_router(statistics.router)
    dp.include_router(menu.router)
    dp.include_router(lead.router)
    dp.include_router(form.router)
    dp.include_router(payment.router)
    # dp.include_router(message.router)
    
    
    asyncio.create_task(subscription_notifier(bot))
    
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