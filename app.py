from flask import Flask, request
from flask_restful import Api, Resource, reqparse 
from security import authenticate, identity
from flask_jwt import JWT, jwt_required

app = Flask(__name__)
app.secret_key = "my_scret_key"

jwt = JWT(app, authenticate, identity)
api = Api(app)

items = []

class Item(Resource):
    @jwt_required()
    def get(self, name):
        item = next(filter(lambda x: x['name'] == name, items), None)
        return {"item":item}, 200 if item is not None else 404
    
    def post(self, name):
        parser = reqparse.RequestParser()
        #parser.add_argument('name', type=str, required=True)
        parser.add_argument('price', type=float, required=True)
        data = parser.parse_args()
        item = next(filter(lambda x: x == name, items), None)
        if item:
            return {"message": f"item {name} already exist"} , 404
        #
        # data = request.get_json()
        item = {"name": name,
                 "price": data["price"]}
        items.append(item)
        return item, 201

class ItemList(Resource):
    def get(self):
        return {"items": items}
    

api.add_resource(Item, '/item/<string:name>')
api.add_resource(ItemList, '/items')

app.run(port=5000, debug=True)

