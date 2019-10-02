from restful.dbconn import Database
from flask_restful import Resource, reqparse


class User:
    TABLE_NAME = 'users'

    def __init__(self, _id, username, password):
        self.id = _id
        self.username = username
        self.password = password

    @classmethod
    def find_by_username(cls, username):
        with Database() as connection:
            cursor = connection.cursor()
            query = 'SELECT * FROM {} WHERE username = ?'.format(cls.TABLE_NAME)
            result = cursor.execute(query, (username,))
            user = result.fetchone()

        return cls(user[0], user[1], user[2]) if user else None

    @classmethod
    def find_by_id(cls, user_id):
        with Database() as connection:
            cursor = connection.cursor()
            query = 'SELECT * FROM {} WHERE id = ?'.format(cls.TABLE_NAME)
            result = cursor.execute(query, (user_id,))
            user = result.fetchone()
            print(user)

        return cls(user[0], user[1], user[2]) if user else None


class UserRegister(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument('username',
                        type=str,
                        help='This field should not be left blank',
                        required=True)

    parser.add_argument('password',
                        type=str,
                        help='This field should not be left blank',
                        required=True)


    def post(self):
        data = UserRegister.parser.parse_args()
        username = data['username']
        password = data['password']

        user = User.find_by_username(username)
        if not user:
            with Database() as connection:
                cursor = connection.cursor()
                signup = 'INSERT INTO {} VALUES(NULL, ?, ?)'.format(User.TABLE_NAME)
                cursor.execute(signup, (username, password))
                return {'message': 'successfully created'}
        else:
            return {
                'message': 'user already exists'
            }