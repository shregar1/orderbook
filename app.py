
from __future__ import annotations
#
import ulid
import uvicorn
#
from litestar import Litestar, WebSocket, websocket, get
from litestar.handlers.websocket_handlers import WebsocketRouteHandler
from litestar.contrib.sqlalchemy.base import BigIntBase
from litestar.contrib.sqlalchemy.plugins import AsyncSessionConfig, SQLAlchemyAsyncConfig, SQLAlchemyInitPlugin
from litestar.controller import Controller
from litestar.middleware.base import MiddlewareProtocol
from litestar.types import ASGIApp, Receive, Scope, Send
from loguru import logger
from litestar.datastructures import Headers, State
#
from middlewares.context import RequestContextMiddleware
#
from controllers.placeOrder import PlaceOrderCotroller
from controllers.modifyOrder import ModifyOrderCotroller
from controllers.cancelOrder import CancelOrderCotroller
from controllers.fetchALLOrders import FetchAllOrdersCotroller
from controllers.fetchOrder import FetchOrdersCotroller
#
from models.apiLK import APILK
from models.httpMethodLK import HTTPMethodLK
from models.orders import Orders
from models.orderTypeLK import OrderTypeLK
from models.orderTransaction import OrderTransaction
from models.transactionsLog import TransactionsLog
from models.users import Users
#
from start_utils import websocket_handler

session_config = AsyncSessionConfig(expire_on_commit=False)
sqlalchemy_config = SQLAlchemyAsyncConfig(
    connection_string="sqlite+aiosqlite:///orderbook.sqlite", session_config=session_config
)  # Create 'db_session' dependency.
sqlalchemy_plugin = SQLAlchemyInitPlugin(config=sqlalchemy_config)


async def on_startup() -> None:
    """Initializes the database."""
    async with sqlalchemy_config.get_engine().begin() as conn:
        await conn.run_sync(BigIntBase.metadata.create_all)

async def before_request() -> None:
    print("Inside before request")




@get("/hello")
async def index() -> dict[str, str]:
    from start_utils import websocket_sessions
    print(websocket_sessions)
    try:
        for websocket_session in websocket_sessions:
            print(websocket_session)
            await websocket_session.send_json({"message": "connection alive"})
        return {"message": "connection alive"}, 200
    except Exception as err:
        print(err)
        raise err

middleware = []

logger.debug(f"Registering {RequestContextMiddleware.__name__} middleware.")
middleware.append(RequestContextMiddleware)
logger.debug(f"Registered {RequestContextMiddleware.__name__} middleware.")

route_handlers = [index]

logger.debug(f"Registering {websocket_handler} websocket controller.")
route_handlers.append(websocket_handler)
logger.debug(f"Registered {websocket_handler} websocket controller.")

logger.debug(f"Registering {PlaceOrderCotroller.__name__} controller.")
route_handlers.append(PlaceOrderCotroller)
logger.debug(f"Registered {PlaceOrderCotroller.__name__} controller.")

logger.debug(f"Registering {ModifyOrderCotroller.__name__} controller.")
route_handlers.append(ModifyOrderCotroller)
logger.debug(f"Registered {ModifyOrderCotroller.__name__} controller.")

logger.debug(f"Registering {CancelOrderCotroller.__name__} controller.")
route_handlers.append(CancelOrderCotroller)
logger.debug(f"Registered {CancelOrderCotroller.__name__} controller.")

logger.debug(f"Registering {FetchAllOrdersCotroller.__name__} controller.")
route_handlers.append(FetchAllOrdersCotroller)
logger.debug(f"Registered {FetchAllOrdersCotroller.__name__} controller.")

logger.debug(f"Registering {FetchOrdersCotroller.__name__} controller.")
route_handlers.append(FetchOrdersCotroller)
logger.debug(f"Registered {FetchOrdersCotroller.__name__} controller.")


app = Litestar(
    route_handlers=route_handlers,
    middleware=middleware,
    on_startup=[on_startup],
    plugins=[SQLAlchemyInitPlugin(config=sqlalchemy_config)],
)


if __name__ == '__main__':
    uvicorn.run("app:app", port=8000, host='127.0.0.1', reload=True)