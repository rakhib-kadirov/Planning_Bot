from aiogram import Router
from aiogram.types import Message, InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.filters import CommandStart,CommandObject
from sqlalchemy import select
from db import SessionLocal
from models import Company
from services.subscription import activate_company_trial
from aiogram.fsm.context import FSMContext
from states.lead import LeadState

router = Router()

# start_kb = InlineKeyboardMarkup(
#     inline_keyboard=[
#         [InlineKeyboardButton(text="Оставить заявку", callback_data="start_form")]
#     ]
# )

# @router.message(CommandStart())
# async def start(msg: Message):
#     await msg.answer(
#         "Привет! Нажмите кнопку, чтобы оставить заявку",
#         reply_markup=start_kb,
#     )


@router.message(CommandStart())
async def start_handler(msg: Message, state: FSMContext, command: CommandObject):
    print("START WORKS")
    args = msg.text.split()
    
    data = await state.get_data()
    
    if data.get("role") == "client":
        await state.set_state(LeadState.name)
        await msg.answer("What is your name?")
        return
    
    async with SessionLocal() as session:
        # Если есть deep link — это клиент
        if command.args and command.args.startswith("company_"):
            company_id = int(command.args.replace("company_", ""))  # получаем 123 из ?start=123
            
            await state.update_data(
                role="client",
                company_id=company_id
            )
            
            await state.set_state(LeadState.name)
            await msg.answer("What is your name?")
            return
    
        # # Иначе — это владелец компании
        # # 1️⃣ Пользователь пришёл по ссылке компании → оставляет заявку
        # if len(args) > 1 and args[1].startswith("company_"):
        #     company_id = int(args[1].replace("company_", ""))
            
        #     await state.update_data(company_id=company_id)
        #     await state.set_state(LeadState.name)
            
        #     await msg.answer("What is your name?")
        #     return
        
        result = await session.execute(
            select(Company).where(Company.owner_tg_id == msg.from_user.id)
        )
        company = result.scalar_one_or_none()
        
        if not company:
            company = Company(
                owner_tg_id=msg.from_user.id,
                # owner_tg_id=msg.from_user.id,
                name=f"Company {msg.from_user.id}"
            )
            activate_company_trial(company)
            session.add(company)
            await session.commit()
            
            await state.update_data(
                role="owner",
                company_id=company.id
            )
            
            await msg.answer(
                "🎁 Your 3-day trial has been activated.\n\n"
                "Here is your link for clients:\n"
                f"https://t.me/PlaningChat_bot?start=company_{company.id}"
            )
        else:
            await msg.answer(
                "Here is your link for clients:\n"
                f"https://t.me/PlaningChat_bot?start=company_{company.id}"
            )


# @router.message(CommandStart(deep_link=True))
# async def start_with_ref(message: Message, command: CommandStart, state: FSMContext):
#     company_id = command.args  # получаем 123 из ?start=123

#     await state.update_data(company_id=company_id)

#     await message.answer("Leave your request:")