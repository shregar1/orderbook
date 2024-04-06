
from litestar import Controller, Router, post, Request, Response
#
from abstractions.controller import IController
#
from constants.apiLK import APILK
from constants.apiStatus import APIStatus
#
from dtos.response.base import BaseResponseDTO
#
from services.cancelOrder import CancelOrderService
#
from errors.badInputError import BadInputError

class CancelOrderCotroller(Controller, IController):
    path = "/api/orders"

    def __init__(self, owner: Router) -> None:
        super().__init__(owner)
        IController.__init__(self)
        self.api_name = APILK.CANCEL_ORDER

    @post("/cancel/{order_urn:str}")
    async def delete(self, request: Request, order_urn: str) -> dict:
            
        try:

            self.urn = request.state.get("request_urn")

            self.logger.debug("Validating request")
            transaction_log = await self.validate_request(request)
            self.logger.debug("Validated request")

            data = {"order_urn": order_urn}

            self.logger.debug("Initialising cancel order service")
            modify_order_service = CancelOrderService(
                urn=self.urn,
                transaction_log_id=transaction_log.id
            )
            self.logger.debug("Initialised cancel order service")

            self.logger.debug("Running cancel order service")
            response_payload = await modify_order_service.run(
                data=data
            )
            self.logger.debug("Successfully executed cancel order service.")

            self.logger.debug("Preparing response metadata")
            http_status_code: int = 200
            response_dto = BaseResponseDTO(
                transaction_urn=self.urn,
                status=APIStatus.SUCCESS,
                response_message="Successfully cancelled order.",
                response_key="success_order_update",
                data=response_payload,
                error=None
            )
        
        except BadInputError as err:

            self.logger.error(f"{BadInputError.__name__} occured while removing order.")
            error_payload = {
                "detail": err.response_message,
                "extra": {
                    "message": err.response_message,
                    "key": err.response_key
                },
                "status_code": err.status_code
            }

            self.logger.debug("Preparing response metadata")
            http_status_code: int = 400
            response_dto = BaseResponseDTO(
                transaction_urn=self.urn,
                status=APIStatus.FAILED,
                response_message="Failed to cancel order.",
                response_key="bad_input_error",
                error=error_payload
            )
        
        except Exception as err:
            self.logger.error(f"{err.__name__} occured while removing order")

            self.logger.debug("Preparing response metadata")
            http_status_code: int = 500       
            response_dto = BaseResponseDTO(
                transaction_urn=self.urn,
                status=APIStatus.FAILED,
                response_message="Failed to cancel order.",
                response_key="internal_server_error"
            )

        self.logger.debug("Updating transaction log")
        await self.update_transaction_log(
            transaction_log_id=transaction_log.id,
            response_payload=response_dto.__dict__,
            response_headers={},
            http_status_code=http_status_code
        )
        self.logger.debug("Updated transaction log")

        return Response(
            content=response_dto.__dict__,
            status_code=http_status_code
        ) 