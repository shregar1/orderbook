import collections
import ulid
#
from datetime import datetime
from typing import Any
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
from services.matchOrder import MatchOrderService
#
from start_utils import orders, trades, session_factory
#
from utilities.websocket import WebsocketUtility


class PlaceOrderService(IService):
    
    def __init__(self, urn: str = None, **kwargs) -> None:
        super().__init__(urn)
        self.urn = urn
        self.transaction_log_id = kwargs.get("transaction_log_id")
        self.websocket_utility = WebsocketUtility(urn=self.urn)

    async def __create_order(self, order: Orders) -> Orders:

        self.logger.debug("Starting database session")
        async with session_factory() as db_session:
            
            orderRepository = OrdersRepository(session=db_session)
            
            order: Orders = await orderRepository.add(
                data=order
            )

            self.logger.debug("Commiting database changes")
            await db_session.commit()
            self.logger.debug(f"Created order record for id: {order.id}")

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
    
    async def run(self, data: dict) -> dict:

        try:
            quantity = data.get('quantity')
            price = data.get('price')
            
            order_urn = f"ORDER_{ulid.new().str}"
            self.logger.debug("Creating Order")
            order: Orders = Orders(
                urn=order_urn,
                transaction_log_id=self.transaction_log_id,
                quantity=quantity,
                price=price,
                order_type_id=1 if data.get("is_buy") else 2,
                average_traded_price=0,
                traded_quantity=0,
                order_active=1,
                created_by=1,
                created_at=datetime.now()
            )
            order: Orders = await self.__create_order(order=order)
            orders[order.urn] = order.to_dict()
            self.logger.debug("Created Order")

            data = {
                "orders": orders,
                "trades": trades
            }
            
            self.logger.debug("Initialising match order service")
            match_order_service = MatchOrderService(
                urn=self.urn,
                transaction_log_id=self.transaction_log_id
            )
            self.logger.debug("Initialised match order service")

            self.logger.debug("Running match order service")
            _ = await match_order_service.run(data=data)
            self.logger.debug("Successfully executed match order service")
            
            self.logger.debug("Broadcasting order book snapshot")
            await self.__emit_order_book_snapshot(orders=orders)
            self.logger.debug("Broadcasted order book snapshot")

            order: Orders = await self.__fetch_order(order_id=order.id)
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