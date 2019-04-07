import requests
from bs4 import BeautifulSoup
import re
from src.commons.database import Database
from uuid import uuid4
from src.models.stores.store import Store


class Item:
    def __init__(self, name, url, _id=uuid4().hex):
        self._id = _id
        self.name = name
        self.url = url
        store = Store.get_by_url(url)
        self.tag_name = store.tag_name
        self.query = store.query
        self.price = None

    def __repr__(self):
        return f"<Item {self.name} with URL {self.url}>"

    def load_price(self):
        # < p class ="price price--large" > £219.00< / p >
        content = requests.get(self.url).content
        soup = BeautifulSoup(content, "html.parser")
        element = soup.find(self.tag_name, self.query)
        price_text = element.text.strip()
        price = re.search(r'(\d+.\d+)', price_text).group()
        self.price = float(price)
        return self.price

    def save_to_db(self):
        Database.insert('items', self.json())

    def json(self):
        return {
            '_id': self._id,
            'name': self.name,
            'url': self.url
        }

    @classmethod
    def get_by_id(cls, _id):
        return cls(**Database.find_one('items', {'_id': _id}))
