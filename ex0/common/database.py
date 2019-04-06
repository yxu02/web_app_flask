import pymongo


class Database(object):
    URI = "mongodb://127.0.0.1:27017"
    DATABASE = None

    @classmethod
    def initialize(cls):
        client = pymongo.MongoClient(Database.URI)
        cls.DATABASE = client['fullstack']

    @classmethod
    def insert(cls, collection, data):
        cls.DATABASE[collection].insert(data)

    @classmethod
    def find(cls, collection, query):
        return cls.DATABASE[collection].find(query)

    @classmethod
    def find_one(cls, collection, query):
        return cls.DATABASE[collection].find_one(query)
