CREATE TABLE Users (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  urn TEXT NOT NULL,
  username TEXT NOT NULL,
  email TEXT NOT NULL,
  password TEXT NOT NULL,
  created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
  is_logged_in INTEGER NOT NULL DEFAULT 0,
  last_login TIMESTAMP,
  updated_at TIMESTAMP
);

CREATE TABLE HTTPMethodLK (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  name TEXT,
  code TEXT,
  description TEXT,
  created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
  created_by INTEGER NOT NULL,
  updated_at TIMESTAMP,
  FOREIGN KEY (created_by) REFERENCES Users (id)
);

CREATE TABLE APILK (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  name TEXT,
  method INTEGER,
  description TEXT,
  created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
  created_by INTEGER NOT NULL,
  updated_at TIMESTAMP,
  FOREIGN KEY (method) REFERENCES HTTPMethodLK (id),
  FOREIGN KEY (created_by) REFERENCES Users (id)
);

CREATE TABLE TransactionsLog (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  urn TEXT NOT NULL,
  reference_urn TEXT NOT NULL,
  api_id INTEGER,
  request_payload JSON NOT NULL,
  request_headers JSON NOT NULL,
  response_payload JSON NOT NULL,
  response_headers JSON NOT NULL,
  http_status_code JSON NOT NULL,
  created_by INTEGER NOT NULL,
  created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
  updated_at TIMESTAMP,
  FOREIGN KEY (created_by) REFERENCES Users (id)
);

CREATE TABLE OrderTypeLK (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  name TEXT,
  code TEXT,
  description TEXT,
  created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
  created_by INTEGER NOT NULL,
  updated_at TIMESTAMP,
  FOREIGN KEY (created_by) REFERENCES Users (id)
);

CREATE TABLE Orders (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  urn TEXT NOT NULL,
  transaction_log_id INTEGER,
  quantity INTEGER NOT NULL,
  price REAL NOT NULL,
  order_type_id INTEGER NOT NULL,
  average_traded_price REAL NOT NULL,
  traded_quantity REAL NOT NULL,
  order_active REAL NOT NULL,
  created_by INTEGER NOT NULL,
  created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
  updated_at TIMESTAMP,
  FOREIGN KEY (transaction_log_id) REFERENCES TransactionsLog (id),
  FOREIGN KEY (order_type_id) REFERENCES OrderTypeLK (id),
  FOREIGN KEY (created_by) REFERENCES Users (id)
);

CREATE TABLE OrderTransaction (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  urn TEXT NOT NULL,
  bid_order_id INTEGER NOT NULL,
  ask_order_id INTEGER NOT NULL,
  quantity INTEGER NOT NULL,
  price REAL NOT NULL,
  execution_timestamp TIMESTAMP NOT NULL,
  created_by INTEGER NOT NULL,
  created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
  updated_at TIMESTAMP,
  FOREIGN KEY (bid_order_id) REFERENCES Orders (id),
  FOREIGN KEY (ask_order_id) REFERENCES Orders (id),
  FOREIGN KEY (created_by) REFERENCES Users (id)
);

ALTER TABLE APILK 
ADD COLUMN endpoint VARCHAR(255);

ALTER TABLE Users 
ADD COLUMN is_deleted BOOLEAN DEFAULT false;

CREATE INDEX Users_index_0 ON Users (urn);
CREATE INDEX Users_index_1 ON Users (email);
CREATE INDEX Users_index_2 ON Users (username);
CREATE INDEX Users_index_3 ON Users (created_at);
CREATE INDEX TransactionsLog_index_4 ON TransactionsLog (urn);
CREATE INDEX TransactionsLog_index_5 ON TransactionsLog (reference_urn);
CREATE INDEX Orders_index_6 ON Orders (urn);
CREATE INDEX Orders_index_7 ON Orders (transaction_log_id);
CREATE INDEX Orders_index_8 ON Orders (created_at);
CREATE INDEX OrderTransaction_index_9 ON OrderTransaction (urn);
CREATE INDEX OrderTransaction_index_10 ON OrderTransaction (ask_order_id);
CREATE INDEX OrderTransaction_index_11 ON OrderTransaction (bid_order_id);
CREATE INDEX OrderTransaction_index_12 ON OrderTransaction (created_at);
CREATE INDEX OrderTransaction_index_13 ON OrderTransaction (execution_timestamp);
