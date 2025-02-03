from typing import List

from pydantic import BaseModel, EmailStr


class AccountReturn(BaseModel):
    id: int
    balance: float

    class Config:
        orm_mode = True


class AccountsReturn(BaseModel):
    accounts: List[AccountReturn]