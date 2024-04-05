
from decimal import Decimal
from litestar import Controller, Router, post, Request, Response
from pydantic import BaseModel
#
from abstractions.controller import IController
from constants.apiLK import APILK
#
from errors.badInputError import BadInputError
#
from services.placeOrder import PlaceOrderService


class PlaceOrderCotroller(Controller, IController):
    path = "/api/orders"
    
    class Order(BaseModel):
        quantity: int
        price: Decimal
        is_buy: bool

    def __init__(self, owner: Router) -> None:
        super().__init__(owner)
        IController.__init__(self)
        self.api_name = APILK.PLACE_ORDER

    @post("/create")
    async def post(self, request: Request, data: Order) -> dict:
            
        try:

            self.urn = request.state.get("request_urn")
            transaction_log = await self.validate_request(request)

            self.logger.debug("Initialising place order service")
            place_order_service = PlaceOrderService(
                urn=self.urn,
                transaction_log_id=transaction_log.id
            )
            self.logger.debug("Initialised place order service")

            self.logger.debug("Running place order service")
            response_payload = await place_order_service.run(data=data.model_dump())
            self.logger.debug("Successfully executed place order service.")

            self.logger.debug("Preparing response metadata")
            http_status_code: int = 201

            self.logger.debug("Updating transaction log")
            await self.update_transaction_log(
                transaction_log_id=transaction_log.id,
                response_payload=response_payload,
                response_headers={},
                http_status_code=http_status_code
            )

            return Response(
                content=response_payload,
                status_code=http_status_code
            )

        except BadInputError as err:

            self.logger.error(f"{BadInputError.__name__} occured while modifying order.")
            response_payload = {
                "detail": err.response_message,
                "extra": {
                    "message": err.response_message,
                    "key": err.response_key
                },
                "status_code": err.status_code
            }

            return Response(
                content=response_payload,
                status_code=err.status_code
            )