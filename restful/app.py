from flask import Flask, jsonify, request
from flask_restful import Resource, Api
from flask_jwt import JWT, jwt_required
from restful.security import authenticate, identity

app = Flask(__name__)
app.secret_key = 'david'
api = Api(app)

jwt = JWT(app, authenticate, identity)

items = []


class ItemList(Resource):

    def get(self):
        response = {'items': items}
        return response, 200


class Item(Resource):

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

        data = request.get_json(silent=True)
        price = data['price']
        item = {
            'name': name,
            'price': price if price else 0.0
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
        global items
        data = request.get_json(silent=True)
        price = data.get('price')

        match = next((item for item in items if item['name'] == name), None)
        if items and match: # if there are items and there's a match, then update
            old = match['price']
            match['price'] = price if price else old
        else:               # otherwise just append
            item = {
                'name': name,
                'price': price if price else 0
            }
            items.append(item)
        return {'message': 'item has been put'}, 201


api.add_resource(ItemList, '/items')
api.add_resource(Item, '/item/<string:name>')

if __name__ == '__main__':
    app.run(port=5000, debug=True)
