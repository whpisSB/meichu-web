from flask_jwt_extended import get_jwt, get_jwt_identity, create_access_token

def check_permission(target_permission):
    jwt = get_jwt()
    user_type = jwt['position']
    print(user_type)
    if user_type.find('restaurant') != -1:
        user_type = 'restaurant'
    if user_type == 'admin':
        return True
    if user_type == 'restaurant':
        if target_permission != 'admin':
            return True
        return False
    if user_type == 'worker':
        if target_permission == 'worker':
            return True
        return False

def get_restaurant_id():
    jwt = get_jwt()
    if jwt['position'].find('restaurant') == -1:
        return None
    return jwt['position'].split('_')[1]

def get_user_id():
    return get_jwt_identity()

def generate_token(user_account, user_type):
    return create_access_token(identity=user_account, additional_claims={'position': user_type})