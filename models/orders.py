from datetime import datetime
from sqlalchemy import Column, Integer, String, Float, SmallInteger, ForeignKey, DateTime
from litestar.contrib.sqlalchemy.base import BigIntBase
#
from models.transactionsLog import TransactionsLog
from models.orderTypeLK import OrderTypeLK
from models.users import Users




class Orders(BigIntBase):
    __tablename__ = 'orders'

    urn = Column(String(255), nullable=False)
    transaction_log_id = Column(Integer, ForeignKey(TransactionsLog.id))
    quantity = Column(Integer, nullable=False)
    price = Column(Float, nullable=False)
    order_type_id = Column(Integer, ForeignKey(OrderTypeLK.id))
    average_traded_price = Column(Float, nullable=False)
    traded_quantity = Column(Float, nullable=False)
    order_active = Column(SmallInteger, nullable=False)
    created_by = Column(Integer, ForeignKey(Users.id))
    created_at = Column(DateTime, default=datetime.now())
    updated_at = Column(DateTime)

    def __repr__(self):
        return f"<Orders(id={self.id}, urn={self.urn})>"
