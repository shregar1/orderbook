from typing import Union, Optional
from dataclasses import dataclass


@dataclass
class BaseResponseDTO:

    transaction_urn: str
    status: str
    response_message: str
    response_key: str
    data: Optional[Union[dict, list]] = None
    error: Optional[Union[dict, list]] = None

    