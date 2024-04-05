from datetime import datetime
from decimal import Decimal
from pydantic import BaseModel
from typing import Optional


class OrderTransaction(BaseModel):
    urn: str
    bid_order_id: int
    ask_order_id: int
    quantity: int
    price: Decimal
    execution_timestamp: datetime
    created_by: int
    created_at: datetime
    updated_at: Optional[datetime]