from flask_restful import Resource
from flask import request
from flask_jwt_extended import (
    jwt_required,
    fresh_jwt_required
)
from models.item import ItemModel
from schemas.item import ItemSchema

itemSchema = ItemSchema
item_list_schema = ItemSchema(many=True)


class Item(Resource):
    @jwt_required  # No longer needs brackets
    def get(self, name):
        item = ItemModel.find_by_name(name)
        if item:
            return item.dump(item), 200
        return {"message": "Item not found."}, 404

    @fresh_jwt_required
    def post(self, name):
        if ItemModel.find_by_name(name):
            return {"message": "An item with name '{}' already exists.".format(name)}, 400

        item_json = request.get_json()
        item_json['name'] = name

        item = itemSchema.load(item_json)

        try:
            item.save_to_db()
        except:
            return {"message": "An error occurred while inserting the item."}, 500

        return itemSchema.dump(item), 201

    @jwt_required
    def delete(self, name):
        item = ItemModel.find_by_name(name)
        if item:
            item.delete_from_db()
            return {"message": "Item deleted."}, 200
        return {"message": "Item not found."}, 404

    def put(self, name):
        item_json = request.get_json()

        item = ItemModel.find_by_name(name)

        if item:
            item.price = item_json['price']
        else:
            item_json['name'] = name

            item = itemSchema.load(item_json)

        item.save_to_db()

        return item.json(), 200


class ItemList(Resource):
    def get(self):
        return {"items": item_list_schema.dump(ItemModel.find_all())}, 200
