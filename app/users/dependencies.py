from datetime import datetime

from fastapi import Request, Depends, HTTPException
from jose import jwt, JWTError
from starlette import status

from app.config import settings
from app.exceptions import IncorrectTokenFormatException, TokenAbscentException, TokenExpiredException, \
    UserIsNotPresentException
from app.models import User
from app.users.dao import UserDAO


async def get_token(request: Request):
    token = request.cookies.get("access_token")
    if not token:
        raise TokenAbscentException
    return token


async def get_current_user(token: str = Depends(get_token)):
    try:
        payload = jwt.decode(token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM])
    except JWTError:
        raise IncorrectTokenFormatException
    expire: str = payload.get("exp")
    if (not expire) or (int(expire) < datetime.utcnow().timestamp()):
        raise TokenExpiredException
    user_id: str = payload.get("sub")
    if not user_id:
        raise UserIsNotPresentException
    user = await UserDAO.find_by_id(int(user_id))
    if not user:
        raise UserIsNotPresentException
    return user


async def check_admin(current_user: User = Depends(get_current_user)):
    if current_user.role != "admin":
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Not enough permissions")
    return current_user
