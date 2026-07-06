from app.categories.schema.categories_schema import GetCategoriesResponseSchema

def get_categories_transformer(data):
    response = (GetCategoriesResponseSchema
                .model_validate(items, from_attributes=True)
                .model_dump()for items in data)
    return response

def get_category_id_transformer(data):
    response = (GetCategoriesResponseSchema
                .model_validate(data, from_attributes=True)
                .model_dump())
    return response