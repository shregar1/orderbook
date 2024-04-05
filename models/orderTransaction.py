from datetime import datetime
from sqlalchemy import Column, Integer, String, Float, DateTime, ForeignKey
from litestar.contrib.sqlalchemy.base import BigIntBase
#
from models.orders import Orders
from models.users import Users




class OrderTransaction(BigIntBase):
    __tablename__ = 'order_transaction'


    urn = Column(String(255), nullable=False)
    bid_order_id = Column(Integer, ForeignKey(Orders.id))
    ask_order_id = Column(Integer, ForeignKey(Orders.id))
    quantity = Column(Integer, nullable=False)
    price = Column(Float, nullable=False)
    execution_timestamp = Column(DateTime, default=datetime.now())
    created_by = Column(Integer, ForeignKey(Users.id))
    created_at = Column(DateTime, default=datetime.now())
    updated_at = Column(DateTime)

    def __repr__(self):
        return f"<OrderTransaction(id={self.id}, urn={self.urn})>"
