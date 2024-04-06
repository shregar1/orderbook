from decimal import Decimal


class OrderDTO(dict):

    urn: str
    quantity: int
    price: Decimal
    order_type: str
    average_traded_price: Decimal
    traded_quantity: int
    order_active: bool
    created_at: str