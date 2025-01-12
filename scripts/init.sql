-- Create the items table
CREATE TABLE items (
    id SERIAL PRIMARY KEY,
    name VARCHAR(50),
    description VARCHAR(255),
    price NUMERIC
);

--==================================================================

-- Create the currencies table
CREATE TABLE currencies (
    id SERIAL PRIMARY KEY,
    name VARCHAR(50),
    description VARCHAR(255),
    code VARCHAR(50)
);

-- Insert data into currencies table
INSERT INTO currencies (id, name, description, code) VALUES
    (1, 'ABABN_TETHER', 'توضیحات برای رمز ارز آبان تتر', 'ABAN'),
    (2, 'NATIONAL_TETHER', 'رمز ارز', 'TETHER');

--====================================================================

-- Create the users table
CREATE TABLE users (
    id SERIAL PRIMARY KEY,
    first_name VARCHAR(255),
    last_name VARCHAR(255),
    national_code VARCHAR(255) UNIQUE NOT NULL,
    password VARCHAR(255) UNIQUE NOT NULL
);

-- Create the accounts table
CREATE TABLE accounts (
    id SERIAL PRIMARY KEY,
    account_number VARCHAR(255),
    total_amount NUMERIC,
    f_user_id INT,
    CONSTRAINT fk_user FOREIGN KEY (f_user_id) REFERENCES users(id) ON DELETE CASCADE
);

-- Create indexes for optimization
CREATE INDEX idx_users_first_name ON users (first_name);
CREATE INDEX idx_accounts_account_number ON accounts (account_number);
CREATE INDEX idx_accounts_f_user_id ON accounts (f_user_id);

--====================================================================

-- Create the orders table
CREATE TABLE orders (
    id SERIAL PRIMARY KEY,
    f_user_id INT REFERENCES users(id),
    crypto_name VARCHAR(50),
    amount FLOAT,
    total_price FLOAT,
    is_settled CHAR(1) DEFAULT '0'
);
