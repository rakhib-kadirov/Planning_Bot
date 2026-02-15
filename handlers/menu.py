from aiogram import types
from aiogram.types import Message, CallbackQuery, InlineKeyboardButton, InlineKeyboardMarkup
from aiogram.utils.keyboard import InlineKeyboardBuilder
from aiogram.filters import Command
from aiogram import Router
from aiogram.fsm.context import FSMContext
from sqlalchemy import select

from db import SessionLocal
from handlers.payment import pay
from models import Company

router = Router()

print("MENU ROUTER LOADED")

def main_menu():
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [InlineKeyboardButton(text="💳 Payment", callback_data="menu_payment")],
            [InlineKeyboardButton(text="💳 Statistics", callback_data="menu_statistics")],
            [InlineKeyboardButton(text="❓ Help", callback_data="menu_help")],
            [InlineKeyboardButton(text="Contacts", callback_data="menu_contacts")],
        ],
        resize_keyboard=True
    )

def payment_menu():
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [InlineKeyboardButton(text="Basic Tariff - 9,99$", callback_data="tariff_basic")],
            [InlineKeyboardButton(text="Standard Tariff - 19,99$", callback_data="tariff_standard")],
            [InlineKeyboardButton(text="Business Tariff - 29,99$", callback_data="tariff_business")],
            [InlineKeyboardButton(text="⬅️ Back", callback_data="menu_back")],
        ],
        resize_keyboard=True
    )
    
@router.message(Command("menu"))
async def menu_cmd(msg: Message):
    async with SessionLocal() as session:
        result = await session.execute(
            select(Company).where(Company.owner_tg_id == msg.from_user.id)
        )
        company = result.scalar_one_or_none()
        
        if not company:
            return # Если пользователь не является владельцем компании, не показываем меню
        
        await msg.answer("Main menu:", reply_markup=main_menu())

@router.callback_query(lambda c: c.data == "menu_payment")
async def open_payment(call: CallbackQuery):
    await call.message.edit_text(
        "Select a tariff plan:",
        reply_markup=payment_menu()
    )
    await call.answer()

@router.callback_query(lambda c: c.data == "menu_back")
async def back_to_menu(call: CallbackQuery):
    await call.message.edit_text(
        "Main menu:",
        reply_markup=main_menu()
    )
    await call.answer()

# Click handler
@router.callback_query(lambda c: c.data.startswith("tariff_"))
async def callbacks(call: types.CallbackQuery):
    data = call.data
    
    money_tariff_basic = 999
    money_tariff_standard = 1999
    money_tariff_business = 2999
    
    if call.data == "menu_payment":
        await call.message.edit_text("Select a tariff plan:", reply_markup=payment_menu())
    elif data.startswith("tariff_"):
        if data == "tariff_basic":
            # text = f"Вы выбрали тариф Базовый - {money_tariff_basic / 100:.2f}$"
            await pay(call.message, money_tariff_basic)
        elif data == "tariff_standard":
            # text = f"Вы выбрали тариф Стандартный - {money_tariff_standard / 100:.2f}$"
            await pay(call.message, money_tariff_standard)
        elif data == "tariff_business":
            # text = f"Вы выбрали тариф Бизнес - {money_tariff_business / 100:.2f}$"
            await pay(call.message, money_tariff_business)
        # await call.message.answer(text)
    elif call.data == "back_to_main":
        await call.message.edit_text("Main menu:", reply_markup=main_menu())
    
    # await call.message.answer()
    # await call.answer()
    
@router.callback_query(lambda c: c.data == "menu_help")
async def help_menu(call: CallbackQuery):
    await call.message.answer("Write to the operator or select a tariff.")
    await call.answer()

@router.callback_query(lambda c: c.data == "menu_contacts")
async def help_menu(call: CallbackQuery):
    await call.message.answer("Contacts:\nEmail: rakhibkqadirov@gmail.com")
    await call.answer()