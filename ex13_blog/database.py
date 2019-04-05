import pymongo

class Database:
    URI = 'mongodb://localhost:27017'
    DATABASE = None

    @classmethod
    def initialize(cls):
        # this is the client to access all databases at the uri
        client = pymongo.MongoClient(cls.URI)
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

