from uuid import uuid4
from src.commons.database import Database
from src.commons.utils import Utils
from src.models.users.errors import IncorrectPasswordError, UserNotExistsError


class User:
    def __init__(self, email, password, _id=uuid4().hex):
        self.email = email
        self.password = password
        self._id = _id

    def __repr__(self):
        return f"<User {self.email}>"

    @classmethod
    def is_login_valid(cls, email, password):
        user = Database.find_one('users', {'email': email})

        if user is None:
            raise UserNotExistsError("User does not exist!")
        else:
            if not Utils.check_hashed_password(password, user['password']):
                raise IncorrectPasswordError("Password not match!")
        return True
