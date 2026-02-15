from aiogram import BaseMiddleware
from aiogram.types import Message
from config import ADMIN_IDS


class AdminMiddleware(BaseMiddleware):
    async def __call__(self, handler, event, data):
        if isinstance(event, Message):
            if event.from_user.id in ADMIN_IDS:
                return await handler(event, data)
            else:
                return
