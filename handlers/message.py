# from aiogram import Router
# from aiogram.types import Message, ReplyKeyboardMarkup, KeyboardButton
# from handlers.menu import open_payment
# from services.ai import ai_reply
# from services.subscription import has_active_subscription

# router = Router()

# @router.message()
# async def ai_fallback(msg: Message, tariff: str):
#     if tariff == "Базовый":
#         reply = await ai_reply(msg.text, max_tokens=500)
#     elif tariff == "Стандартный":
#         reply = await ai_reply(msg.text, max_tokens=1500)
#     elif tariff == "Бизнес":
#         reply = await ai_reply(msg.text, max_tokens=5000)
    
#     # проверка на пустой ответ
#     if not reply or not reply.strip():  # проверяем, что строка не пустая и не только пробелы
#         await msg.answer("⚠️ Ошибка генерации ответа.")
#         return
    
#     await msg.answer(reply)
