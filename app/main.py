import uvicorn
from fastapi import FastAPI

from app.users.router import router as users_router
from app.accounts.router import router as accounts_router
from app.payments.router import router as payments_router
from app.webhook.router import router as webhook_router

app = FastAPI()

app.include_router(users_router)
app.include_router(accounts_router)
app.include_router(payments_router)
app.include_router(webhook_router)


if __name__ == "__main__":
    uvicorn.run("main:app", host="127.0.0.1", port=8000, reload=True)