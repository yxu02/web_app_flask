from flask_restful import Resource, reqparse
from models.user import UserModel

class UserSignUp(Resource):

    parser = reqparse.RequestParser()
    parser.add_argument('username', required=True)
    parser.add_argument('password', required=True)

    def post(self):
        data = UserSignUp.parser.parse_args()
        _user = UserModel.find_user_by_name(data['username'])
        if _user is not None:
            return {'message':"User is already registered."}, 400

        _user = UserModel(**data)
        try:
            _user.save_to_db()

        except:
            return {'message': 'an error occurred at save to database'}, 500
        return {'message': 'succeed to register user!'}, 201