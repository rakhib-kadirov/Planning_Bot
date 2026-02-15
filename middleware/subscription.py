from aiogram import BaseMiddleware
from aiogram.types import Message, CallbackQuery
from services.subscription import get_user_tariff
from handlers.menu import open_payment
from services.subscription import has_active_subscription

ALLOWED_TARIFFS = ["Base", "Standard", "Business"]

ALLOWED_COMMANDS = {
    "/start",
    "/menu",
    "/admin",
    "/subs",
    "/user",
    "/extend",
    "/disable",
}

ALLOWED_CALLBACKS = {
    "menu",
    "menu_payment",
    "menu_help",
    "menu_contacts",
    "menu_back",
    # "start_form",
    "tariff_basic",
    "tariff_standard",
    "tariff_business",
}


class SubscriptionMiddleware(BaseMiddleware):
    async def __call__(self, handler, event, data):
        user_id = None
        text = None
        callback = None

        if isinstance(event, Message):
            user_id = event.from_user.id

            # ✅ ВСЕГДА пропускаем successful_payment
            if event.successful_payment:
                return await handler(event, data)

            text = event.text or ""

            if text.startswith(tuple(ALLOWED_COMMANDS)):
                return await handler(event, data)

        # Разрешённые команды без подписки
        if isinstance(event, CallbackQuery):
            user_id = event.from_user.id
            callback = event.data

            # разрешаем меню и оплату
            if callback in ALLOWED_CALLBACKS:
                return await handler(event, data)

        if not user_id:
            return await handler(event, data)

        active = await has_active_subscription(user_id)
        if not active:
            if isinstance(event, Message):
                await event.answer(
                    "⛔ The subscription is inactive or has expired.\n\n"
                    "Available rates:\n"
                    "• Basic - basic access\n"
                    "• Standard - Advanced\n"
                    "• Business - is complete\n\n"
                    "Go to Menu → Payment."
                )
            elif isinstance(event, CallbackQuery):
                await event.answer("⛔ No active subscription", show_alert=True)
            return

        return await handler(event, data)


# class SubscriptionMiddleware(BaseMiddleware):
#     async def __call__(self, handler, event, data):

#         if isinstance(event, (Message, CallbackQuery)):
#             user_id = event.from_user
#             if not user_id:
#                 return await handler(event, data)  # Если нет user_id, пропускаем проверку

#             if isinstance(event, Message):
#                 if event.text and event.text.startswith("/start"):
#                     return await handler(event, data)  # Пропускаем проверку для команды /start

#             active = await has_active_subscription(user_id.id)
#             if not active:
#                 if isinstance(event, Message):
#                     await event.answer(
#                         "❌ У вас нет активной подписки.\n\n"
#                         "Пожалуйста, оформите подписку, чтобы продолжить.\n\n"
#                         "Оформите подписку в меню «Оплата».",
#                         reply_markup=open_payment()
#                     )
#                 elif isinstance(event, CallbackQuery):
#                     await event.answer(
#                         "❌ Подписка не активна",
#                         show_alert=True
#                     )
#                 return  # Прекращаем обработку, если подписка не активна

#             # if not await has_active_subscription(user_id):
#             #     await event.answer("❌ Подписка не активна")
#             #     return

#         return await handler(event, data)
