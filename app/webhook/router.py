import hashlib
import hmac
from decimal import Decimal, InvalidOperation

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy import select
from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession
from starlette import status

from app.database import get_async_session
from app.models import Payment, Account
from app.webhook.schemas import WebhookRequest
from app.config import settings

router = APIRouter(
    prefix='/webhook',
    tags=['Webhook'],
)




@router.post("/payment")
async def process_payment(
        webhook_data: WebhookRequest,
        db: AsyncSession = Depends(get_async_session)
):
    try:
        amount = Decimal(str(webhook_data.amount)).quantize(Decimal('0.00'))
    except InvalidOperation:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Invalid amount format"
        )

    if amount <= Decimal('0'):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Amount must be positive"
        )

    # Проверка подписи
    secret_key = settings.SECRET_KEY
    data_str = (
        f"{webhook_data.account_id}"
        f"{amount}"
        f"{webhook_data.transaction_id}"
        f"{webhook_data.user_id}"
        f"{secret_key}"
    )
    expected_signature = hashlib.sha256(data_str.encode()).hexdigest()
    print(expected_signature)
    if not hmac.compare_digest(expected_signature, webhook_data.signature):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Invalid signature"
        )

    # Проверка уникальности транзакции
    existing_payment = await db.execute(
        select(Payment).where(Payment.transaction_id == webhook_data.transaction_id)
    )
    if existing_payment.scalar_one_or_none():
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Transaction ID already exists"
        )

    # Проверка существования счета
    account = await db.execute(
        select(Account)
        .where(Account.id == webhook_data.account_id)
    )
    account = account.scalar_one_or_none()

    if not account:
        # Создание нового счета
        account = Account(
            id=webhook_data.account_id,
            user_id=webhook_data.user_id,
            balance=Decimal('0.00')
        )
        db.add(account)
        try:
            await db.commit()
            await db.refresh(account)
        except IntegrityError:
            await db.rollback()
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Account ID conflict"
            )

    # Создание платежа
    payment = Payment(
        account_id=webhook_data.account_id,
        transaction_id=webhook_data.transaction_id,
        amount=webhook_data.amount
    )
    db.add(payment)

    # Обновление баланса
    account.balance += Decimal(webhook_data.amount)
    await db.commit()
    await db.refresh(account)

    return {"status": "success", "message": "Payment processed"}




