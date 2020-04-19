from flask import Flask, jsonify, request

app = Flask(__name__)

stores = [
    {
        'name': "MY_store",
        'items':[{
            'name': 'item1',
            'price': 100,
        }]
    }
]

# POST /store data: {name:}
@app.route('/store', methods=["POST"])
def create_store():
    request_store = request.get_json()
    new_store = {
        'name': request_store["name"],
        'items': [] 
    }
    stores.append(new_store)
    return jsonify(new_store)

# GET /store/<string:name> 
@app.route('/store/<string:name>')
def get_store(name):
    for store in stores:
        if store['name'] == name:
            return jsonify(store)
    return jsonify({'message': 'store not found'})
# GET /store
@app.route('/store')
def get_stores():
    return jsonify({"store": stores})

#POST /store/<string:name>/item {name:, price:}
@app.route('/store/<string:name>/item', methods=["POST"])
def create_item_in_store(name):
    request_data = request.get_json()
    for store in stores:
        if store['name'] == name:
            new_item = {
                "name": request_data["name"],
                "price": request_data["price"]
            }
            store["items"].append(new_item)
            return jsonify(store)
    return jsonify({'message': 'store not found'})
#GET /store/<string:name>/item

@app.route('/store/<string:name>/item', methods=["GET"])
def get_item_in_store(name):
    for store in stores:
        if store["name"] == name:
            return jsonify(store["items"])
    return jsonify({"no item found"})

app.run(port=5000, debug=True)