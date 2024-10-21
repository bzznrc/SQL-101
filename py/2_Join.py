# %% [markdown]
# # What Is a Join? 🖇️
# 
# We saw how our data is rarely in the right format and we might need to group it and apply aggregate functions.
# 
# Unfortunately, it doesn't end there. Most times our data is also scattered in different tables, and we often need to put it back together.
# 
# It's not like this because data people are bad and want you to suffer (or not just that). Let's consider our example:
# 
# So far, we worked on the **Transactions** table, but usually you get a bunch of them, linked in what is called a **Fact-Dimension** relation. In our case:
# 
# - **Transactions** is our **Fact** table—it records what "happened", in this case a purchase. It includes keys that allow you to look up details in the other tables (the Dimension ones).
# - **Product** is one of the **Dimension** tables. It's accessed with the `sku_id` and it lists all the features of each SKU.
# - **Store** is the other **Dimension** table, and links to the Transactions one via the `store_id` field.
# 
# Why are the data arranged like that? Why don't we just have a big table that includes all the data?
# 
# There are multiple technical reasons, but the main ones are:
# 
# - **Size**: The **Product** table in our toy example is very tiny. But in reality, it could easily have 20/30+ columns. Now, for an item such as *Berillo Spaghetti N.5 500G*, you have just one line with these 20/30+ columns filled. If all the data was instead in the main **Transactions** table, every single transaction would have 20/30+ extra columns, and every single *Berillo Spaghetti N.5 500G* purchase would repeat the same information over and over again.
# - **Handling**: Let's say you realize that there is an error in the column *Size* for the item *Berillo Spaghetti N.5 500G*. If the information is split into two tables, you can just correct it once, whereas if all the data was in the main **Transactions** table, you would need to look up all the *Berillo Spaghetti N.5 500G* transactions and modify them one by one. Not great for performance.

# %%
# Load the SQL extension
%load_ext sql

# Connect to the existing SQLite database file
%sql sqlite:///my_database.db

# %% [markdown]
# **Check Our Tables 🔎**

# Let's select the first 5 lines for each to have a sense of how they look.

# Fact Table: it has one line for each fact, which is a purchase in this case

# %%
%%sql
SELECT * FROM sql_101_transactions LIMIT 5;

# %%
# Dimension Table: Product

%%sql
SELECT * FROM sql_101_product;

# %%
# Dimension Table: Store

%%sql
SELECT * FROM sql_101_store;

# %% [markdown]
# # Building Our First Join 👶

# In the **Transactions** table, we have the `sku_id` field, which shows up again in the **Product** table. It is used to identify a specific SKU and look it up in **Product**. It's the one we need to use for our **Join**.

# This magical field is called a **Key**. I think it's because it unlocks the relationship between the tables, but I could've made this up completely.

# But how do you know which key field to use in general? Usually for a Dimension table, the key should be the *first field*, and usually the name should be the same as that used in the Fact table (but this is a convention, and evil people designing the data with the clear intent of making your life miserable are out there).

# %%
# Let's perform a LEFT JOIN between transactions and products

%%sql
SELECT t.*,
       p.brand,
       p.product_name
FROM sql_101_transactions AS t
LEFT JOIN sql_101_product AS p ON t.sku_id = p.sku_id;

# %% [markdown]
# # Joins 101 🔗

# For a professional explanation: [W3Schools SQL Join](https://www.w3schools.com/sql/sql_join.asp)

# So basically, we want to take two or more tables, join them based on one field, and select fields from them as if they were a single one.

# Everything related to Joins lives within the **FROM** clause of our query.

# It looks like this:

# - **SELECT [...]**
# - **FROM** [table 1] **AS** [alias 1]
#   - [type] **JOIN** [table 2] **AS** [alias 2] **ON** [table/alias 1].[column] = [table/alias 2].[column]
#   - [type] **JOIN** [table 3] **AS** [alias 3] **ON** [table/alias 1].[column] = [table/alias 3].[column]
# - **WHERE [...]**

# Looks like there's a lot to unpack.

# To begin with, we usually use **Aliases** for tables so it is quicker to type and easier to read.
# You wouldn't like to have to type something like "CustomerOrderDetailsExtendedInformationDimTable" too often.

# Now, for the really complex bit: that [type] thing before the **JOIN**.
# There are a few kinds of Joins, and [this picture might help you](https://www.w3schools.com/sql/sql_join.asp). We'll see the main ones:

# - **INNER JOIN**: This is the most basic one. Assuming we're joining Table A and Table B, this results in all the lines that are in **both** tables.
# - **LEFT JOIN**: This results in all the lines that are in the left table (Table A in this case), and only the Table B rows that match Table A will have values in the result set. Table A rows that don't find a match in Table B will have all the values that would come from Table B set as NULL.
# - **RIGHT JOIN**: Same as Left but it's Right. ¯\\_(ツ)_/¯
# - **FULL OUTER JOIN**: This is kind of a mess. All the lines for both Table A and Table B. There could be NULLs in the Table A section of the results (Table B records that don't have a match in A) as well as NULLs in the Table B section. You should ask yourself why you're doing this.

# %%
# Let's look at the transactions table

%%sql
SELECT * FROM sql_101_transactions;

# %%
# Starting from the previous one, this time we add Aliases and include also the stores.

%%sql
SELECT 
  t.*, -- All fields from transactions
  p.brand, p.category, p.list_price, p.product_name, -- Relevant fields from products
  s.store_location, s.store_name 
