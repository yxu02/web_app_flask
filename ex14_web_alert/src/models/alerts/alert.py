from uuid import uuid4
import requests

from src.commons.database import Database
from src.models.alerts.constants import API_KEY, FROM, MAILGUN_URL, ALERT_TIMEOUT
from datetime import datetime, timedelta

from src.models.items.item import Item


class Alert:
    def __init__(self, user_email, price_limit, item_id, last_checked, _id=uuid4().hex):
        self.user_email = user_email
        self.price_limit = price_limit
        self.item = Item.get_by_id(item_id)
        self.last_checked = datetime.utcnow() if not last_checked else last_checked
        self._id = _id

    def __repr__(self):
        return f"<Alert for user {self.user_email} on item {self.item.name} " \
            f"with price limit {self.price_limit}>"

    def send(self):
        return requests.post(
            MAILGUN_URL,
            auth=("api", API_KEY),
            data={
                "from": FROM,
                "to": [self.user_email],
                "subject": f"Price limit reached for {self.item.name}",
                "text": f"We found a deal matching your price limit!\nLink here: {self.item.url}"
            }
        )

    @classmethod
    def find_outdated_alerts(cls, timeout=ALERT_TIMEOUT):
        update_limit = datetime.utcnow() - timedelta(minutes=timeout)

        return [cls(**alert) for alert in Database.find('alerts', {'last_checked': {'$lte': update_limit}})]

    def save_to_db(self):
        Database.update('alerts', {'_id': self._id}, self.json())

    def json(self):
        return {
            '_id': self._id,
            'price_limit': self.price_limit,
            'last_checked': self.last_checked,
            'email': self.user_email,
            'item_id': self.item._id
        }

    def load_item_price(self):
        self.item.load_price()
        self.last_checked = datetime.utcnow()
        self.save_to_db()
        return self.item.price

    def send_email_if_price_reached(self):
        if self.item.price < self.price_limit:
            self.send()
