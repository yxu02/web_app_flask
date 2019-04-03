from db import db
from flask import request, url_for
from libs.mailgun import Mailgun
from models.confirmation import ConfirmationModel


class UserModel(db.Model):
    __tablename__ = "users"

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), nullable=False, unique=True)
    password = db.Column(db.String(80), nullable=False)
    email = db.Column(db.String(80), nullable=False, unique=True)

    # set up one-to-many relationship, set up lazy loading, set up cascade deleting
    confirmation = db.relationship("ConfirmationModel", lazy="dynamic", cascade="all, delete-orphan")

    @classmethod
    def find_by_username(cls, username: str) -> "UserModel":
        return cls.query.filter_by(username=username).first()

    @classmethod
    def find_by_email(cls, email: str) -> "UserModel":
        return cls.query.filter_by(email=email).first()

    @classmethod
    def find_by_id(cls, _id: int) -> "UserModel":
        return cls.query.filter_by(id=_id).first()

    @property
    def find_last_confirmation(self) -> "ConfirmationModel":
        return self.confirmation.order_by(db.desc(ConfirmationModel.expire_at)).first()

    def send_confirmation_email(self):
        # # argument in url_for automatically remove special characters like user_confirmed becomes userconfirmed
        link = request.url_root[:-1] + url_for("confirmation", confirmation_id=self.find_last_confirmation.id)
        subject = "Registration Confirmation",
        text = f"Please click the link to confirmation your registration: {link}"
        html = f'<html>Please click the link to confirmation your registration: <a href="{link}">{link}</a></html>'
        Mailgun.send_email(self.email, subject, text, html)

    def save_to_db(self) -> None:
        db.session.add(self)
        db.session.commit()

    def delete_from_db(self) -> None:
        db.session.delete(self)
        db.session.commit()
