from app.utility.response_utility import PaginationResponseSchema
from app.orders.schema.orders_schema import (
    OrderSummerySchema, GetOrderItemsSchema, GetOrderIdResponseSchema, GetOrderHistoryResponseSchema,
    OrderBaseSchema, GetOrderStatusResponseSchema, GetCanteenOrderDetailResponseSchema, ItemsSchema, 
    CustomerSchema, GetCanteenSummerySchema
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
    response_data = (GetOrderStatusResponseSchema
                     .model_validate(data, from_attributes=True)
                     .model_dump()
                     )
    return response_data


def get_active_orders_transformer(data):
    response_data = (OrderBaseSchema
                     .model_validate(order, from_attributes=True)
                     .model_dump()
                     for order in data
                     )
    return response_data 


def get_canteen_orders_details_transformer(data):
    items = (ItemsSchema.model_validate(item, from_attributes=True).model_dump() 
             for item in data)
    customer = (CustomerSchema.model_validate(data[0], from_attributes=True).model_dump())
    summery = (GetCanteenSummerySchema.model_validate(data[0], from_attributes=True).model_dump())
    data = {**summery, "items":items, "customer":customer}
    response_data =(GetCanteenOrderDetailResponseSchema
                    .model_validate(data, from_attributes=True)
                    .model_dump()
                    )
    return response_data
