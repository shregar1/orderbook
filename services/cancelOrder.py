import ulid
#
from http import HTTPStatus
from typing import Any, List
#
from abstractions.service import IService
#
from dtos.response.placeOrder import PlaceOrderResponseDTO
#
from errors.badInputError import BadInputError
#
from services.matchOrder import MatchOrderService
#
from repositories.orders import OrdersRepository
from models.orders import Orders
#
from start_utils import orders, trades, session_factory
#
from utilities.websocket import WebsocketUtility


class CancelOrderService(IService):
    
    def __init__(self, urn: str = None, **kwargs) -> None:
        super().__init__(urn)
        self.urn = urn
        self.transaction_log_id = kwargs.get("transaction_log_id")
        self.websocket_utility = WebsocketUtility(urn=self.urn)

    async def __fetch_order(self, order_id: int) -> Orders:

        self.logger.debug("Starting database session")
        async with session_factory() as db_session:

            self.logger.debug("Initialising Order Repository.")
            orderRepository = OrdersRepository(session=db_session)
            self.logger.debug("Initialised Order Repository.")

            self.logger.debug(f"Fetching order with id: {order_id}")
            order: Orders = await orderRepository.get(item_id=order_id)
            self.logger.debug(f"Fetched order with id: {order_id}")

            return order

    async def __update_order(self, data: dict) -> Orders:

        self.logger.debug("Starting database session")
        async with session_factory() as db_session:

            self.logger.debug("Initialising Order Repository.")
            orderRepository = OrdersRepository(session=db_session)
            self.logger.debug("Initialised Order Repository.")

            self.logger.debug(f"Fetching order with urn: {data.get('order_urn')}")
            order: Orders = await orderRepository.get_one_or_none(urn=data.get("order_urn"))

            if not order:
                raise BadInputError(
                    response_message="Invalid oreder URN. Order not found.",
                    response_key="order_urn",
                    status_code=HTTPStatus.BAD_REQUEST
                )

            self.logger.debug("Updating order price")
            order.order_active = 0
            order: Orders = await orderRepository.update(
                data=order
            )
            self.logger.debug("Updated oredr price")

            self.logger.debug("Commiting database changes")
            await db_session.commit()
            self.logger.debug(f"Updated order")

            return order
    
    async def __emit_order_book_snapshot(self, orders: dict):

        buy_orders = []
        sell_orders = []

        self.logger.debug("Segregating buy and sell orders.")
        for order_urn, order in orders.items():
            if order.get("order_type_id") == 1:
                 buy_orders.append(order)
            if order.get("order_type_id") == 2:
                sell_orders.append(order)

        self.logger.debug("Segregated buy and sell orders.")
        
        self.logger.debug("Preparing broadcast data.")
        broadcast_data: dict = {
            "buy_orders": buy_orders,
            "sell_orders": sell_orders
        }
        self.logger.debug("Prepared broadcast data")

        self.logger.debug("Starting broadcast")
        is_broadcasted: bool =await self.websocket_utility.broadcast(
            data=broadcast_data,
            event="orderBook"
        )
        self.logger.debug(f"Completed broadcast with status: {is_broadcasted}")

        return is_broadcasted
    
    async def run(self, data: dict) -> PlaceOrderResponseDTO:
        try:
            
            self.logger.debug("Updating Order")
            order: Orders = await self.__update_order(data=data)
            orders[order.urn] = order.to_dict()
            self.logger.debug("Updated Order")

            data = {
                "orders": orders,
                "trades": trades
            }

            # Match orders after placing a new order
            
            self.logger.debug("Broadcasting order book snapshot")
            await self.__emit_order_book_snapshot(orders=orders)
            self.logger.debug("Broadcasted order book snapshot")

            order: Orders = await self.__fetch_order(order_id=order.id)
            order: dict = order.to_dict()
            order["created_at"] = str(order["created_at"])
            order["updated_at"] = str(order["updated_at"])
    
            return order

        except Exception as err:

            self.logger.error(f"An error occured while placing order: {err}")
            raise err