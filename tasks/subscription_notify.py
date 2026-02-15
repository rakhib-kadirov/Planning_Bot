import asyncio
from aiogram import Bot
from services.subscription_checker import (
    get_expiring_subscriptions,
    mark_as_notified
)

async def subscription_notifier(bot: Bot):
    while True:
        subs = await get_expiring_subscriptions(days_before=3)
        
        for sub in subs:
            try:
                await bot.send_message(
                    sub.user_id,
                    (
                        "⏳ Ваша подписка скоро истекает.\n\n"
                        f"Тариф: {sub.tariff}\n"
                        f"Дата окончания: {sub.expires_at.date()}\n\n"
                        "Продлите подписку, чтобы сохранить доступ."
                    )    
                )
                await mark_as_notified(sub)
            except Exception:
                pass # Игнорируем ошибки отправки (например, если пользователь удалён или заблокировал бота)
            
        await asyncio.sleep(24 * 3600)  # Проверять раз в сутки