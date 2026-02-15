async def send_auto_reply(bot, chat_id):
    await bot.send_message(
        chat_id,
        "Thank you for your request! We will contact you soon."
    )