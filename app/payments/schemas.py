from typing import List

from pydantic import BaseModel


class PaymentReturn(BaseModel):
    transaction_id: str
    amount: float

    class Config:
        orm_mode = True


class PaymentsReturn(BaseModel):
    payments: List[PaymentReturn]

    class Config:
        orm_mode = True
