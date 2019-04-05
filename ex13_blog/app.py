from database import Database
from post import Post
from blog import Blog
from menu import Menu
from pprint import pprint

Database.initialize()

menu = Menu()

menu.run_menu()
# blog = Blog(
#             title="test title",
#             description="test description",
#             author="test author")
#
# blog.new_post()
#
# blog.save_to_db()
#
# b= Blog.find_blog(blog.id)
#
# pprint(b.find_posts())
