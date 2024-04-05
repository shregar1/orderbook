import ulid
#
from abc import ABC
from datetime import datetime
from loguru import logger
from litestar import Request
from repositories.transactionsLog import TransactionsLogRepository
from repositories.apiLK import APILKRepository
from repositories.httpMethodLK import HTTPMethodLKRepository
#
from models.apiLK import APILK
from models.httpMethodLK import HTTPMethodLK
from models.transactionsLog import TransactionsLog
#
from start_utils import session_factory

class IController(ABC):

    def __init__(self, urn: str = None) -> None:
        self.urn = urn
        self.logger = logger

    async def __create_transaction_log(self, urn: str, api_name: str, request_payload: dict, request_headers: dict):

        self.logger.debug("Starting database session")
        async with session_factory() as db_session:
            
            apiLKRepository = APILKRepository(session=db_session)
            transactionLogRepository = TransactionsLogRepository(session=db_session)
            api: APILK = await apiLKRepository.get_one(name=api_name)
            
            transaction_log: TransactionsLog = await transactionLogRepository.add(
                    TransactionsLog(
                        urn = urn,
                        reference_urn = ulid.new().str,
                        api_id = api.id,
                        request_payload=request_payload,
                        request_headers=request_headers,
                        request_timestamp=datetime.now(),
                        created_by = 1,
                        created_at = datetime.now()
                )
            )

            self.logger.debug("Commiting database changes")
            await db_session.commit()
            self.logger.debug(f"Created transaction log record for id: {transaction_log.id}")
            return transaction_log

    async def validate_request(self, request: Request) -> TransactionsLog:
        request_payload: dict = await request.json()
        request_headers: dict = request.headers.dict()
        transaction_log: TransactionsLog = await self.__create_transaction_log(
            urn=self.urn,
            api_name=self.api_name,
            request_payload=request_payload,
            request_headers=request_headers
        )
        return transaction_log         

    async def update_transaction_log(
        self, 
        transaction_log_id: int, 
        response_payload: dict, 
        response_headers: dict, 
        http_status_code: int
    ) -> None:
        self.logger.debug("Updating transaction log")
        try:

            async with session_factory() as db_session:
                transactionLogRepository = TransactionsLogRepository(session=db_session)
                transaction_log: TransactionsLog = await transactionLogRepository.update(
                    data=TransactionsLog(
                        id=transaction_log_id,
                        response_payload=response_payload, 
                        response_headers=response_headers,
                        response_timestamp=datetime.now(),
                        http_status_code=http_status_code,
                        updated_at=datetime.now()
                    )
                )
                self.logger.debug("Commiting database changes")
                await db_session.commit()
                self.logger.debug(f"Updated transaction log record with id: {transaction_log.id}")
                return transaction_log
            
        except Exception as err:
            self.logger.error(f"Error occured while updating transaction log: {err}")
            raise err



