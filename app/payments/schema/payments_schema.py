from pydantic import BaseModel

class CreatePaymentRequestSchema(BaseModel):
    order_id : int
    