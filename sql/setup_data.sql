CREATE TABLE IF NOT EXISTS address (
  id INTEGER PRIMARY KEY,
  address_line1 TEXT NOT NULL,
  address_line2 TEXT,
  city TEXT NOT NULL,
  region TEXT,
  country TEXT NOT NULL,
  zip INTEGER NOT NULL
);

CREATE TABLE IF NOT EXISTS store_item (
  id            INTEGER PRIMARY KEY,
  name          TEXT NOT NULL,
  description   TEXT NOT NULL,
  stock         INTEGER NOT NULL,
  category      TEXT NOT NULL
);

CREATE TABLE IF NOT EXISTS payment (
  id          INTEGER PRIMARY KEY,
  card_number INTEGER NOT NULL, -- Change from string to INTEGER
  cvv         INTEGER NOT NULL,
  expiration  DATE NOT NULL,
  payment     INTEGER, -- Change from paymentAddress to payment (INTEGER)
  FOREIGN KEY(payment) REFERENCES address(id)
);

-- "order" is reserved word in SQL so rename to "orders"
CREATE TABLE IF NOT EXISTS orders (
  id                  INTEGER PRIMARY KEY,
  item_id             INTEGER,
  user                INTEGER
  shipping_address_id INTEGER NOT NULL,
  payment_id          INTEGER NOT NULL,
  date                DATE NOT NULL,
  FOREIGN KEY(item_id) REFERENCES store_item(id),
  FOREIGN KEY(shipping_address_id) REFERENCES address(id),
  FOREIGN KEY(payment_id) REFERENCES payment(id),
  FOREIGN KEY(user) REFERENCES user(id)
);

CREATE TABLE IF NOT EXISTS user (
  id               INTEGER PRIMARY KEY,
  user_name        TEXT,
  password         TEXT NOT NULL,
  shipping_address TEXT NOT NULL,
  order_history    INTEGER,
  FOREIGN KEY(order_history) REFERENCES orders(id)
);

ALTER TABLE IF EXISTS orders
ADD CONSTRAINT FK_User
FOREIGN KEY(user) REFERENCES user(id);

DROP TABLE IF EXISTS user;
DROP TABLE IF EXISTS orders;
DROP TABLE IF EXISTS payment;
DROP TABLE IF EXISTS store_item;
DROP TABLE IF EXISTS address;
