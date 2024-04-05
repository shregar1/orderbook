from typing import Any
from litestar.contrib.sqlalchemy.repository import SQLAlchemyAsyncRepository
#
from models.transactionsLog import TransactionsLog

class TransactionsLogRepository(SQLAlchemyAsyncRepository):
    model_type = TransactionsLog
