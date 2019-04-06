from flask import Flask, render_template, request, session, make_response
from common.database import Database
from models.user import User
from models.blog import Blog
from models.post import Post

app = Flask(__name__)
app.secret_key = 'awefae'


@app.route('/')
def home():
    return render_template('home.html')


@app.route('/login')
def login():
    return render_template('login.html')


@app.route('/register')
def register():
    return render_template('register.html')


@app.before_first_request
def initialize_database():
    Database.initialize()


@app.route('/auth/login', methods=['POST'])
def login_user():
    email = request.form['email']
    password = request.form['password']
    if User.login_valid(email, password):
        User.login(email)
    else:
        session['email'] = None
        return make_response(home())

    return render_template('profile.html', email=session['email'])


@app.route('/auth/register', methods=['POST'])
def register_user():
    email = request.form['email']
    password = request.form['password']
    User.register(email, password)
    return render_template('profile.html', email=session['email'])

@app.route('/blogs/<string:user_id>')
@app.route('/blogs')
def user_blogs(user_id=None):
    user = None
    if user_id is not None:
        user = User.get_by_id(user_id)
        if user is None:
            user = User.get_by_email(session['email'])
    else:
        user = User.get_by_email(session['email'])

    blogs = user.get_blogs()

    return render_template('user_blogs.html',
                           blogs=blogs, email=user.email)


@app.route('/blogs/new', methods=['POST', 'GET'])
def create_new_blog():
    if request.method == 'GET':
        return render_template('new_blog.html')
    else:
        user = User.get_by_email(session['email'])
        title = request.form['title']
        # author, title, description, author_id, _id
        description = request.form['description']
        author = user.email
        author_id = user._id
        blog = Blog(author, title, description, author_id)
        blog.save_to_mongo()
        return make_response(user_blogs(user._id))


@app.route('/posts/<string:blog_id>')
def blog_posts(blog_id):
    blog = Blog.from_mongo(blog_id)
    if blog is None:
        return make_response(user_blogs())
    else:
        posts = blog.get_posts()
        return render_template('posts.html', posts=posts, blog_title=blog.title, blog_id=blog._id)


@app.route('/posts/new/<string:blog_id>', methods=['POST', 'GET'])
def create_new_post(blog_id):
    if request.method == 'GET':
        return render_template('new_post.html', blog_id=blog_id)
    else:
        user = User.get_by_email(session['email'])
        author = user.email
        title = request.form['title']
        content = request.form['content']
        # blog_id, title, content, author
        post = Post(blog_id, title, content, author)
        post.save_to_mongo()
        return make_response(blog_posts(blog_id))


if __name__ == '__main__':
    app.run(debug=True)
