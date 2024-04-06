from abstractions.service import IService
#
from constants.orderType import OrderType
#
from dtos.models.order import OrderDTO
#
from start_utils import orders


class FetchAllOrdersService(IService):
    
    def __init__(self, urn: str = None, **kwargs) -> None:
        super().__init__(urn)
        self.urn = urn
        self.transaction_log_id = kwargs.get("transaction_log_id")

    
    async def run(self, data: dict) -> OrderDTO:
        try:
            
            self.logger.debug("Fetching active Orders")
            active_orders: list = [order for order_urn, order in orders.items() if order["order_active"]]
            self.logger.debug("Fetching active Orders")
    
            return [
                OrderDTO(
                urn=order.get("urn"),
                quantity=order.get("quantity"),
                price=order.get("price"),
                order_type=OrderType.BUY if order.get("order_type_id") == 1 else OrderType.SELL,
                average_traded_price=order.get("average_traded_price"),
                traded_quantity=order.get("traded_quantity"),
                order_active=True if order.get("order_active") else False,
                created_at=str(order.get("created_at"))
            )
            for order in active_orders
            ]

        except Exception as err:

            self.logger.error(f"An error occured while placing order: {err}")
            raise err
