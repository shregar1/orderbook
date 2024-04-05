from typing import Any
from litestar.contrib.sqlalchemy.repository import SQLAlchemyAsyncRepository
#
from models.orderTransaction import OrderTransaction

class OrderTransactionLogRepository(SQLAlchemyAsyncRepository):
    model_type = OrderTransaction
