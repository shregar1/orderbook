from typing import Coroutine
import asyncio
import ulid
from datetime import datetime
from litestar import Request
from contextlib import asynccontextmanager
from litestar.datastructures import MutableScopeHeaders
from litestar.middleware.base import MiddlewareProtocol
from litestar.types import ASGIApp, Receive, Scope, Send
#
from repositories.transactionsLog import TransactionsLogRepository
from repositories.apiLK import APILKRepository
from repositories.httpMethodLK import HTTPMethodLKRepository
from loguru import logger
#
from models.transactionsLog import TransactionsLog
#
from start_utils import session_factory


class TransactionLogMiddleware(MiddlewareProtocol):

    def __init__(self, app: ASGIApp) -> None:
        super().__init__(app)
        self.app = app
        self.logger = logger

    async def __call__(self, scope: Scope, receive: Receive, send: Send) -> None:
        if scope["type"] == "http":
            try:
                request = Request(scope)
                request_urn = request.state.get("request_urn")
                transaction_log = await self.create_transaction_log(urn=request_urn, method=request.method, endpoint=scope.get("path"))
                
                await self.app(scope, receive, send)
            except Exception as err:
                print(err)
                raise err
        else:
            await self.app(scope, receive, send)