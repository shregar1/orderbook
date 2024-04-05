from abstractions.utility import IUtility
#
from litestar import WebSocket
from loguru import logger


class WebsocketUtility(IUtility):
    
    def __init__(self, urn: str = None) -> None:
        super().__init__(urn)
        self.urn = urn
        self.logger = logger

    async def broadcast(self, data: dict, event: str) -> bool:
        try:
            from start_utils import websocket_sessions
            for websocket_session in websocket_sessions:
                if websocket_session:
                    websocket_session: WebSocket = websocket_session
                    event_payload: dict = {
                        "event": event,
                        "data": data
                    }
                    await websocket_session.send_json(event_payload)
            return True
        except Exception as err:
            self.logger.debug(f"An error occured while sending data over websocket: {err}")
            return False
