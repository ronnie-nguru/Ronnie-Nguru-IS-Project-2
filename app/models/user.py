from sqlalchemy import Column, String
from hashlib import md5
from flask_login import UserMixin

from app.models.base_model import BaseModel, Base


class User(BaseModel, UserMixin, Base):
    first_name = Column(String(32))
    last_name = Column(String(32))
    email = Column(String(64), nullable=False)
    phone_number = Column(String(32))
    _password = Column(String(128), nullable=False)

    @property
    def password(self):
        raise AttributeError(
            'Cannot access password attribute outside of User context')

    @password.setter
    def password(self, pwd):
        self._password = md5(pwd.encode()).hexdigest()

    def verify_password(self, pwd):
        return md5(pwd.encode()).hexdigest() == self._password
