import datetime

from flask import Flask
from flask_jwt import JWT
from flask_restful import Api

from resources.item import Item, Items
from resources.user import UserSignUp
from resources.store import Store, Stores
from security import authenticate, identity

app = Flask(__name__)
app.secret_key = 'faefasdfawefas'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///data.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['PROPAGATE_EXCEPTIONS'] = True
api = Api(app)

app.config['JWT_AUTH_URL_RULE'] = '/login'  # /login
app.config['JWT_EXPIRATION_DELTA'] = datetime.timedelta(seconds=3600)
jwt = JWT(app, authenticate, identity)


@app.before_first_request
def create_tables():
    db.create_all()


@app.route('/')
def home():
    pass


api.add_resource(Item, '/item/<string:name>')
api.add_resource(Items, '/items')
api.add_resource(UserSignUp, '/signup')
api.add_resource(Stores, '/stores')
api.add_resource(Store, '/store/<string:name>')

# if run in pycharm, comment out next line
# if __name__ == '__main__':
from db import db

db.init_app(app)
app.run(debug=True)
