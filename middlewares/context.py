import ulid
from datetime import datetime
from litestar import Request
from litestar.datastructures import MutableScopeHeaders
from litestar.middleware.base import MiddlewareProtocol
from litestar.types import ASGIApp, Receive, Scope, Send, Message
from loguru import logger


class RequestContextMiddleware(MiddlewareProtocol):
    def __init__(self, app: ASGIApp) -> None:
        super().__init__(app)
        self.app = app
        self.logger = logger

    async def __call__(self, scope: Scope, receive: Receive, send: Send) -> None:
        if scope["type"] == "http":
            request = Request(scope)
            self.logger.debug("Generating reuest urn")
            request_urn: str = ulid.new().str
            request.state.setdefault("request_urn", request_urn)
            self.logger.debug("Generated request urn", request.state.get("request_urn2"))
            await self.app(scope, receive, send)
        else:
            await self.app(scope, receive, send)