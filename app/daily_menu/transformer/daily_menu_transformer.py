from app.daily_menu.schema.daily_menu_schema import DailyMenuResponseSchema

def get_daily_menu_transformer(data):
    response_data = (DailyMenuResponseSchema
                     .model_validate(item, from_attributes=True)
                     .model_dump()for item in data)
    return response_data