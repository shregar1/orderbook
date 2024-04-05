from typing import Any
from litestar.contrib.sqlalchemy.repository import SQLAlchemyAsyncRepository
#
from models.httpMethodLK import HTTPMethodLK

class HTTPMethodLKRepository(SQLAlchemyAsyncRepository):
    model_type = HTTPMethodLK