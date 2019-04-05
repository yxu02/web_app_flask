from database import Database as db
import uuid
from datetime import datetime


class Post:
    def __init__(self, **kwargs):
        self.blog_id = kwargs.get('blog_id', None)
        self.title = kwargs.get('title', None)
        self.content = kwargs.get('content', None)
        self.author = kwargs.get('author', None)
        self.id = kwargs.get('id', uuid.uuid4().hex)
        self.created_date = kwargs.get('date', datetime.utcnow())

    def save_to_db(self):
        db.insert(collection='posts', data=self.json())

    def json(self):
        return {
            'id': self.id,
            'title': self.title,
            'content': self.content,
            'author': self.author,
            'blog_id': self.blog_id,
            'created_date': self.created_date
        }

    @classmethod
    def find_post(cls, _id):
        return db.find_one(collection='posts', query={'id': _id})

    @classmethod
    def find_posts(cls, _id):
        return [post for post in db.find(collection='posts', query={'blog_id': _id})]
