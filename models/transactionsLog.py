from datetime import datetime
from sqlalchemy import Column, Integer, String, JSON, DateTime, ForeignKey
from litestar.contrib.sqlalchemy.base import BigIntBase
#
from models.users import Users
from models.apiLK import APILK




class TransactionsLog(BigIntBase):
    __tablename__ = 'TransactionLog'



    urn = Column(String(255), nullable=False)
    reference_urn = Column(String(255), nullable=False)
    api_id = Column(Integer, ForeignKey(APILK.id))
    request_payload = Column(JSON, nullable=True)
    request_headers = Column(JSON, nullable=True)
    request_timestamp = Column(DateTime, nullable=True)
    response_payload = Column(JSON, nullable=True)
    response_headers = Column(JSON, nullable=True)
    response_timestamp = Column(DateTime, nullable=True)
    http_status_code = Column(Integer, nullable=True)
    created_by = Column(Integer, ForeignKey(Users.id))
    created_at = Column(DateTime, default=datetime.now())
    updated_at = Column(DateTime)

    def __repr__(self):
        return f"<TransactionsLog(id={self.id}, urn={self.urn}, reference_urn={self.reference_urn})>"
