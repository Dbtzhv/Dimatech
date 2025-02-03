from fastapi import APIRouter, status, Response, Depends, HTTPException

from app.exceptions import UserAlreadyExistsException, IncorrectEmailOrPasswordException
from app.users.auth import get_password_hash, authenticate_user, create_access_token
from app.users.dao import UserDAO
from app.users.dependencies import get_current_user, check_admin
from app.models import User
from app.users.schemas import SUserAuth, UserReturn, SUserRegister, UserCreate, UserUpdate, UsersAccounts

router = APIRouter(
    prefix='/auth',
    tags=['Auth & Users'],
)


@router.post('/register')
async def register_user(user_data: SUserRegister):
    existing_user = await UserDAO.find_one_or_none(email=user_data.email)
    if existing_user:
        raise UserAlreadyExistsException
    hashed_password = get_password_hash(user_data.password)
    await UserDAO.add(
        email=user_data.email,
        full_name=user_data.full_name,
        hashed_password=hashed_password,
        role='user',
    )


@router.post('/login')
async def login_user(response: Response, user_data: SUserAuth):
    user = await authenticate_user(user_data.email, user_data.password)
    if not user:
        raise IncorrectEmailOrPasswordException
    access_token = create_access_token({'sub': str(user.id)})
    response.set_cookie('access_token', access_token, httponly=True)
    return access_token


@router.post('/logout')
async def logout_user():
    response = Response(status_code=status.HTTP_200_OK)
    response.delete_cookie('access_token')
    return response


@router.get('/me', response_model=UserReturn)
async def read_users_me(current_user: User = Depends(get_current_user)):
    return current_user


@router.post("/users")
async def create_user(user_data: UserCreate, current_user: User = Depends(check_admin)):
    hashed_password = get_password_hash(user_data.hashed_password)
    user_data.hashed_password = hashed_password
    await UserDAO.add(**user_data.dict())
    return 'User has been created'


@router.patch("/users/{user_id}")
async def update_user(user_id: int, user_data: UserUpdate, current_user: User = Depends(check_admin)):
    user = await UserDAO.find_by_id(user_id)

    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")

    result = await UserDAO.update_by_id(model_id=user_id, **user_data.dict())
    return result


@router.delete("/users/{user_id}")
async def delete_user(user_id: int, current_user: User = Depends(check_admin)):
    user = await UserDAO.find_by_id(user_id)

    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")

    result = await UserDAO.delete_by_id(model_id=user_id)
    return result


@router.get('/users_and_accounts', response_model=UsersAccounts)
async def get_users_and_accounts(current_user: User = Depends(get_current_user)):
    if current_user.role != 'admin':
        raise HTTPException(status_code=403, detail="You do not have access to this resource")

    users = await UserDAO.find_users_with_accounts()

    return {"users_accounts": users}