from passlib.hash import pbkdf2_sha512


class Utils:
    @staticmethod
    def hash_password(password):
        return pbkdf2_sha512.encrypt(password)

    @classmethod
    def check_hashed_password(cls, password, hashed_password):
        return pbkdf2_sha512.verify(password, hashed_password)
