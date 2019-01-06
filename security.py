from model.user import UserModel


def auth(username, password):
    user = UserModel.find_by_username(username)
    if user and user.password == password:
        return user


def identity(payload: dict):
    user_id = payload['identity']
    return UserModel.find_by_id(user_id)
