from flask_restful import Resource
from models.store import StoreModel
from schemas.store import StoreSchema

store_schema = StoreSchema()
store_list_schema = StoreSchema(many=True)


class Store(Resource):
    def get(self, name):
        store = StoreModel.find_by_name(name)
        if store:
            return store_schema.dump(store)
        return {"message": "Store not found."}, 404

    def post(self, name):
        if StoreModel.find_by_name(name):
            return {"message": "A store with name '{}' already exists.".format(name)}, 400

        store = StoreModel(name=name)  # StoreMode __init__ is gone. Use db.Model that use dict to initialize store
        try:
            store.save_to_db()
        except:
            return {"message": "An error occurred while creating the store."}, 500

        return store_schema.dump(store), 201

    def delete(self, name):
        store = StoreModel.find_by_name(name)
        if store:
            store.delete_from_db()

        return {"message": "Store deleted."}


class StoreList(Resource):
    def get(self):
        return {"stores": store_list_schema.dump(StoreModel.find_all())}
