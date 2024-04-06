from litestar import Controller, Router, get, Request, Response
#
from abstractions.controller import IController
#
from constants.apiLK import APILK
from constants.apiStatus import APIStatus
#
from dtos.response.base import BaseResponseDTO
#
from errors.badInputError import BadInputError
#
from services.fetchOrder import FetchOrderService
#
from start_utils import orders


class FetchOrdersCotroller(Controller, IController):
    path = "/api/orders"

    def __init__(self, owner: Router) -> None:
        super().__init__(owner)
        IController.__init__(self)
        self.api_name = APILK.FETCH_ORDER

    @get("/fetch/{order_urn: str}")
    async def delete(self, request: Request, order_urn: str) -> dict:
            
        try:

            self.urn = request.state.get("request_urn")

            self.logger.debug("Validating request")
            transaction_log = await self.validate_request(request)
            self.logger.debug("Validated request")

            data = {"order_urn": order_urn}

            self.logger.debug("Initialising fetch order service")
            modify_order_service = FetchOrderService(
                urn=self.urn,
                transaction_log_id=transaction_log.id
            )
            self.logger.debug("Initialised fetch order service")

            self.logger.debug("Running fetch order service")
            response_payload = await modify_order_service.run(
                data=data
            )
            self.logger.debug("Successfully executed fetch order service.")

            self.logger.debug("Preparing response metadata")
            http_status_code: int = 200
            response_dto = BaseResponseDTO(
                transaction_urn=self.urn,
                status=APIStatus.SUCCESS,
                response_message="Successfully fetched order.",
                response_key="success_order_fetched",
                data=response_payload,
                error=None
            )
        
        except BadInputError as err:

            self.logger.error(f"{BadInputError.__name__} occured while fetching order.")
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
                response_message="Failed to fetch order.",
                response_key="bad_input_error",
                error=error_payload
            )
        
        except Exception as err:
            self.logger.error(f"{err.__name__} occured while fetching order")

            self.logger.debug("Preparing response metadata")
            http_status_code: int = 500     
            response_dto = BaseResponseDTO(
                transaction_urn=self.urn,
                status=APIStatus.FAILED,
                response_message="Failed to fetch order.",
                response_key="internal_server_error"
            )

        self.logger.debug("Updating transaction log")
        await self.update_transaction_log(
            transaction_log_id=transaction_log.id,
            response_payload=response_dto.__dict__,
            response_headers={},
            http_status_code=http_status_code
        )

        return Response(
            content=response_dto.__dict__,
            status_code=http_status_code
        )   