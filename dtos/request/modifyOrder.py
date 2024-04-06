from decimal import Decimal
from pydantic import BaseModel


class ModifyOrderRequestDTO(BaseModel):

    price: Decimal
