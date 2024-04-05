from decimal import Decimal
from pydantic import BaseModel

class PlaceOrderRequestDTO(BaseModel):

    quantity: int
    price: Decimal
    is_buy: bool