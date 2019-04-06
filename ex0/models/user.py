from uuid import uuid4
from common.database import Database
from flask import session
from models.blog import Blog


class User:
    def __init__(self, email, password, _id=None):
        self.email = email
        self.password = password
        self._id = uuid4().hex if _id is None else _id
        pass

    @classmethod
    def get_by_email(cls, email):
        data = Database.find_one('users', {'email': email})
        if data is not None:
            return cls(**data)

    @classmethod
    def get_by_id(cls, _id):
        data = Database.find_one('users', {'_id': _id})
        if data is not None:
            return cls(**data)

    @classmethod
    def login_valid(cls, email, password) -> bool:
        user = cls.get_by_email(email)
        return True if user and user.password == password else False

    @classmethod
    def register(cls, email, password) -> bool:
        user = cls.get_by_email(email)
        if user is None:
            user = User(email, password)
            user.save_to_database()
            session['email'] = email
            return True
        return False

    @staticmethod
    def login(email):
        session['email'] = email

    @staticmethod
    def logout():
        session['email'] = None

    def get_blogs(self):
        return Blog.find_by_author_id(self._id)

    def new_blog(self, title, description):
        blog = Blog(self.email, title, description, self._id)
        blog.save_to_mongo()

    def new_post(self, blog_id, title, content):
        blog = Blog.from_mongo(blog_id)
        blog.new_post(title, content)

    def save_to_database(self):
        Database.insert('users', self.json())

    def json(self):
        return {
            '_id': self._id,
            'email': self.email,
            'password': self.password
        }
