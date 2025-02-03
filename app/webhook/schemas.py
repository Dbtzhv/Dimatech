from pydantic import BaseModel

class WebhookRequest(BaseModel):
    transaction_id: str
    account_id: int
    user_id: int
    amount: float
    signature: str
    