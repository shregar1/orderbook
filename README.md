# orderbook
orderbook

# start server
python3 app.py

# connect websocket
websocket.py

#Curls

## Create Order:
curl --location 'http://127.0.0.1:8000/api/orders/create' \
--header 'Content-Type: application/json' \
--data '{
    "quantity": 100,
    "price": 99.3,
    "is_buy": true
}'

## Modify Oder:

curl --location --request PUT 'http://127.0.0.1:8000/api/orders/update/<order_urn>' \
--header 'Content-Type: application/json' \
--data '{
    "price": 98.0
}'

# Cancel Order:
curl --location 'http://127.0.0.1:8000/api/orders/cancel/<order_urn>' \
--header 'Content-Type: application/json' \
--data '{}'

# Fetch All Order:
curl --location 'http://127.0.0.1:8000/api/orders/fetchall'

# Fetch Order:
curl --location --globoff 'http://127.0.0.1:8000/api/orders/fetch/<order_urn>'