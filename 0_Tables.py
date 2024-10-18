# %% [markdown]
# # Let's Get Some Data 💾
# 
# To start working with SQL and perform our data tasks, we need some tables to play with. Let's create three tables:
# 
# - `sql_101_store`
# - `sql_101_product`
# - `sql_101_transactions`
# 
# *Ooooohhhhh!* (the audience is amazed here).

# %%
# Load the SQL extension
%load_ext sql

# Connect to a SQLite database file
%sql sqlite:///my_database.db

# %%
# Let's create our tables using SQL commands
%%sql
DROP TABLE IF EXISTS sql_101_store;
CREATE TABLE sql_101_store (
    store_id INT,
    store_name TEXT,
    store_location TEXT,
    store_manager TEXT,
    store_open_date DATE,
    store_phone TEXT
);

DROP TABLE IF EXISTS sql_101_product;
CREATE TABLE sql_101_product (
    sku_id INT,
    product_name TEXT,
    category TEXT,
    sub_category TEXT,
    brand TEXT,
    list_price DECIMAL(10, 2)
);

DROP TABLE IF EXISTS sql_101_transactions;
CREATE TABLE sql_101_transactions (
    transaction_id INT,
    transaction_date DATE,
    customer_id INT,
    amount INT,
    price_per_unit DECIMAL(10, 2),
    sku_id INT,
    store_id INT
);

# %% [markdown]
# Now that we've created our tables, let's insert some data into them.

# %%
# Inserting data into the sql_101_product table
%%sql
INSERT INTO sql_101_product (sku_id, product_name, category, sub_category, brand, list_price) VALUES
  (1, 'Spaghetti N5', 'pasta', 'long cut', 'Berillo', 1.60),
  (2, 'Just Penne', 'pasta', 'short cut', 'De Cocco', 1.70),
  (3, 'Fusilloni', 'pasta', 'short cut', 'Molisano', 1.80),
  (4, 'Tomatoni Sauce', 'sauces', 'red', 'Motti', 2.50),
  (5, 'Presto Pesto Sauce', 'sauces', 'pesto', 'Berillo', 3.00),
  (6, 'Cileni Ripieni', 'bakery', 'biscuits', 'Berillo', 2.00),
  (7, 'Biskotti', 'bakery', 'biscuits', 'Ferraro', 2.20),
  (8, 'Also Penne', 'pasta', 'short cut', 'Berillo', 1.60),
  (9, 'Fusillonioni', 'pasta', 'short cut', 'Berillo', 1.70),
  (10, 'Spaghetti N5000', 'pasta', 'long cut', 'De Cocco', 2.00);

# %%
# Inserting data into the sql_101_store table
%%sql
INSERT INTO sql_101_store (store_id, store_name, store_location, store_manager, store_open_date, store_phone) VALUES
    (1, 'Downtown Store', '123 Main St, Cityville', 'Alice Smith', '2020-01-15', '123-456-7890'),
    (2, 'Uptown Store', '456 High St, Cityville', 'Bob Johnson', '2019-03-10', '123-555-7890');

# %% [markdown]
# Now let's populate the `sql_101_transactions` table with some transaction data.

# %%
# Inserting data into the sql_101_transactions table
%%sql
INSERT INTO sql_101_transactions (transaction_id, transaction_date, customer_id, amount, price_per_unit, sku_id, store_id) VALUES
    (1, '2024-05-01', 101, 3, 1.50, 1, 1),
    (2, '2024-05-02', 102, 2, 2.50, 4, 1),
    (3, '2024-05-03', 103, 1, 2.00, 6, 2),
    (4, '2024-05-04', 104, 5, 2.20, 7, 2),
    (5, '2024-05-05', 105, 2, 1.70, 2, 1),
    (6, '2024-05-06', 106, 3, 3.00, 5, 1),
    (7, '2024-05-07', 107, 1, 1.80, 3, 2),
    (8, '2024-05-08', 108, 4, 2.20, 7, 2),
    (9, '2024-05-09', 109, 2, 1.50, 1, 1),
    (10, '2024-05-10', 110, 5, 2.50, 4, 2),
    -- Add more transactions as needed
    (11, '2024-06-01', 111, 3, 1.60, 8, 1),
    (12, '2024-06-02', 112, 2, 2.00, 6, 1),
    (13, '2024-06-03', 113, 4, 1.70, 2, 2),
    (14, '2024-06-04', 114, 1, 2.50, 4, 2),
    (15, '2024-06-05', 115, 5, 2.00, 6, 1),
    (16, '2024-06-06', 116, 2, 1.80, 3, 1),
    (17, '2024-06-07', 117, 3, 2.20, 7, 2),
    (18, '2024-06-08', 118, 4, 1.70, 9, 2),
    (19, '2024-06-09', 119, 2, 1.60, 1, 1),
    (20, '2024-06-10', 120, 5, 2.00, 10, 1);
    -- Continue adding transactions up to transaction_id 100

# %% [markdown]
# # Inspecting the Data 🔍
# 
# Let's take a look at the data we've just inserted into our tables.

# %%
# Selecting the first 10 rows from the sql_101_transactions table
%%sql
SELECT * FROM sql_101_transactions LIMIT 10;

# %%
# Selecting all the rows from the sql_101_product table
%%sql
SELECT * FROM sql_101_product;

# %%
# Selecting all the rows from the sql_101_store table
%%sql
SELECT * FROM sql_101_store;
