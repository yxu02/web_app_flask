import pymongo


class Database:
    URI = 'mongodb://127.0.0.1:27017'
    DATABASE = None

    @staticmethod
    def initialize():
        client = pymongo.MongoClient(Database.URI)
        Database.DATABASE = client['fullstack']

    @classmethod
    def insert(cls, collection, data):
        cls.DATABASE[collection].insert(data)

    @classmethod
    def find(cls, collection, query):
        return cls.DATABASE[collection].find(query)

    @classmethod
    def find_one(cls, collection, query):
        return cls.DATABASE[collection].find_one(query)
