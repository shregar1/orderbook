
from litestar import Controller, Router, post, Request, Response
from litestar.dto import DataclassDTO, DTOConfig
#
from abstractions.controller import IController
#
from constants.apiLK import APILK
from constants.apiStatus import APIStatus
#
from dtos.response.base import BaseResponseDTO
from dtos.request.placeOder import PlaceOrderRequestDTO
#
from errors.badInputError import BadInputError
#
from services.placeOrder import PlaceOrderService


class PlaceOrderCotroller(Controller, IController):
    path = "/api/orders"

    def __init__(self, owner: Router) -> None:
        super().__init__(owner)
        IController.__init__(self)
        self.api_name = APILK.PLACE_ORDER

    @post("/create")
    async def post(self, request: Request, data: PlaceOrderRequestDTO) -> BaseResponseDTO:
            
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
            response_dto = BaseResponseDTO(
                transaction_urn=self.urn,
                status=APIStatus.SUCCESS,
                response_message="Successfully placed order.",
                response_key="success_order_create",
                data=response_payload,
                error=None
            )

        except BadInputError as err:

            self.logger.error(f"{BadInputError.__name__} occured while placing order.")
            error_payload = {
                "detail": err.response_message,
                "extra": {
                    "message": err.response_message,
                    "key": err.response_key
                },
                "status_code": err.status_code
            }

            http_status_code: int = 400
            response_dto = BaseResponseDTO(
                transaction_urn=self.urn,
                status=APIStatus.FAILED,
                response_message="Failed to placed order.",
                response_key="bad_input_error",
                error=error_payload
            )
        
        except Exception as err:
            self.logger.error(f"{err.__name__} occured while placing order")
            
            http_status_code: int = 500
            response_dto = BaseResponseDTO(
                transaction_urn=self.urn,
                status=APIStatus.FAILED,
                response_message="Failed to placed order.",
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