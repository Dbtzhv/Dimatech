from typing import Annotated
from sqlalchemy import INTEGER, String, ForeignKey, DECIMAL
from sqlalchemy.orm import Mapped, mapped_column, relationship
from app.database import Base

int_pk = Annotated[int, mapped_column(INTEGER, primary_key=True)]
str_not_null = Annotated[str, mapped_column(String, nullable=False)]
decimal_not_null = Annotated[float, mapped_column(DECIMAL(10, 2), nullable=False)]

class User(Base):
    __tablename__ = "users"

    id: Mapped[int_pk]
    email: Mapped[str_not_null]
    full_name: Mapped[str_not_null]
    hashed_password: Mapped[str_not_null]
    role: Mapped[str_not_null]

    accounts: Mapped[list["Account"]] = relationship("Account", back_populates="user")


class Account(Base):
    __tablename__ = "accounts"

    id: Mapped[int_pk]
    user_id: Mapped[Annotated[int, mapped_column(ForeignKey("users.id"), nullable=False)]]
    balance: Mapped[decimal_not_null]

    user: Mapped["User"] = relationship(back_populates="accounts")
    payments: Mapped[list["Payment"]] = relationship(back_populates="account")


class Payment(Base):
    __tablename__ = "payments"

    id: Mapped[int_pk]
    account_id: Mapped[Annotated[int, mapped_column(ForeignKey("accounts.id"), nullable=False)]]
    transaction_id: Mapped[Annotated[str, mapped_column(String, unique=True, nullable=False)]]
    amount: Mapped[decimal_not_null]

    account: Mapped["Account"] = relationship(back_populates="payments")


