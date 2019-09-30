from flask import Flask, jsonify, request

app = Flask(__name__)

# POST - used to receive data and we have to deal with it
# GET - used to send data back only

# from the browser's perspective, this is the opposite
# the browser will use POST to send us data
# and use GET to receive data

stores = [
    {
        'name': 'teclado',
        'items': [
            {
                'name': 'REST API with Python and Flask',
                'price': 11.99
            }
        ]
    },
    {
        'name': 'shitty',
        'items': [
            {
                'name': 'Advanced REST API with Python and Flask',
                'price': 12.99
            },
            {
                'name': 'Game of Thrones',
                'price': 15.00
            }
        ]
    }
]


# POST /store {name}
@app.route('/store', methods=['POST'])
def create_store():
    form = {**request.form}
    if form.get('name'):
        new_store = {
            'name': form.get('name'),
            'items': []
        }
        stores.append(new_store)
        return jsonify(new_store)
    else:
        return jsonify({'message': f"no name value sent with request"})


# GET /store/<string:name>
@app.route('/store/<string:name>', methods=['GET'])
def get_store(name):
    for store in stores:
        if store['name'] == name:
            return jsonify(store)
    else:
        return jsonify({'message': f"store with name '{name}' not found."})


# GET /store
@app.route('/store')
def get_stores():
    return jsonify({'stores': stores})


# POST /store/<string:name>/item {name, price}
@app.route('/store/<string:name>/item', methods=['POST'])
def create_item_in_store(name):
    item_data = {**request.form}
    for store in stores:
        if store['name'] == name:
            store['items'].append(item_data)
            return jsonify(store['items'])
    else:
        return jsonify({'message': f"store with name '{name}' not found."})


# GET /store/<string:name>/item
@app.route('/store/<string:name>/item')
def get_items_in_store(name):
    for store in stores:
        if store['name'] == name:
            return jsonify(store['items'])
    else:
        return jsonify({'message': f"store with name '{name}' not found."})


if __name__ == '__main__':
    app.run(port=5000, debug=True)
