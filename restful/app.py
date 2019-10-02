from flask import Flask, jsonify
from flask_restful import Resource, Api, reqparse
from flask_jwt import JWT, jwt_required
from restful.security import authenticate, identity

from datetime import timedelta

from restful.user import UserRegister

app = Flask(__name__)
app.secret_key = 'david'
api = Api(app)

app.config['JWT_AUTH_URL_RULE'] = '/login'
jwt = JWT(app, authenticate, identity)
app.config['JWT_EXPIRATION_DELTA'] = timedelta(seconds=1800)
app.config['JWT_AUTH_USERNAME_KEY'] = 'username'

items = []

@jwt.auth_request_handler
def customized_response_handler(access_token, identity):
    return jsonify({
        'token': access_token.decode('utf-8'),
        'userid': identity.id
    })


# @jwt.jwt_error_handler
# def customized_error_handler(error):
#     return jsonify({
#         'message': error.description,
#         'code': error.code
#     })

class ItemList(Resource):

    def get(self):
        response = {'items': items}
        return response, 200


class Item(Resource):

    parser = reqparse.RequestParser()
    parser.add_argument('price',
                        type=float,
                        required=True,
                        help='This field cannot be left blank')

    def get(self, name):
        item = next((item for item in items if item['name'] == name), None)

    #    error_msg = {'message': f'item with name {name} was not found'}
        return {'item': item}, 200 if item else 404

    def post(self, name):
        """
        :param name:
        :return error_msg if item already exists with status code 400
                or item with status code 201 if successfully created:
        """
        item = next((item for item in items if item['name'] == name), None) # check if item already exists

        if item:    # True if exists
            error_msg = {'message': f'item with name {name} already exists'}
            return error_msg, 400

        data = Item.parser.parse_args()
        price = data.get('price')

        item = {
            'name': name,
            'price': price
        }
        items.append(item)
        return item, 201

    def delete(self, name):
        global items
        items = list((each for each in items if each['name'] != name))
        return {
            'message': 'item deleted'
        }, 200

    def put(self, name):
        data = Item.parser.parse_args()
        price = data.get('price')

        match = next((item for item in items if item['name'] == name), None)
        if match: # if there are items and there's a match, then update
            match.update(data)
        else:               # otherwise just append
            item = {
                'name': name,
                'price': price
            }
            items.append(item)
        return {'message': 'item has been put'}, 201


api.add_resource(ItemList, '/items')
api.add_resource(Item, '/item/<string:name>')
api.add_resource(UserRegister, '/signup')

if __name__ == '__main__':
    app.run(port=5000, debug=True)
