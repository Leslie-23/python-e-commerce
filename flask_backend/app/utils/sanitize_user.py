def sanitize_user(user):
    """
    Remove sensitive data from user object
    """
    user_dict = user.to_mongo().to_dict()
    if '_id' in user_dict:
        user_dict['id'] = str(user_dict['_id'])
        del user_dict['_id']
    if 'password' in user_dict:
        del user_dict['password']
    return user_dict
