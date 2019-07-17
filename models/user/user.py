import uuid
from dataclasses import dataclass, field
from typing import Dict
from models.model import Model
import models.user.errors as UserErrors
from common.utils import Utils



@dataclass
class User(Model):
    collection: str = field(init=False, default="users")
    email: str
    password: str = field(repr=False)
    _id: str = field(default_factory=lambda: uuid.uuid4().hex)

    @classmethod
    def find_by_email(cls, email: str) -> "User":
        try:
            return cls.find_one_by("email", email)
        except IndexError:
            raise UserErrors.UserNotFoundError("A user with this e-mail was not found in the database ! ")

    @classmethod
    def register_user(cls, email: str, password: str) -> bool:
        # Checking if e-mail format is correct
        if not Utils.email_is_valid(email):
            raise UserErrors.InvalidEmailError("This e-mail does not have the right format ! ")

        # Trying to check if user already exists
        try:
            cls.find_by_email(email)
            raise UserErrors.UserAlreadyRegistered("There is already a user registered in this e-mail id ! ")
        except UserErrors.UserNotFoundError:
            User(email, Utils.hash_password(password)).save_to_mongo()

        return True

    @classmethod
    def is_login_valid(cls, email: str, password: str) -> bool:
        user = cls.find_by_email(email)
        if not Utils.check_hashed_password(password ,user.password):
            raise UserErrors.IncorrectPasswordError(f"Incorrect password for the user {email}")
        return True

    def json(self) -> Dict:
        return {
            '_id': self._id,
            'email': self.email,
            'password': self.password
        }
