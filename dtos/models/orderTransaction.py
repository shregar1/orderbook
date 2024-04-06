from decimal import Decimal


class OrderTransactionDTO(dict):

    urn: str
    bid_order_urn: int
    ask_order_urn: int
    quantity: int
    price: Decimal
    execution_timestamp: str
    created_by: int
    created_at: str