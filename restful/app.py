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
        return jsonify(response)


class Item(Resource):

    @jwt_required()
    def get(self, name):
        item = next((item for item in items if item['name'] == name), None)

    #    error_msg = {'message': f'item with name {name} was not found'}
        return {'item': item}, 200 if item else 404

    def post(self, name):
        item = next((item for item in items if item['name'] == name), None)
        if item:
            error_msg = {'message': f'item with name {name} already exists'}
            return error_msg, 400   #   bad request

        data = request.get_json(silent=True)
        price = data['price']
        item = {
            'name': name,
            'price': price if price is not None else 0.0
        }
        items.append(item)
        return item, 201


api.add_resource(ItemList, '/items')
api.add_resource(Item, '/item/<string:name>')

if __name__ == '__main__':
    app.run(port=5000, debug=True)
