from datetime import datetime
from sqlalchemy import Column, Integer, String, Text, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from litestar.contrib.sqlalchemy.base import BigIntBase
#
from models.httpMethodLK import HTTPMethodLK
from models.users import Users



class APILK(BigIntBase):
    __tablename__ = 'api_lk'


    name = Column(String(255), nullable=False)
    method = Column(Integer, ForeignKey(HTTPMethodLK.id))
    description = Column(Text, nullable=True)
    endpoint = Column(Text, nullable=False)
    created_by = Column(Integer, ForeignKey(Users.id))
    created_at = Column(DateTime, default=datetime.now())
    updated_at = Column(DateTime)

    def __repr__(self):
        return f"<APILK(id={self.id}, name={self.name})>"
