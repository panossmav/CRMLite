CREATE TABLE IF NOT EXISTS user_logs(
    user TEXT NOT NULL,
    action TEXT NOT NULL,
    dateandtime TEXT NOT NULL,
    log_id INTEGER PRIMARY KEY AUTOINCREMENT
);

CREATE TABLE IF NOT EXISTS customers(
    name TEXT NOT NULL,
    phone INTEGER NOT NULL,
    email TEXT NOT NULL,
    address TEXT,
    vat INTEGER,
    cust_id INTEGER PRIMARY KEY AUTOINCREMENT
);

CREATE TABLE IF NOT EXISTS products(
    title TEXT NOT NULL,
    price FLOAT NOT NULL,
    stock INTEGER,
    sku INTEGER PRIMARY KEY AUTOINCREMENT
);

CREATE TABLE IF NOT EXISTS orders(
    cust_name TEXT,
    cust_phone INTEGER NOT NULL,
    prod_sku INTEGER NOT NULL,
    prod_title TEXT,
    rev FLOAT NOT NULL,
    status TEXT NOT NULL DEFAULT 'Fulfilled',
    order_id INTEGER PRIMARY KEY AUTOINCREMENT
);