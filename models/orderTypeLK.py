from datetime import datetime
from sqlalchemy import Column, Integer, String, Text, DateTime, ForeignKey
from litestar.contrib.sqlalchemy.base import BigIntBase
#
from models.users import Users




class OrderTypeLK(BigIntBase):
    __tablename__ = 'order_type_lk'


    name = Column(String(255), nullable=False)
    code = Column(String(255), nullable=False)
    description = Column(Text, nullable=True)
    created_by = Column(Integer, ForeignKey(Users.id))
    created_at = Column(DateTime, default=datetime.now())
    updated_at = Column(DateTime)

    def __repr__(self):
        return f"<OrderTypeLK(id={self.id}, name={self.name})>"
