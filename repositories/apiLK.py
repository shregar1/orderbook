from typing import Any
from litestar.contrib.sqlalchemy.repository import SQLAlchemyAsyncRepository
#
from models.apiLK import APILK

class APILKRepository(SQLAlchemyAsyncRepository):
    model_type = APILK
