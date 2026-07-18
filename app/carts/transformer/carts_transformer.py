from app.carts.schema.carts_schema import GetCartResponseSchema, SummerySchema, CartItemsSchema

def get_cart_items_transformer(summery, items):
    summery = (SummerySchema
               .model_validate(summery, from_attributes=True)
               .model_dump()
               )
    items = [CartItemsSchema
             .model_validate(item, from_attributes=True)
             .model_dump()
             for item in items
             ]
    data = {**summery, "items": items}
    response_data = (GetCartResponseSchema
                     .model_validate(data , from_attributes=True)
                     .model_dump()
                    )
    return response_data