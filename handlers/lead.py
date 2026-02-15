from aiogram import Router, Bot
from aiogram.types import Message
from aiogram.fsm.context import FSMContext

from states.lead import LeadState
from models import Lead
from db import SessionLocal

from services.crm import save_lead, get_company_telegram_id

import phonenumbers
import re

router = Router()

def is_valid_phone(phone: str) -> bool:
    # digits = re.sub(r"\D", "", phone)
    # return len(digits) >= 8
    try:
        parsed_phone = phonenumbers.parse(phone, None)
        return phonenumbers.is_valid_number(parsed_phone)
    except phonenumbers.NumberParseException:
        return False

@router.message(LeadState.name)
async def lead_name(msg: Message, state: FSMContext):
    pattern = r'^[^\d\W_]+(?: [^\d\W_]+)*$'
    if not re.match(pattern, msg.text):
        # await msg.answer("❌ Имя не должно содержать цифры или специальные символы. Введите имя ещё раз:")
        await msg.answer("❌ The name must not contain numbers or special characters. Please re-enter the name:")
        return

    await state.update_data(name=msg.text)
    await state.set_state(LeadState.phone)
    # await msg.answer("Введите номер телефона:")
    await msg.answer("Enter your phone number:")
    # await LeadState.phone.set()
    
@router.message(LeadState.phone)
async def lead_phone(msg: Message, state: FSMContext):
    if not is_valid_phone(msg.text):
        # await msg.answer("❌ Неверный номер. Введите телефон ещё раз")
        await msg.answer("❌ Invalid number. Please enter your phone number again.")
        return
    
    await state.update_data(phone=msg.text)
    await state.set_state(LeadState.comment)
    # await msg.answer("Введите комментарий (или напишите 'нет'):")
    await msg.answer("Enter a comment (or write 'none'):")
    # await LeadState.comment.set()
    
@router.message(LeadState.comment)
async def lead_comment(msg: Message, state: FSMContext, bot: Bot):
    data = await state.get_data()
    company_id = data.get("company_id")
    
    async with SessionLocal() as session:
        if not company_id:
            await msg.answer("❌ Error: Company ID not found.")
            return
        
        lead = Lead(
            company_id=company_id,
            user_id=msg.from_user.id,
            name=data["name"],
            phone=data["phone"],
            comment=msg.text if msg.text.lower() != "нет" else ""
        )
        
        company_telegram_id = await get_company_telegram_id(int(company_id))
        
        if company_telegram_id:
            await bot.send_message(
                chat_id=company_telegram_id,
                text=(
                    f"New application from {data['name']}:\n"
                    f"Phone: {data['phone']}\n"
                    f"Comment: {lead.comment}"
                )
            )
            session.add(lead)
            await session.commit()
            await msg.answer("✅ Your application has been sent to the company.")
        else:
            await msg.answer("❌ Failed to submit application, company not found.")
        
        
    # await msg.answer("✅ Спасибо! Ваша заявка принята.")
    await state.clear()
    
    
# @router.message()
# async def get_lead(message: Message, state: FSMContext, bot: Bot):
#     data = await state.get_data()
#     company_id = data.get("company_id")
    
#     if not company_id:
#         await message.answer("❌ Error: Company ID not found.")
#         return
    
#     # Сохраняем в базу данных
#     await save_lead(
#         company_id=company_id,
#         user_id=message.from_user.id,
#         # comment=message.text
#         data=data
#     )
    
#     # Получаем Telegram ID компании для отправки уведомления
#     company_tg_id = await get_company_telegram_id(int(company_id))
    
#     # Отправляем уведомление компании о новой заявке
#     if company_tg_id:
#         await bot.send_message(
#             chat_id=company_tg_id,
#             text=(
#                 f"New application from {message.from_user.full_name}:\n"
#                 f"{message.text}"
#             )
#         )
#         await message.answer("✅ Your application has been sent to the company.")
#     else:
#         await message.answer("❌ Failed to submit application, company not found.")
    