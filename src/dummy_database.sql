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
    address_id SERIAL PRIMARY KEY,
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
    legal_address_id INT,
    FOREIGN KEY (legal_address_id) REFERENCES address(address_id),
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
    department_id INT,
    FOREIGN KEY (department_id) REFERENCES department(department_id),
    email_address VARCHAR,
    created_at TIMESTAMP,
    last_updated TIMESTAMP
);


DROP TABLE IF EXISTS sales_order;

CREATE TABLE sales_order (
    sales_order_id SERIAL PRIMARY KEY,
    created_at TIMESTAMP,
    last_updated TIMESTAMP,
    design_id INT,
    FOREIGN KEY (design_id) REFERENCES design(design_id),
    staff_id INT,
    FOREIGN KEY (staff_id) REFERENCES staff(staff_id),
    counterparty_id INT,
    FOREIGN KEY (counterparty_id) REFERENCES counterparty(counterparty_id),
    units_sold INT,
    unit_price NUMERIC,
    currency_id INT,
    FOREIGN KEY (currency_id) REFERENCES currency(currency_id),
    agreed_delivery_date VARCHAR,
    agreed_delivery_location_id INT,
    FOREIGN KEY (agreed_delivery_location_id) REFERENCES address(address_id)
);


DROP TABLE IF EXISTS purchase_order;

CREATE TABLE purchase_order (
    purchase_order_id SERIAL PRIMARY KEY,
    created_at TIMESTAMP,
    last_updated TIMESTAMP,
    staff_id INT,
    FOREIGN KEY (staff_id) REFERENCES staff(staff_id),
    counterparty_id INT,
    FOREIGN KEY (counterparty_id) REFERENCES counterparty(counterparty_id),
    item_code VARCHAR,
    item_quantity INT,
    item_unit_price NUMERIC,
    currency_id INT,
    FOREIGN KEY (currency_id) REFERENCES currency(currency_id),
    agreed_delivery_date VARCHAR,
    agreed_payment_date VARCHAR,
    agreed_delivery_location_id INT,
    FOREIGN KEY (agreed_delivery_location_id) REFERENCES address(address_id)
);


DROP TABLE IF EXISTS transaction;

CREATE TABLE transaction (
    transaction_id SERIAL PRIMARY KEY,
    transaction_type VARCHAR,
    sales_order_id INT,
    FOREIGN KEY (sales_order_id) REFERENCES sales_order(sales_order_id),
    purchase_order_id INT,
    FOREIGN KEY (purchase_order_id) REFERENCES purchase_order(purchase_order_id),
    created_at TIMESTAMP,
    last_updated TIMESTAMP
);


DROP TABLE IF EXISTS payment;

CREATE TABLE payment (
    payment_id SERIAL PRIMARY KEY,
    created_at TIMESTAMP,
    last_updated TIMESTAMP,
    transaction_id INT,
    FOREIGN KEY (transaction_id) REFERENCES transaction(transaction_id),
    counterparty_id INT,
    FOREIGN KEY (counterparty_id) REFERENCES counterparty(counterparty_id),
    payment_amount NUMERIC,
    currency_id INT,
    FOREIGN KEY (currency_id) REFERENCES currency(currency_id),
    payment_type_id INT,
    FOREIGN KEY (payment_type_id) REFERENCES payment_type(payment_type_id),
    paid BOOLEAN,
    payment_date VARCHAR,
    company_ac_number INT,
    counterparty_ac_number INT
);


INSERT INTO design
    (created_at, last_updated, design_name, file_location, file_name)
VALUES
    (now(), now(), 'wood', '/public', 'wood.json'),
    (now(), now(), 'plastic', '/private', 'plastic.json'),
    (now(), now(), 'granite', '/home', 'granite.json');


INSERT INTO currency
    (currency_code, created_at, last_updated)
VALUES
    ('AUD', now(), now()),
    ('GHS', now(), now()),
    ('CHF', now(), now());


INSERT INTO payment_type
    (payment_type_name, created_at, last_updated)
VALUES
    ('RECEIPT', now(), now()),
    ('REFUND', now(), now()),
    ('PAYMENT', now(), now());


INSERT INTO address
    (address_line_1, address_line_2, district, city, postal_code, country, phone, created_at, last_updated)
VALUES
    ('1 Northcoder Way', 'Learning Radial', 'Bedfordshire', 'Central City', '48115', 'Sudan', '1245 658745', now(), now()),
    ('2 Python Avenue', 'Pandas Bridge', 'Derbyshire', 'Derby', '888624', 'Congo', '5568 554241', now(), now()),
    ('3 SQL Street', 'Postgres Freeway', NULL, 'Star City', '384755', 'Zimbabwe', '8965 484496', now(), now());


INSERT INTO counterparty
    (counterparty_legal_name, commercial_contact, delivery_contact, created_at, last_updated)
VALUES
    ('Dad and Sons', 'Jason Todd', 'Felicity Smoak', now(), now()),
    ('Money LLC', 'Katy Kane', 'Barry Allen', now(), now()),
    ('Handbag Inc', 'Diana Prince', 'Alfred Pennyworth', now(), now());


INSERT INTO department
    (department_name, location, manager, created_at, last_updated)
VALUES
    ('Sales', 'Leeds', 'Tobias Funke', now(), now()),
    ('HR', 'Manchester', 'Lucille Bluth', now(), now()),
    ('Finance', 'Bolton', 'Lucille Austero', now(), now());


INSERT INTO staff
    (first_name, last_name, email_address, created_at, last_updated)
VALUES
    ('Pamela', 'Isley', 'pamelaisley@terrifictotes.com', now(), now()),
    ('Harleen', 'Quinzell', 'harleenquinzell@terrifictotes.com', now(), now()),
    ('Oswald', 'Cobblepot', 'oswaldcobblepot@terrifictotes.com', now(), now());


INSERT INTO sales_order
    (created_at, last_updated, units_sold, unit_price, agreed_delivery_date)
VALUES
    (now(), now(), 45841, 5.50, 2021-11-26),
    (now(), now(), 43214, 4.30, 2022-02-11),
    (now(), now(), 21451, 8.99, 2022-16-01);


INSERT INTO purchase_order
    (created_at, last_updated, item_code, item_quantity, item_unit_price, agreed_delivery_date, agreed_payment_date)
VALUES
    (now(), now(), 'DNG65DT', 400, 548.25, 2021-11-26, 2021-12-26),
    (now(), now(), '7FEHT5Y', 9999, 12.50, 2022-02-11, 2022-03-11),
    (now(), now(), 'FE456GH', 54, 999.30, 2022-06-01, 2022-07-01);


INSERT INTO transaction
    (transaction_type, created_at, last_updated)
VALUES
    ('SALE', now(), now()),
    ('PURCHASE', now(), now()),
    ('PURCHASE', now(), now());


INSERT INTO payment
    (created_at, last_updated, payment_amount, paid, payment_date, company_ac_number, counterparty_ac_number)
VALUES
    (now(), now(), 645724.50, TRUE, 2021-12-26, 9854217, 98745124),
    (now(), now(), 225410.41, TRUE, 2022-03-11, 4578124, 45124547),
    (now(), now(), 895874.99, FALSE, 2022-07-01, 4512114, 69695232);