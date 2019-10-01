from flask import Flask, jsonify, request, render_template

app = Flask(__name__)

# POST - used to receive data and we have to deal with it
# GET - used to send data back only

# from the browser's perspective, this is the opposite
# the browser will use POST to send us data
# and use GET to receive data

stores = []



@app.route('/')
def home():
    return render_template('index.html')

# POST /store {name}
@app.route('/store', methods=['POST'])
def create_store():
    form = request.get_json()
    print(form)
    if form.get('name'):
        new_store = {
            'name': form['name'],
            'items': []
        }
        stores.append(new_store)
        return jsonify(new_store)
    return jsonify({'message': f"no name value sent with request"})


# GET /store/<string:name>
@app.route('/store/<string:name>', methods=['GET'])
def get_store(name):
    for store in stores:
        if store['name'] == name:
            return jsonify(store)
    return jsonify({'message': f"store with name '{name}' not found."})


# GET /store
@app.route('/store')
def get_stores():
    return jsonify({'stores': stores})


# POST /store/<string:name>/item {name, price}
@app.route('/store/<string:name>/item', methods=['POST'])
def create_item_in_store(name):
    item_data = request.get_json()
    for store in stores:
        if store['name'] == name:
            store['items'].append(item_data)
            return jsonify(store['items'])
    return jsonify({'message': f"store with name '{name}' not found."})


# GET /store/<string:name>/item
@app.route('/store/<string:name>/item')
def get_items_in_store(name):
    for store in stores:
        if store['name'] == name:
            return jsonify(store['items'])
    return jsonify({'message': f"store with name '{name}' not found."})


if __name__ == '__main__':
    app.run(port=5000, debug=True)
