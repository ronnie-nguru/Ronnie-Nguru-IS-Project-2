from datetime import datetime

from sqlalchemy import Column, String, Integer, Numeric, DateTime, ForeignKey
from sqlalchemy.orm import relationship

from app.models.base_model import Base, BaseModel


class BankAccount(BaseModel, Base):
    __tablename__ = 'bank_accounts'
    user_id = Column(Integer, ForeignKey('users.id'), nullable=False)
    account_number = Column(String(20), unique=True, nullable=False)
    account_type = Column(String(20), nullable=False)
    balance = Column(Numeric(15, 2), default=0.00, nullable=False)
    currency = Column(String(3), default='USD', nullable=False)
    status = Column(String(25), default='active')  # Active, Closed, Frozen

    user = relationship('User', back_populates='bank_accounts')
    transactions = relationship('Transaction', back_populates='account')

    def __repr__(self):
        return f'<BankAccount {self.id}: {self.account_number}, Balance: {self.balance}, Currency: {self.currency}>'
