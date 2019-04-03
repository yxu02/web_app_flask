from flask import make_response, render_template
from flask_restful import Resource
from models.confirmation import ConfirmationModel
from models.user import UserModel
from db import db
from time import time
from schemas.confirmation import ConfirmationSchema
from libs.mailgun import MailgunException
import traceback

confirmationSchema = ConfirmationSchema()

class Confirmation(Resource):

    @classmethod
    def get(cls, confirmation_id: str):
        """Return confirmation HTML information"""
        confirmation = ConfirmationModel.find_by_id(confirmation_id)

        if not confirmation:
            return {'message': "not found"}, 404

        elif confirmation.expired:
            return {'message': "already expired"}, 400

        elif confirmation.confirmed:
            return {'message': "already confirmed"}, 400

        confirmation.confirmed = True
        confirmation.save_to_db()

        header = {'Content-Type': 'text/html'}

        return make_response(render_template("confirmation_page.html", email=confirmation.user.email), 200, header)


class ConfirmationByUser(Resource):
    @classmethod
    def get(cls, user_id: int):
        """Return confirmation for a given user. For testing only"""
        user = UserModel.find_by_id(user_id)

        if not user:
            return {'message': 'user not found'}, 404

        return {
                "current time": int(time()),
                "Confirmations": [confirmationSchema.dump(each)
                                  for each in user.confirmation.order_by(db.desc(ConfirmationModel.expire_at))]}


    @classmethod
    def post(cls, user_id: int):
        """Resend confirmation email"""
        user = UserModel.find_by_id(user_id)

        if not user:
            return {'message': 'user not found'}, 404

        try:
            confirmation = user.find_last_confirmation

            if confirmation:
                if confirmation.confirmed:
                    return {'message': "already confirmed"}, 400

                confirmation.force_to_expire()

            new_confirmation = ConfirmationModel(user_id)
            new_confirmation.save_to_db()
            user.send_confirmation_email()
        except MailgunException as e:
            return {'message': str(e)}, 500
        except:
            traceback.print_exc()
            return {'message': 'resent confirmation email failed'}, 500
        return {'message': 'resent confirmation email'}, 200
