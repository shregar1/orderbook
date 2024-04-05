import ulid
#
from datetime import datetime
from typing import List
#
from abstractions.service import IService
#
#
from models.orderTransaction import OrderTransaction
from models.orders import Orders
#
from repositories.orderTransaction import OrderTransactionLogRepository
from repositories.orders import OrdersRepository
from loguru import logger
#
from start_utils import session_factory
#
from utilities.websocket import WebsocketUtility


class MatchOrderService(IService):

    def __init__(self, urn: str = None, **kwargs) -> None:
        super().__init__(urn)
        self.urn = urn
        self.transaction_log_id = kwargs.get("transaction_log_id")
        self.logger = logger
        self.websocket_utility = WebsocketUtility(urn=self.urn)

    async def __create_order_ransaction(self, order_transaction: OrderTransaction) -> OrderTransaction:

        self.logger.debug("Starting database session")
        async with session_factory() as db_session:
            
            orderTransactionRepository = OrderTransactionLogRepository(session=db_session)
            
            transaction_log: OrderTransaction = await orderTransactionRepository.add(
                data=order_transaction
            )

            self.logger.debug("Commiting database changes")
            await db_session.commit()
            self.logger.debug(f"Created order transaction record for id: {transaction_log.id}")
            return transaction_log

    async def __update_orders(self, orders: List[Orders]) -> Orders:

        self.logger.debug("Starting database session")
        async with session_factory() as db_session:
            
            orderRepository = OrdersRepository(session=db_session)
            
            orders: List[Orders] = await orderRepository.update_many(
                data=orders
            )

            self.logger.debug("Commiting database changes")
            await db_session.commit()
            self.logger.debug(f"Updated orders")
            print(orders)
            return orders

    async def __emit_trades(self, trades: dict):


        self.logger.debug("Segregated buy and sell orders.")
        
        self.logger.debug("Preparing broadcast data.")
        broadcast_data: dict = {
            "trades": [trade for trade_urn, trade in trades.items()]
        }
        self.logger.debug("Prepared broadcast data")

        self.logger.debug("Starting broadcast")
        is_broadcasted: bool =await self.websocket_utility.broadcast(
            data=broadcast_data,
            event="trades"
        )
        self.logger.debug(f"Completed broadcast with status: {is_broadcasted}")

        return is_broadcasted

    async def run(self, data: dict):
        global orders, trades

        orders = data.get("orders")
        trades = data.get("trades")

        buy_orders = [order for order_urn, order in orders.items() if order["order_type_id"] == 1 and order["order_active"]]
        sell_orders = [order for order_urn, order in orders.items() if order["order_type_id"] == 2 and order["order_active"]]
        
        self.logger.debug("Matching orders.")
        for buy_order in buy_orders:

            for sell_order in sell_orders:

                if buy_order['price'] >= sell_order['price']:

                    matched_quantity = min(buy_order['quantity'], sell_order['quantity'])

                    if matched_quantity > 0:

                        trade_price = (buy_order['price'] + sell_order['price']) / 2  # Assuming average price for simplicity
                        trade = OrderTransaction(
                            urn=f"ORDER_TRANSACTION_{ulid.new().str}",
                            bid_order_id=buy_order.get("id"),
                            ask_order_id=sell_order.get("id"),
                            quantity=matched_quantity,
                            execution_timestamp=datetime.now(),
                            price=trade_price,
                            created_by=1,
                            created_at=datetime.now(),
                            updated_at=datetime.now()
                        )

                        self.logger.debug("Creating trade.")
                        trade = await self.__create_order_ransaction(order_transaction=trade)
                        self.logger.debug("Created trade.")

                        trades[trade.urn] = trade.to_dict()

                        self.logger.debug("Broadcasting trades")
                        await self.__emit_trades(trades=trades)
                        self.logger.debug("Broadcasted trades")

                        self.logger.debug("Preparing order updates.")
                        buy_order['traded_quantity'] += matched_quantity
                        sell_order['traded_quantity'] += matched_quantity
                        buy_order['average_traded_price'] = (buy_order['average_traded_price'] * (buy_order['traded_quantity'] - matched_quantity) + trade_price * matched_quantity) / buy_order['traded_quantity']
                        sell_order['average_traded_price'] = (sell_order['average_traded_price'] * (sell_order['traded_quantity'] - matched_quantity) + trade_price * matched_quantity) / sell_order['traded_quantity']
                        buy_order['quantity'] -= matched_quantity
                        sell_order['quantity'] -= matched_quantity
                        if buy_order['quantity'] == 0:
                            buy_order['order_active'] = 0
                        if sell_order['quantity'] == 0:
                            sell_order['order_active'] = 0
                        buy_order = Orders(
                            id=buy_order["id"],
                            traded_quantity=buy_order['traded_quantity'],
                            average_traded_price=buy_order["average_traded_price"],
                            quantity=buy_order["quantity"],
                            order_active=buy_order["order_active"],
                            updated_at=datetime.now()
                        )
                        sell_order = Orders(
                            id=sell_order["id"],
                            traded_quantity=sell_order['traded_quantity'],
                            average_traded_price=sell_order["average_traded_price"],
                            quantity=sell_order["quantity"],
                            order_active=sell_order["order_active"],
                            updated_at=datetime.now()
                        )
                        self.logger.debug("Prepared order updates.")

                        self.logger.debug("Updating Orders")
                        await self.__update_orders(orders=[buy_order, sell_order])
                        self.logger.debug("Updated Orders")

        self.logger.debug("Filtering Orders.")
        orders = {order_urn: order for order_urn, order in orders.items() if order['order_active']}
        self.logger.debug("Filtered Orders.")

        return None