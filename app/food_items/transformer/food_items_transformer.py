from app.food_items.schema.food_items_schema import GetFoodItemsResponseSchema


def get_food_items_transformer(data):
    response = (GetFoodItemsResponseSchema
                .model_validate(item, from_attributes=True)
                .model_dump()for item in data)
    return response

def get_food_item_id_transformer(data):
    response = (GetFoodItemsResponseSchema
                .model_validate(data, from_attributes=True)
                .model_dump())
    return response