from database import Database as db
import uuid
from datetime import datetime
from post import Post


class Blog:
    def __init__(self, **kwargs):
        self.description = kwargs.get('description', None)
        self.title = kwargs.get('title', None)
        self.author = kwargs.get('author', None)
        self.id = kwargs.get('id', uuid.uuid4().hex)
        self.created_date = kwargs.get('date', datetime.utcnow())

    def save_to_db(self):
        db.insert(collection='blogs', data=self.json())

    def json(self):
        return {
            'id': self.id,
            'title': self.title,
            'author': self.author,
            'description': self.description,
            'created_date': self.created_date
        }

    def new_post(self):
        title = input("Enter post title: ")
        content = input("Enter post content: ")
        date = input("Enter post date or leave blank for today (DDMMYYYY): ")
        if not date:
            date = datetime.utcnow()
        else:
            date = datetime.strptime(date, '%d%m%Y')
        post = Post(blog_id=self.id,
                    title=title,
                    content=content,
                    author=self.author,
                    created_date=date)
        post.save_to_db()

    @classmethod
    def find_blog(cls, _id):
        blog = db.find_one(collection='blogs', query={'id': _id})
        return cls(author=blog['author'],
                   title=blog['title'],
                   description=blog['description'],
                   id=blog['id'])

    def find_posts(self):
        return Post.find_posts(self.id)
