
DROP DATABASE IF EXISTS dummy_totesys;
CREATE DATABASE dummy_totesys;

\c dummy_totesys;


DROP TABLE IF EXISTS design;

CREATE TABLE design (
    design_id SERIAL PRIMARY KEY,
    created_at TIMESTAMP,
    last_updated TIMESTAMP,
    design_name VARCHAR,
    file_location VARCHAR,
    file_name VARCHAR
);


DROP TABLE IF EXISTS currency;

CREATE TABLE currency (
    currency_id SERIAL PRIMARY KEY,
    currency_code VARCHAR,
    created_at TIMESTAMP,
    last_updated TIMESTAMP
);


DROP TABLE IF EXISTS payment_type;

CREATE TABLE payment_type (
    payment_type_id SERIAL PRIMARY KEY,
    payment_type_name VARCHAR,
    created_at TIMESTAMP,
    last_updated TIMESTAMP
);


DROP TABLE IF EXISTS address;

CREATE TABLE address (
    address_id INT PRIMARY KEY,
    address_line_1 VARCHAR,
    address_line_2 VARCHAR,
    district VARCHAR,
    city VARCHAR,
    postal_code VARCHAR,
    country VARCHAR,
    phone VARCHAR,
    created_at TIMESTAMP,
    last_updated TIMESTAMP
);


DROP TABLE IF EXISTS counterparty;

CREATE TABLE counterparty (
    counterparty_id SERIAL PRIMARY KEY,
    counterparty_legal_name VARCHAR,
    legal_address_id INT REFERENCES address(address_id),
    commercial_contact VARCHAR,
    delivery_contact VARCHAR,
    created_at TIMESTAMP,
    last_updated TIMESTAMP
);


DROP TABLE IF EXISTS department;

CREATE TABLE department (
    department_id SERIAL PRIMARY KEY,
    department_name VARCHAR,
    location VARCHAR,
    manager VARCHAR,
    created_at TIMESTAMP,
    last_updated TIMESTAMP
);


DROP TABLE IF EXISTS staff;

CREATE TABLE staff (
    staff_id SERIAL PRIMARY KEY,
    first_name VARCHAR,
    last_name VARCHAR,
    department_id INT REFERENCES department(department_id),
    email_address VARCHAR,
    created_at TIMESTAMP,
    last_updated TIMESTAMP
);


DROP TABLE IF EXISTS sales_order;

CREATE TABLE sales_order (
    sales_order_id SERIAL PRIMARY KEY,
    created_at TIMESTAMP,
    last_updated TIMESTAMP,
    design_id INT REFERENCES design(design_id),
    staff_id INT REFERENCES staff(staff_id),
    counterparty_id INT REFERENCES counterparty(counterparty_id),
    units_sold INT,
    unit_price NUMERIC,
    currency_id INT REFERENCES currency(currency_id),
    agreed_delivery_date VARCHAR,
    agreed_delivery_location_id INT REFERENCES address(address_id)
);


DROP TABLE IF EXISTS purchase_order;

CREATE TABLE purchase_order (
    purchase_order_id SERIAL PRIMARY KEY,
    created_at TIMESTAMP,
    last_updated TIMESTAMP,
    staff_id INT REFERENCES staff(staff_id),
    counterparty_id INT REFERENCES counterparty(counterparty_id),
    item_code VARCHAR,
    item_quantity INT,
    item_unit_price NUMERIC,
    currency_id INT REFERENCES currency(currency_id),
    agreed_delivery_date VARCHAR,
    agreed_payment_date VARCHAR,
    agreed_delivery_location_id INT REFERENCES address(address_id)
);


DROP TABLE IF EXISTS transaction;

CREATE TABLE transaction (
    transaction_id SERIAL PRIMARY KEY,
    transaction_type VARCHAR,
    sales_order_id INT REFERENCES sales_order(sales_order_id),
    purchase_order_id INT REFERENCES purchase_order(purchase_order_id),
    created_at TIMESTAMP,
    last_updated TIMESTAMP
);


DROP TABLE IF EXISTS payment;

CREATE TABLE payment (
    payment_id SERIAL PRIMARY KEY,
    created_at TIMESTAMP,
    last_updated TIMESTAMP,
    transaction_id INT REFERENCES transaction(transaction_id),
    counterparty_id INT REFERENCES counterparty(counterparty_id),
    payment_amount NUMERIC,
    currency_id INT REFERENCES currency(currency_id),
    payment_type_id INT REFERENCES payment_type(payment_type_id),
    paid BOOLEAN,
    payment_date VARCHAR,
    company_ac_number INT,
    counterparty_ac_number INT
);
