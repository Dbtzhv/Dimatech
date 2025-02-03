from fastapi import APIRouter, Depends

from app.accounts.dao import AccountDAO
from app.accounts.schemas import AccountsReturn
from app.users.dependencies import get_current_user
from app.models import User

router = APIRouter(
    prefix='/accounts',
    tags=['Accounts'],
)


@router.get('/my', response_model=AccountsReturn)
async def read_users_accounts(current_user: User = Depends(get_current_user)):
    accounts = await AccountDAO.find_accounts_by_user_id(current_user.id)
    return {"accounts": accounts}
