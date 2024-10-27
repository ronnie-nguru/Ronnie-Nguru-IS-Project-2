from datetime import datetime

from sqlalchemy import Column, String, Numeric, CheckConstraint, DateTime, Integer, ForeignKey
from sqlalchemy.orm import relationship

from app.models.base_model import BaseModel, Base, time_fmt


class Transaction(BaseModel, Base):
    __tablename__ = 'transactions'
    transaction_type = Column(String(32))
    amount = Column(Numeric(15, 2), nullable=False)
    transaction_date = Column(DateTime, nullable=False,
                              default=datetime.now().strftime(time_fmt))
    description = Column(String(256))
    balance_after = Column(Numeric(15, 2))

    account_id = Column(Integer, ForeignKey('bank_accounts.id'))
    account = relationship('BankAccount', back_populates='transactions')

    __table_args__ = (
        CheckConstraint('amount > 0', name='check_amount_positive'),
    )
