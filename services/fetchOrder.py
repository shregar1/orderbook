import ulid
#
from http import HTTPStatus
#
from abstractions.service import IService
#
from constants.orderType import OrderType
#
from dtos.models.order import OrderDTO
#
from models.orders import Orders
#
from repositories.orders import OrdersRepository
#
from start_utils import session_factory
#
from utilities.websocket import WebsocketUtility


class FetchOrderService(IService):
    
    def __init__(self, urn: str = None, **kwargs) -> None:
        super().__init__(urn)
        self.urn = urn
        self.transaction_log_id = kwargs.get("transaction_log_id")
        self.websocket_utility = WebsocketUtility(urn=self.urn)

    async def __fetch_order(self, order_urn: str) -> Orders:

        self.logger.debug("Starting database session")
        async with session_factory() as db_session:

            self.logger.debug("Initialising Order Repository.")
            orderRepository = OrdersRepository(session=db_session)
            self.logger.debug("Initialised Order Repository.")

            self.logger.debug(f"Fetching order with id: {order_urn}")
            order: Orders = await orderRepository.get_one_or_none(urn=order_urn)
            self.logger.debug(f"Fetched order with id: {order_urn}")

            return order

    
    async def run(self, data: dict) -> OrderDTO:
        try:
            
            self.logger.debug("Fetching Order")
            order: Orders = await self.__fetch_order(order_urn=data.get("order_urn"))
            self.logger.debug("Fetching Order")
    
            return OrderDTO(
                urn=order.urn,
                quantity=order.quantity,
                price=order.price,
                order_type=OrderType.BUY if order.order_type_id == 1 else OrderType.SELL,
                average_traded_price=order.average_traded_price,
                traded_quantity=order.traded_quantity,
                order_active=True if order.order_active else False,
                created_at=str(order.created_at)
            )

        except Exception as err:

            self.logger.error(f"An error occured while placing order: {err}")
            raise err