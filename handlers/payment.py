from aiogram import Router, F
from aiogram.types import Message, CallbackQuery, LabeledPrice, PreCheckoutQuery
from sqlalchemy import select
from db import SessionLocal
from models import Company, Subscription
from services.subscription import activate_subscription
from config import PROVIDER_TOKEN_sg, PROVIDER_TOKEN_pm
from datetime import datetime, timedelta

router = Router()

# @router.message(lambda m: m.text == "Оплатить")
async def pay(msg: Message, tariff_id: int):
    prices = [LabeledPrice(label="30-day subscription", amount=tariff_id)]  # amount in cents
    
    tariff_name = (
        "Base" if tariff_id == 999 
        else "Standard" if tariff_id == 1999 
        else "Business" if tariff_id == 2999 
        else "Base"
    )

    await msg.bot.send_invoice(
        chat_id=msg.chat.id,
        title="Subscribe to PlanningChat",
        description=f"""Pay for a 30-day subscription to use PlanningChat.
                        You have chosen a tariff {tariff_name}""",
        payload=f"sub:{tariff_name}",
        provider_token=PROVIDER_TOKEN_sg,  # Using Smart Glocal Test token
        # provider_token=PROVIDER_TOKEN_pm,  # Using PayMaster Test token
        currency="USD",
        prices=prices,
        start_parameter="subscription-start",
    )
    
    # await activate_subscription(msg.from_user.id)
    # await msg.answer("✅ Подписка активирована (тест)")
    
@router.pre_checkout_query()
async def pre_checkout(pre: PreCheckoutQuery):
    await pre.answer(ok=True)

# @router.message(lambda m: m.successful_payment)
# async def successful_payment(msg: Message):
#     await activate_subscription(msg.from_user.id)
#     await msg.answer("✅ Подписка активирована на 30 дней. Спасибо за оплату!")


@router.message(F.successful_payment)
async def on_successful_payment(call: Message):
    payload = call.successful_payment.invoice_payload
    tariff = payload.split(":")[1]
    
    await activate_subscription(user_id=call.from_user.id, tariff=tariff, days=30)
    # async with SessionLocal() as session:
    #     # 1️⃣ Ищем компанию владельца
    #     result = await session.execute(
    #         select(Company).where(Company.owner_tg_id == call.from_user.id)
    #     )
    #     company = result.scalar_one_or_none()

    #     if not company:
    #         await call.answer("❌ У Вас нет компании. Сначала создайте её через /start.")
    #         return

    #     # 2️⃣ Проверяем существующую подписку
    #     result = await session.execute(
    #         select(Subscription).where(
    #             Subscription.company_id == company.id
    #         )
    #     )
    #     subscription = result.scalar_one_or_none()

    #     now = datetime.utcnow()
    #     new_expiry = now + timedelta(days=30)

    #     if subscription:
    #         # если подписка ещё активна — продлеваем от текущей даты окончания
    #         if subscription.expires_at > now:
    #             subscription.expires_at += timedelta(days=30)
    #         else:
    #             subscription.expires_at = new_expiry

    #         subscription.tariff = tariff

    #     else:
    #         # создаём новую подписку
    #         subscription = Subscription(
    #             user_id=call.from_user.id,
    #             company_id=company.id,
    #             tariff=tariff,
    #             expires_at=new_expiry,
    #         )
    #         session.add(subscription)

    #     await session.commit()

    # await call.answer(
    #     f"✅ Подписка '{tariff}' активирована до {subscription.expires_at.date()}."
    # )
    
    await call.answer("✅ Your subscription is activated for 30 days. Thank you for your payment!")