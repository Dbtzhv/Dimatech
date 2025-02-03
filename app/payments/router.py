from fastapi import APIRouter, Depends

from app.payments.schemas import PaymentsReturn

from app.payments.dao import PaymentDAO
from app.users.dependencies import get_current_user
from app.models import User

router = APIRouter(
    prefix='/payments',
    tags=['Payments'],
)


@router.get('/my', response_model=PaymentsReturn)
async def read_users_payments(current_user: User = Depends(get_current_user)):
    accounts = await PaymentDAO.find_payments_by_user_id(current_user.id)
    return {"payments": accounts}