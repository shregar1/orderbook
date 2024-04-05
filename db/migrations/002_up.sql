

INSERT INTO users (urn, username, email, password, created_at, is_logged_in, is_deleted) 
VALUES ('01HTF7XVWH7M2DMXQM62Y9GNFV', 'admin', 'admin@example.com', 'helloworld', CURRENT_TIMESTAMP, 0, false);

INSERT INTO http_method_lk (name, code, description, created_by, created_at) 
VALUES 
    ('GET', 'GET', 'Retrieve data', 1, CURRENT_TIMESTAMP),
    ('POST', 'POST', 'Create new data', 1, CURRENT_TIMESTAMP),
    ('PUT', 'PUT', 'Update existing data', 1, CURRENT_TIMESTAMP),
    ('PATCH', 'PATCH', 'Partial update of existing data', 1, CURRENT_TIMESTAMP),
    ('DELETE', 'DELETE', 'Delete data', 1, CURRENT_TIMESTAMP),
    -- Add other methods as needed
    ('OPTIONS', 'OPTIONS', 'Options for the resource', 1, CURRENT_TIMESTAMP),
    ('HEAD', 'HEAD', 'Retrieve headers only', 1, CURRENT_TIMESTAMP),
    ('TRACE', 'TRACE', 'Echoes back the received request', 1, CURRENT_TIMESTAMP),
    ('CONNECT', 'CONNECT', 'Reserved for use with proxies', 1, CURRENT_TIMESTAMP);

INSERT INTO order_type_lk (name, code, description, created_by, created_at) 
VALUES 
    ('Buy', 'BUY', 'Buy order type', 1, CURRENT_TIMESTAMP),
    ('Sell', 'SELL', 'Sell order type', 1, CURRENT_TIMESTAMP);

INSERT INTO api_lk (name, method, description, created_by, created_at, endpoint) 
VALUES ('PLACE_ORDER', 
        (SELECT id FROM http_method_lk WHERE name = 'POST'), 
        'API endpoint for placing orders', 
        1, 
        CURRENT_TIMESTAMP,
        '/api/orders/create');

INSERT INTO api_lk (name, method, description, created_by, created_at, endpoint) 
VALUES ('MODIFY_ORDER', 
        (SELECT id FROM http_method_lk WHERE name = 'PUT'), 
        'API endpoint for modifying orders', 
        1, 
        CURRENT_TIMESTAMP,
        '/api/order/update/{order_id}');

INSERT INTO api_lk (name, method, description, created_by, created_at, endpoint) 
VALUES ('CANCEL_ORDER', 
        (SELECT id FROM http_method_lk WHERE name = 'DELETE'), 
        'API endpoint for canceling orders', 
        1, 
        CURRENT_TIMESTAMP,
        '/api/order/cancel/{order_id}');

INSERT INTO api_lk (name, method, description, created_by, created_at, endpoint) 
VALUES ('FETCH_ALL_ORDERS', 
        (SELECT id FROM http_method_lk WHERE name = 'GET'), 
        'API endpoint for fetching all orders', 
        1, 
        CURRENT_TIMESTAMP,
        '/api/orders');

INSERT INTO api_lk (name, method, description, created_by, created_at, endpoint) 
VALUES ('FETCH_ORDER', 
        (SELECT id FROM http_method_lk WHERE name = 'GET'), 
        'API endpoint for fetching an order', 
        1, 
        CURRENT_TIMESTAMP,
        '/api/orders/{order_id}');

INSERT INTO api_lk (name, method, description, created_by, created_at, endpoint) 
VALUES ('TRADES', 
        (SELECT id FROM http_method_lk WHERE name = 'GET'), 
        'API endpoint for fetching all trades', 
        1, 
        CURRENT_TIMESTAMP,
        '/api/trades');


