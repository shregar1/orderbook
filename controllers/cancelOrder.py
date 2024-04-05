
from decimal import Decimal
from litestar import Controller, Router, post, Request, Response
from pydantic import BaseModel
#
from abstractions.controller import IController
from constants.apiLK import APILK
#
from services.cancelOrder import CancelOrderService
#
from errors.badInputError import BadInputError

class CancelOrderCotroller(Controller, IController):
    path = "/api/orders"

    def __init__(self, owner: Router) -> None:
        super().__init__(owner)
        IController.__init__(self)
        self.api_name = APILK.PLACE_ORDER

    @post("/cancel/{order_urn:str}")
    async def delete(self, request: Request, order_urn: str) -> dict:
            
        try:

            self.urn = request.state.get("request_urn")

            self.logger.debug("Validating request")
            transaction_log = await self.validate_request(request)
            self.logger.debug("Validated request")

            data = {"order_urn": order_urn}

            self.logger.debug("Initialising modify order service")
            modify_order_service = CancelOrderService(
                urn=self.urn,
                transaction_log_id=transaction_log.id
            )
            self.logger.debug("Initialised modify order service")

            self.logger.debug("Running modify order service")
            response_payload = await modify_order_service.run(
                data=data
            )
            self.logger.debug("Successfully executed modify order service.")

            self.logger.debug("Preparing response metadata")
            http_status_code: int = 200

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