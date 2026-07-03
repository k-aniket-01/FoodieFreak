from app.user.transformer.user_transformer import get_user_profile_transformer

def get_user_profile_service(data):
    data = get_user_profile_transformer(data)
    return data