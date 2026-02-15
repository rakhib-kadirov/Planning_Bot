from aiogram import Router, F
from aiogram.types import CallbackQuery, Message
from aiogram.fsm.state import StatesGroup, State
from aiogram.fsm.context import FSMContext
from services.crm import save_lead
import re
from handlers import menu
import phonenumbers

router = Router()

def is_valid_phone(phone: str) -> bool:
    # digits = re.sub(r"\D", "", phone)
    # return len(digits) >= 8
    try:
        parsed_phone = phonenumbers.parse(phone, None)
        return phonenumbers.is_valid_number(parsed_phone)
    except phonenumbers.NumberParseException:
        return False

class Form(StatesGroup):
    name = State()
    phone = State()
    comment = State()

@router.callback_query(F.data == "start_form")
async def start_form(cb: CallbackQuery, state: FSMContext):
    await state.set_state(Form.name)
    await cb.message.answer("What is your name?")
    await cb.answer()

@router.message(Form.name)
async def get_name(msg: Message, state: FSMContext):
    await state.update_data(name=msg.text)
    await state.set_state(Form.phone)
    await msg.answer("Enter your phone number")

@router.message(Form.phone)
async def get_phone(msg: Message, state: FSMContext):
    if not is_valid_phone(msg.text):
        await msg.answer("❌ Invalid number. Please enter your phone number again.")
        return
    
    await state.update_data(phone=msg.text)
    await state.set_state(Form.comment)
    await msg.answer("Comment")

@router.message(Form.comment)
async def finish(msg: Message, state: FSMContext):
    await state.update_data(comment=msg.text)
    data = await state.get_data()
    await save_lead(data)
    await state.clear()
    await msg.answer("✅ Application accepted. We will contact you soon.")