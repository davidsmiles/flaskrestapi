from werkzeug.security import safe_str_cmp
from restful.user import User


def authenticate(username, password):
    user = User.find_by_username(username)
    if user and safe_str_cmp(user.password, password):
        return user


def identity(payload):
    print(payload)
    userid = payload['identity']
    return User.find_by_id(userid)
