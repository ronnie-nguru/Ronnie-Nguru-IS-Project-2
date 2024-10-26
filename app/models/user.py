from sqlalchemy import Column, String
from sqlalchemy.orm import relationship
from hashlib import md5
from flask_login import UserMixin

from app.models.base_model import BaseModel, Base


class User(BaseModel, UserMixin, Base):
    __tablename__ = 'users'
    username = Column(String(16), unique=True)
    first_name = Column(String(32), nullable=False)
    last_name = Column(String(32), nullable=False)
    email = Column(String(64), nullable=False)
    phone_number = Column(String(32))
    _password = Column(String(128), nullable=False)

    bank_accounts = relationship('BankAccount', back_populates='user')

    @property
    def password(self):
        raise AttributeError(
            'Cannot access password attribute outside of User context')

    @password.setter
    def password(self, pwd):
        self._password = md5(pwd.encode()).hexdigest()

    def verify_password(self, pwd):
        return md5(pwd.encode()).hexdigest() == self._password
