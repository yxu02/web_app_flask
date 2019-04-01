from flask_jwt import jwt_required
from flask_restful import reqparse, Resource

from models.item import ItemModel


class Item(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument('price', type=float, required=True)
    parser.add_argument('store_id', type=int, required=True)


    def get(self, name):
        _item = ItemModel.find_by_name(name)
        return _item.json() if _item else {'message': 'item not found'}, 404

    @jwt_required()
    def post(self, name):
        _item = ItemModel.find_by_name(name)
        if _item:
            return {'item': _item.json(), 'message': 'item already exists'}, 400
        data = Item.parser.parse_args()  # data = {'price': xxx, 'store_id': xxx}
        item = ItemModel(name, **data)

        try:
            item.save_to_db()
        except:
            return {'message': 'an error occurred at save to database'}, 500
        return item.json(), 201

    @jwt_required()
    def delete(self, name):
        _item = ItemModel.find_by_name(name)
        if _item:
            _item.delete_from_db()
            return {'item': _item.json(), 'message': 'item deleted'}
        return {'message': 'item not found'}, 400

    @jwt_required()
    def put(self, name):
        item = ItemModel.find_by_name(name)
        data = Item.parser.parse_args()
        if item:
            item.price = data['price']      # cannot use item['price']
        else:
            item = ItemModel(name, **data)

        try:
            item.save_to_db()
        except:
            return {'message': 'an error occurred at save to database'}, 500
        return item.json(), 201


class Items(Resource):

    def get(self):
        return {'items': [i.json() for i in ItemModel.find_all()]}
