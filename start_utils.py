import collections
from sqlalchemy.ext.asyncio import async_sessionmaker, create_async_engine

orders = collections.defaultdict(dict)
trades = collections.defaultdict(dict)


engine = create_async_engine(
    "sqlite+aiosqlite:///orderbook.sqlite",
    future=True,
)
session_factory = async_sessionmaker(engine, expire_on_commit=False)

from litestar import WebSocket, websocket

websocket_sessions = []

@websocket("/connect")
async def websocket_handler(socket: WebSocket) -> None:
    print("Connection accepted")
    await socket.accept()
    global websocket_sessions
    websocket_sessions.append(socket)
    print(websocket_sessions)
    print(await socket.receive())
    print(socket)
    await socket.send_json(data={"message": "connected"})