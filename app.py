from flask import Flask, jsonify

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
                'name': 'REST API with Python and Flask',
                'price': 11.99
            }
        ]
    }
]


# POST /store {name}
@app.route('/store', methods=['POST'])
def create_store():
    pass


# GET /store/<string:name>
@app.route('/store/<string:name>', methods=['GET'])
def get_store(name):
    data = [store for store in stores if store['name'] == name]
    return jsonify(data)


# GET /store
@app.route('/store')
def get_stores():
    return jsonify({'stores': stores})


# POST /store/<string:name>/item {name, price}
@app.route('/store/<string:name>/item', methods=['POST'])
def create_item_in_store(name):
    pass



# GET /store/<string:name>/item
@app.route('/store/<string:name>/item')
def get_items_in_store(name):
    pass


if __name__ == '__main__':
    app.run(port=5000, debug=True)