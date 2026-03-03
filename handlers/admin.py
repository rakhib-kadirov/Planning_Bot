from aiogram import Router
from aiogram.filters import Command
from aiogram.types import Message
from sqlalchemy import select
from db import SessionLocal
from models import Company, Subscription
from datetime import datetime, timedelta
from services.admin import (
    get_active_subscriptions,
    get_user_subscription,
    extend_subscription,
    disable_subscription,
)
from aiogram.fsm.context import FSMContext
from middleware.admin import AdminMiddleware

router = Router()
router.message.middleware(AdminMiddleware())


async def get_owner_company(user_id: int):
    async with SessionLocal() as session:
        company = await session.execute(
            select(Company).where(Company.owner_tg_id == user_id)
        )
        return company.scalars().all()


@router.message(Command("admin"))
async def admin_menu(msg: Message):
    await msg.answer(
        "👑 Админ-панель:\n\n"
        "/subs - Показать активные подписки\n"
        "/user <id> - Подписка пользователя\n"
        "/extend <id> <days> - Продлить подписку\n"
        "/disable <id> - Отключить подписку"
    )


@router.message(Command("subs"))
async def list_subs(msg: Message, state: FSMContext):
    async with SessionLocal() as session:
        result = await session.execute(
            select(Company).where(Company.owner_tg_id != msg.from_user.id)
        )
        companies = result.scalars().all()

        # data = await state.get_data()
        # company_id = data.get("company_id")

        if not companies:
            await msg.answer("У Вас нет компании.")
            return

        has_subs = False
        
        for company in companies:
            result_sub = await session.execute(
                select(Subscription)
                .where(Subscription.company_id == company.id)
            )
            subs = result_sub.scalars().all()
            # subs = await get_active_subscriptions(company_id)
            if not subs:
                continue
                # await msg.answer("Нет активных подписок.")
                # return
            has_subs = True

            text = "Активные подписки:\n\n"
            for sub in subs:
                text += (
                    f"Company ID: {sub.company_id}\n"
                    f"ID: {sub.user_id}\n"
                    f"Тариф: {sub.tariff}\n"
                    f"Истекает: {sub.expires_at.date()}\n\n"
                )

        if not has_subs:
            await msg.answer("Нет активных подписок.")
            return
                
        await msg.answer(text)


@router.message(Command("user"))
async def user_sub(msg: Message):
    args = msg.text.split()
    if len(args) != 2:
        await msg.answer("Использование: /user <id>")
        return

    user_id = int(args[1])
    companies = await get_owner_company(msg.from_user.id)
    
    if not companies:
        await msg.answer("У Вас нет компании.")
        return

    async with SessionLocal() as session:
        for company in companies:
            result = await session.execute(
                select(Subscription).where(
                    Subscription.company_id == company.id, Subscription.user_id == user_id
                )
            )
            sub = result.scalars().all()

    if not sub:
        await msg.answer("У пользователя нет подписки.")
        return

    await msg.answer(
        f"ID: {sub.user_id}\n"
        f"Тариф: {sub.tariff}\n"
        f"Истекает: {sub.expires_at.date()}\n"
    )


@router.message(Command("extend"))
async def extend(msg: Message):
    args = msg.text.split()
    if len(args) != 3:
        await msg.answer("Использование: /extend <id> <days>")
        return

    success = await extend_subscription(int(args[1]), int(args[2]))
    if success:
        await msg.answer("Подписка продлена.")
    else:
        await msg.answer("Ошибка: пользователь не найден.")


@router.message(Command("disable"))
async def disable(msg: Message):
    args = msg.text.split()
    if len(args) != 2:
        await msg.answer("Использование: /disable <id>")
        return

    success = await disable_subscription(int(args[1]))
    if success:
        await msg.answer("Подписка отключена.")
    else:
        await msg.answer("Ошибка: пользователь не найден.")
