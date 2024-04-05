
from decimal import Decimal
from litestar import Controller, Router, get, Request, Response
from pydantic import BaseModel
#
from abstractions.controller import IController
from constants.apiLK import APILK
#
from services.cancelOrder import CancelOrderService
#
from errors.badInputError import BadInputError
#
from start_utils import orders, trades


class FetchOrdersCotroller(Controller, IController):
    path = "/api/orders"

    def __init__(self, owner: Router) -> None:
        super().__init__(owner)
        IController.__init__(self)
        self.api_name = APILK.PLACE_ORDER

    @get("/fetch/{order_urn: str}")
    async def delete(self, request: Request, order_urn: str) -> dict:
            
        try:

            self.urn = request.state.get("request_urn")

            self.logger.debug("Validating request")
            transaction_log = await self.validate_request(request)
            self.logger.debug("Validated request")

            order = orders.get(order_urn)

            http_status_code = 200
            
            return Response(
                content=order,
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
        
        except Exception as err:

            self.logger.error(f"{err.__name__} occured while modifying order: {err}")
            response_payload = {
                "detail": "Internal server error",
                "extra": {
                    "message": "Internal server error",
                    "key": "internal_server_error"
                },
                "status_code": 500
            }

            return Response(
                content=response_payload,
                status_code=500
            )