from db import db
from uuid import uuid4
from time import time

EXPIRATION_DELTA = 1800  # 30mins


class ConfirmationModel(db.Model):
    __tablename__ = "confirmations"

    id = db.Column(db.String(50), primary_key=True)
    expire_at = db.Column(db.Integer, nullable=False)
    confirmed = db.Column(db.Boolean, default=False, nullable=False)
    # foreign key asks the FK column from the sql table instead from the sqlalchemy model
    user_id = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=False)

    user = db.relationship("UserModel")

    def __init__(self, user_id, **kwargs):
        super().__init__(**kwargs)
        self.id = uuid4().hex
        self.user_id = user_id
        self.expire_at = int(time()) + EXPIRATION_DELTA

    @classmethod
    def find_by_id(cls, _id):
        return cls.query.filter_by(id=_id).first()

    @property   # if a function doesn't change anything, one can decorate to be a calculated property instead of func
    def expired(self):
        return int(time()) > self.expire_at

    def force_to_expire(self):
        if not self.expired:
            self.expire_at = int(time())
            self.save_to_db()

    def save_to_db(self):
        db.session.add(self)
        db.session.commit()

    def remove_from_db(self):
        db.session.delete(self)
        db.session.commit()