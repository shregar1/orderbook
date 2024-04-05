from datetime import datetime
from decimal import Decimal
from pydantic import BaseModel
from typing import Optional


class Orders(BaseModel):

    urn: str
    transaction_log_id: int
    quantity: int
    price: Decimal
    order_type_id: int
    average_traded_price: Decimal
    traded_quantity: int
    order_active: bool
    created_by: int
    created_at: datetime
    updated_at: Optional[datetime] = None
