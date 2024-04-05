from datetime import datetime
from sqlalchemy import Column, Integer, String, DateTime, Boolean
from litestar.contrib.sqlalchemy.base import BigIntBase



class Users(BigIntBase):
    __tablename__ = 'users'


    urn = Column(String, nullable=False)
    username = Column(String(50), unique=True, nullable=False)
    email = Column(String(100), unique=True, nullable=False)
    password = Column(String(100), nullable=False)
    created_at = Column(DateTime, default=datetime.now())
    is_logged_in = Column(Boolean, default=False)
    last_login = Column(DateTime)
    is_deleted = Column(Boolean, default=False, nullable=False)
    updated_at = Column(DateTime)

    def __repr__(self):
        return f"<User(id={self.id}, username={self.username}, email={self.email})>"
