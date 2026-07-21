from app.utility.response_utility import PaginationResponseSchema
from app.orders.schema.orders_schema import (
    OrderSummerySchema, GetOrderItemsSchema, GetOrderIdResponseSchema, GetOrderHistoryResponseSchema,
    OrderBaseSchema, GetOrderStatusTransformer
)

def get_id_order_transformer(summery, items):
    summery = (OrderSummerySchema
               .model_validate(summery, from_attributes=True)
               .model_dump()
               )
    items = (GetOrderItemsSchema
             .model_validate(item, from_attributes=True)
             .model_dump()
             for item in items
             )
    data = {**summery, "items":items}
    response_data = (GetOrderIdResponseSchema
                     .model_validate(data, from_attributes=True)
                     .model_dump()
                     )
    return response_data


def get_orders_history_transformer(query, pagination):
    pagination = (PaginationResponseSchema
                  .model_validate(pagination, from_attributes= True)
                  .model_dump()
    )
    orders = [OrderBaseSchema
              .model_validate(item, from_attributes=True)
              .model_dump()
              for item in query
              ]
    data = {**pagination, "orders": orders}
    response_data = (GetOrderHistoryResponseSchema
                     .model_validate(data, from_attributes=True)
                     .model_dump()
    )
    return response_data


def get_order_status_transformer(data):
    response_data = (GetOrderStatusTransformer
                     .model_validate(data, from_attributes=True)
                     .model_dump()
                     )
    return response_data