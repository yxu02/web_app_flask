from database import Database as db
from blog import Blog
from pprint import pprint

class Menu:
    def __init__(self):
        self.user = input("Enter author name: ")
        self.blog = None

        if self._check_user_account():
            print(f'Welcome back {self.user}!')
        else:
            self._create_user_account()

    def _check_user_account(self):
        blog = db.find_one('blogs', {'author': self.user})
        if blog is not None:
            self.blog = Blog.find_blog(blog['id'])
            return True
        return False

    def _create_user_account(self):
        title = input("Enter blog title: ")
        description = input("Enter blog description: ")
        blog = Blog(title=title,
                    description=description,
                    author=self.user)
        blog.save_to_db()
        self.blog = blog

    def run_menu(self):
        check = input("Do you want to read or write blogs? R/W ")

        if str.lower(check) == 'r':
            self._list_blogs()
            self._view_blog()
        elif str.lower(check) == 'w':
            self.blog.new_post()
        else:
            print("Thank you!")

    def _list_blogs(self):
        for blog in db.find('blogs', {}):
            print("ID: {}, Title: {}, Author: {}"
                  .format(blog['id'], blog['title'], blog['author']))

    def _view_blog(self):
            _id = input("Enter blog id: ")
            blog = Blog.find_blog(_id)
            posts = blog.find_posts()
            for post in posts:
                print("Date: {}, title: {}\n\n{}".format(post['created_date'], post['title'], post['content']))