FROM sql_101_transactions t
JOIN sql_101_product p ON t.sku_id = p.sku_id
JOIN sql_101_store s ON t.store_id = s.store_id;

# %% [markdown]
# As you can see, those are lots of fields. The key ones in particular show up twice (one from Table A and one from Table B).
# Usually, you'll want to select your fields to keep the result set a bit more tidy.

# %%
# Selecting specific fields to tidy up the result

%%sql
SELECT 
  t.*, -- All fields from transactions
  p.brand, p.category, p.list_price, p.product_name, -- Relevant fields from products
  s.store_location, s.store_name 
FROM sql_101_transactions t
JOIN sql_101_product p ON t.sku_id = p.sku_id
JOIN sql_101_store s ON t.store_id = s.store_id;

# %% [markdown]
# # What's Up with the Price? 💡

# Looking at the table above, you might notice that the price shows up twice.

# We have the one from the transactions table (`price_per_unit`) and the one from the product table (`list_price`). They look the same in these first lines, but we'd better check.

# This is technically a poor choice in how the database is designed (not my fault, it's ChatGPT's), but we can assume that the `list_price` is the price defined by the Brand and the `price_per_unit` is the actual price paid in the transaction. What happens if a retailer sells an item at a discount? We should see a price in the transactions table which is different from the one we have in the Product table.

# %%
# Checking for list_prices different than the price per unit

%%sql
SELECT 
  t.*, 
  p.brand, p.category, p.list_price, p.product_name,
  s.store_location, s.store_name 
FROM sql_101_transactions t
JOIN sql_101_product p ON t.sku_id = p.sku_id
JOIN sql_101_store s ON t.store_id = s.store_id
WHERE t.price_per_unit <> p.list_price; -- Records where the two prices don't match

# %% [markdown]
# # Joins Gone Wrong 👎

# With our current table structures and the data we have, it's very difficult to make mistakes with joins.
# However, this is very realistic with bigger and complex structures. Let's make an example.

# Assume someone added a new line for an SKU in the Products table with the same ID. This would not work in a realistic scenario as there are automatic checks on the ID fields, but let's pretend you don't know this.

# What happens then is that each line in the `t` table gets joined to all the matching lines in the `p` table. Every `sku_id` will have its match, but the `sku_id` of the duplicated record would match twice. This means that for that SKU, one line in the Transactions table will match with 2 lines in the Product table, and as a result, SQL will show two lines (each expanded with a different line from the Product table).

# Now, if I didn't check and just summed up the value column, I would basically end up with ~twice as much as I should!

# %%
# Let's assume there was a price change and the retailer added this new line with the updated price for Cileni Ripieni
# Note that this wouldn't really happen in a real-world scenario because the new item would likely have a different sku_id
# BUT IT WAS THE EASIEST WAY TO EXPLAIN IT SO WE'LL HAVE TO MAKE THIS WORK

%%sql
INSERT INTO sql_101_product (sku_id, product_name, category, sub_category, brand, list_price) VALUES
  (6, 'Cileni Ripieni', 'bakery', 'biscuits', 'Berillo', 2.80);

# %%
# Let's have a look at the Cileni Ripieni transactions in the Transactions table

%%sql
SELECT *
FROM sql_101_transactions
WHERE sku_id = 6;

# %%
# Let's look at the sku_id number 6 in the Product table

%%sql
SELECT *
FROM sql_101_product
WHERE sku_id = 6;

# %%
# So what happens now when we join them?

%%sql
SELECT *
FROM sql_101_transactions t 
JOIN sql_101_product p ON t.sku_id = p.sku_id
WHERE t.sku_id = 6
ORDER BY t.transaction_date;

# %% [markdown]
# Notice that we have duplicate transactions due to the duplicate `sku_id` in the product table.

# %%
# Finally, let's delete the wrong line in the Product table

%%sql
DELETE 
FROM sql_101_product
WHERE sku_id = 6 AND list_price = 2.80;

# %% [markdown]
# # Fun Exercise 📚

# Only one actually:

# **Join. The. Tables.**

# Perhaps you can start by joining `sql_101_transactions` and `sql_101_product`, and then join `sql_101_store` to them.
# Make sure you have all the transaction fields, the product fields (such as the brand), and the store fields (such as the store_name) in the result.

# %%
# Write your SQL query here:

%%sql
SELECT 
  t.*, 
  p.*, 
  s.*
FROM sql_101_transactions t
JOIN sql_101_product p ON t.sku_id = p.sku_id
JOIN sql_101_store s ON t.store_id = s.store_id;

# %% [markdown]
# # Do I Have to Write All That Stuff Every Time? 🥱

# Nope.

# Usually, when you work on complex table structures, you want to create a new table of your own with the results of the joins you've worked on.

# This table will be just like any other table, and we'll be able to use it easily going forward. We'll also use it for the incredible lesson on Grouping we have coming up 😎

# %%
# Creating a new table sql_101_transactions_ext with the joined data

%%sql
DROP TABLE IF EXISTS sql_101_transactions_ext;
CREATE TABLE sql_101_transactions_ext AS
SELECT 
  t.*,
  t.amount * t.price_per_unit AS tot_spent, -- It'll be useful to have this calculated already
  p.brand, p.category, p.list_price, p.product_name,
  s.store_location, s.store_name 
FROM sql_101_transactions t
JOIN sql_101_product p ON t.sku_id = p.sku_id
JOIN sql_101_store s ON t.store_id = s.store_id;

# %%
# Viewing the first 10 rows of the new table

%%sql
SELECT * FROM sql_101_transactions_ext LIMIT 10;
