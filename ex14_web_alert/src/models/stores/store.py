from uuid import uuid4
from src.commons.database import Database


class Store:
    def __init__(self, name, url_prefix, tag_name, query, _id=uuid4().hex):
        self.name = name
        self.url_prefix = url_prefix
        self.tag_name = tag_name
        self.query = query
        self._id = _id

    def __repr__(self):
        return f"<Store {self.name}>"

    def json(self):
        return {
            '_id': self._id,
            'name': self.name,
            'url_prefix': self.url_prefix,
            'tag_name': self.tag_name,
            'query': self.query
        }

    @classmethod
    def get_by_id(cls, _id):
        return cls(**Database.find_one('stores', {'_id': _id}))

    def save_to_db(self):
        Database.insert('stores', self.json())

    @classmethod
    def get_by_name(cls, name):
        return cls(**Database.find_one('stores', {'name': name}))

    @classmethod
    def get_by_url_prefix(cls, prefix: str):
        return cls(**Database.find_one('stores', {'url_prefix': {'$regex': '^{}'.format(prefix)}}))

    @classmethod
    def get_by_url(cls, url):
        i = 0
        while i < len(url):
            store_json = Database.find_one('stores', {'url_prefix': {'$regex': '^{}'.format(url[:i+1])}})
            if store_json:
                return cls(**store_json)
            i+=1
        pass
