from flask_restful import Resource
from models.store import StoreModel
from flask_jwt import jwt_required


class Store(Resource):

    def get(self, name):
        store = StoreModel.find_by_name(name)
        return store.json() if store else {'message': 'object not found'}, 404

    @jwt_required()
    def post(self, name):
        store = StoreModel.find_by_name(name)
        if store:
            return {'store': store.json(), 'message': 'store already exist'}, 400
        else:
            store = StoreModel(name)
        try:
            store.save_to_db()
        except:
            return {'message': 'error occurred at save data'}, 500
        return store.json(), 201

    @jwt_required()
    def delete(self, name):
        store = StoreModel.find_by_name(name)
        if store is None:
            return {'message': 'object not found'}, 400
        store.delete_from_db()
        return {'store': store.json(), 'message': 'store deleted'}


class Stores(Resource):

    def get(self):
        return {'stores':[store.json() for store in StoreModel.find_all()]}
