def sanitize_user(user):
    """
    Remove sensitive data from user object and convert snake_case to camelCase
    """
    user_dict = user.to_mongo().to_dict()
    if '_id' in user_dict:
        user_dict['id'] = str(user_dict['_id'])
        del user_dict['_id']
    if 'password' in user_dict:
        del user_dict['password']

    # Convert snake_case to camelCase for frontend compatibility
    if 'is_verified' in user_dict:
        user_dict['isVerified'] = user_dict['is_verified']
        del user_dict['is_verified']

    if 'is_admin' in user_dict:
        user_dict['isAdmin'] = user_dict['is_admin']
        del user_dict['is_admin']

    return user_dict
