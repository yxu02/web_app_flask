from flask import Flask, request
from flask_jwt import JWT, jwt_required
from flask_restful import Resource, Api, reqparse

from ex2.security import authenticate, identity

app = Flask(__name__)
app.secret_key = 'faefasdfawefas'
api = Api(app)
items = []
jwt = JWT(app, authenticate, identity)


@app.route('/')
def home():
    pass


class Item(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument('price', required=True)

    def get(self, name):
        item = next(filter(lambda x: x['name'] == name, items), None)
        return {'item': item} if item else 404

    @jwt_required()
    def post(self, name):
        item = next(filter(lambda x: x['name'] == name, items), None)
        if item is not None:
            return item, 400
        data = Item.parser.parse_args() # data = {'price': xxx}
        item = {'name': name, 'price': data['price']}
        items.append(item)
        return item, 201

    @jwt_required()
    def delete(self, name):
        item = next(filter(lambda x: x['name'] == name, items), None)
        if item:
            items.remove(item)
            return {'item': item, 'message': 'item deleted'}
        return {'message': 'item not found'}, 400

    @jwt_required()
    def put(self, name):
        item = next(filter(lambda x: x['name'] == name, items), None)
        data = Item.parser.parse_args()
        new_item = {'name': name, 'price': data['price']}
        if not item:
            items.append(new_item)
            return new_item, 201
        else:
            item.update(data)
            return new_item, 200


class Items(Resource):

    def get(self):
        if not items:
            return {'message': '404 - not found'}, 404
        return {'items': items}


api.add_resource(Item, '/item/<string:name>')
api.add_resource(Items, '/items')

if __name__ == '__main__':
    app.run()
