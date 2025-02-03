from typing import List

from pydantic import BaseModel, EmailStr

from app.accounts.schemas import AccountReturn


class SUserRegister(BaseModel):
    email: EmailStr
    full_name: str
    password: str

    class Config:
        from_attributes = True


class SUserAuth(BaseModel):
    email: EmailStr
    password: str

    class Config:
        from_attributes = True


class UserReturn(BaseModel):
    email: EmailStr
    full_name: str

    class Config:
        from_attributes = True


class UserCreate(BaseModel):
    email: str
    full_name: str
    hashed_password: str
    role: str

    class Config:
        from_attributes = True


class UserUpdate(BaseModel):
    email: str = None
    full_name: str = None
    role: str = None

    class Config:
        from_attributes = True


class UserAccounts(BaseModel):
    id: int
    email: str
    full_name: str
    accounts: List[AccountReturn]

    class Config:
        from_attributes = True


class UsersAccounts(BaseModel):
    users_accounts: List[UserAccounts]

    class Config:
        from_attributes = True
