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
# Let's create our tables using SQL commands
%sql
CREATE OR REPLACE TABLE sql_101_store (
    store_id INT,
    store_name VARCHAR(100),
    store_location VARCHAR(100),
    store_manager VARCHAR(100),
    store_open_date DATE,
    store_phone VARCHAR(15)
);

CREATE OR REPLACE TABLE sql_101_product (
    sku_id INT,
    product_name VARCHAR(100),
    category VARCHAR(50),
    sub_category VARCHAR(50),
    brand VARCHAR(50),
    list_price DECIMAL(10, 2)
);

CREATE OR REPLACE TABLE sql_101_transactions (
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
%sql
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
%sql
INSERT INTO sql_101_store (store_id, store_name, store_location, store_manager, store_open_date, store_phone) VALUES
(1, 'Downtown Store', '123 Main St, Cityville', 'Alice Smith', '2020-01-15', '123-456-7890'),
(2, 'Uptown Store', '456 High St, Cityville', 'Bob Johnson', '2019-03-10', '123-555-7890');

# %% [markdown]
# Now let's populate the `sql_101_transactions` table with some transaction data. Don't worry, ChatGPT helped with this part!

# %%
# Inserting data into the sql_101_transactions table
%sql
-- Inserting transactions data
INSERT INTO sql_101_transactions (transaction_id, transaction_date, customer_id, amount, sku_id, price_per_unit, store_id) VALUES
    (1, '2024-05-01', 101, 3, 1, 1.50, 1),
    (2, '2024-05-02', 102, 2, 4, 2.50, 1),
    (3, '2024-05-03', 103, 1, 6, 2.00, 2),
    (4, '2024-05-04', 104, 5, 7, 2.20, 2),
    (5, '2024-05-05', 105, 2, 2, 1.70, 1),
    (6, '2024-05-06', 106, 3, 5, 3.00, 1),
    (7, '2024-05-07', 107, 1, 3, 1.80, 2),
    (8, '2024-05-08', 108, 4, 7, 2.20, 2),
    (9, '2024-05-09', 109, 2, 1, 1.50, 1),
    (10, '2024-05-10', 110, 5, 4, 2.50, 2),
    -- ... (transactions 11 to 99)
    (100, '2024-08-09', 130, 5, 4, 2.50, 2);

# %% [markdown]
# # Inspecting the Data 🔍
# 
# Let's take a look at the data we've just inserted into our tables.

# %%
# Selecting the first 10 rows from the sql_101_transactions table
%sql
SELECT * FROM sql_101_transactions LIMIT 10;

# %%
# Selecting all the rows from the sql_101_product table
%sql
SELECT * FROM sql_101_product;

# %%
# Selecting all the rows from the sql_101_store table
%sql
SELECT * FROM sql_101_store;
