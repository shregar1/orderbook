from typing import Any
from litestar.contrib.sqlalchemy.repository import SQLAlchemyAsyncRepository
#
from models.orders import Orders


class OrdersRepository(SQLAlchemyAsyncRepository):
    model_type = Orders
