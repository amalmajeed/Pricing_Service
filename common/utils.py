import re
from passlib.hash import pbkdf2_sha512

class Utils:
    @staticmethod
    def email_is_valid(email: str) -> bool:
        # Something that starts with atleast one word or a '-' followed by '@' then a word and period combination and then few characters
        email_pattern = re.compile(r'^[\w-]+@([\w-]+\.)+[\w]+$')
        return True if email_pattern.match(email) else False

    @staticmethod
    def hash_password(password: str) -> str:
        return pbkdf2_sha512.encrypt(password)

    @staticmethod
    def check_hashed_password(password: str, hashed_password: str):
        return pbkdf2_sha512.verify(password, hashed_password)
