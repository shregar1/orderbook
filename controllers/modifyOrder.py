
from litestar import Controller, Router, put, Request, Response
#
from abstractions.controller import IController
#
from constants.apiLK import APILK
from constants.apiStatus import APIStatus
#
from dtos.response.base import BaseResponseDTO
from dtos.request.modifyOrder import ModifyOrderRequestDTO
#
from errors.badInputError import BadInputError
#
from services.modifyOrder import ModifyOrderService


class ModifyOrderCotroller(Controller, IController):
    path = "/api/orders"

    def __init__(self, owner: Router) -> None:
        super().__init__(owner)
        IController.__init__(self)
        self.api_name = APILK.PLACE_ORDER

    @put("/update/{order_urn:str}")
    async def put(self, request: Request, order_urn: str, data: ModifyOrderRequestDTO) -> BaseResponseDTO:
            
        try:

            self.urn = request.state.get("request_urn")

            self.logger.debug("Validating request")
            transaction_log = await self.validate_request(request)
            self.logger.debug("Validated request")

            data = data.model_dump()
            data.update({"order_urn": order_urn})

            self.logger.debug("Initialising modify order service")
            modify_order_service = ModifyOrderService(
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
            response_dto = BaseResponseDTO(
                transaction_urn=self.urn,
                status=APIStatus.SUCCESS,
                response_message="Successfully modified order.",
                response_key="success_order_update",
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

            self.logger.debug("Preparing response metadata")
            http_status_code: int = 400
            response_dto = BaseResponseDTO(
                transaction_urn=self.urn,
                status=APIStatus.FAILED,
                response_message="Failed to modify order.",
                response_key="bad_input_error",
                error=error_payload
            )
        
        except Exception as err:
            self.logger.error(f"{err.__name__} occured while placing order")

            self.logger.debug("Preparing response metadata")  
            http_status_code: int = 500
            response_dto = BaseResponseDTO(
                transaction_urn=self.urn,
                status=APIStatus.FAILED,
                response_message="Failed to modify order.",
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