from werkzeug.security import safe_str_cmp
from restful.user import User


users = [
    User(1, 'david', 'smiles'),
    User(2, 'james', 'ayama')
]

username_mapping = {user.username: user for user in users}
userid_mapping = {user.id: user for user in users}

def authenticate(username, password):
    user = username_mapping.get(username, None)
    if user and safe_str_cmp(user.password, password):
        return user


def identity(payload):
    print(payload)
    userid = payload['identity']
    return userid_mapping.get(userid, None)