from app.orders.schema.orders_schema import OrderSummerySchema, GetOrderItemsSchema, GetOrderIdResponseSchema

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