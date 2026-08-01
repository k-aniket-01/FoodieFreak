from app.payments.schema.payments_schema import PaymentBaseSchema, GetPaymentHistoryResponseSchema
from app.utility.response_utility import PaginationResponseSchema

def get_payment_history_transformer(data, pagination):
    payments = [PaymentBaseSchema
                .model_validate(payment, from_attributes=True)
                .model_dump()
                for payment in data
    ]
    pagin_res = (PaginationResponseSchema
                  .model_validate(pagination, from_attributes=True)
                  .model_dump()
                  )
    data = {"data":payments, "pagination":pagin_res}
    response_data = (GetPaymentHistoryResponseSchema
                     .model_validate(data, from_attributes=True)
                     .model_dump()
                     )
    return response_data

def get_payment_transformer(data):
    response_data = (PaymentBaseSchema
                     .model_validate(data, from_attributes=True)
                     .model_dump()
                     )
    return response_data