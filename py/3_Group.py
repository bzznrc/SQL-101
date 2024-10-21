# %% [markdown]
# # Grouping 👨‍👦‍👦👩‍👩‍👧

# So now you can get:
# - All the data as is (`SELECT *`)
# - Just a few columns (by selecting specific columns)
# - Just a few rows (by adding a `WHERE` clause)
# - Sorted by a column (using `ORDER BY`)
# - Data from several tables together (with various `JOIN`s)

# Nice! But what if we wanted to have some high-level insights on that data? These are some examples that might ring a bell:
# - How many sales per city or per store?
# - How many customers bought a specific product?
# - What's the average transaction amount?

# Of course, the plain data that we start with doesn't have these values in some "cell". We need to calculate them, but how?

# Introducing: **GROUP BY**!
# - `GROUP BY` can separate the data logically based on some criteria.
# - Gets applied after the rest of the query (so you can still `SELECT` stuff `FROM` somewhere `WHERE` conditions).
# - Splits logically the data into groups, so that you'll have one line per group in the results.
# - We typically use it because we can then *do something* with the group, e.g., apply an *aggregate function* (`SUM`, `MAX`, `MIN`, `AVG`, `COUNT`).

# But let's start with these **Aggregate Functions**:

# %%
# Load the SQL extension
%load_ext sql

# Connect to the existing SQLite database file
%sql sqlite:///my_database.db

# %% [markdown]
# # Aggregate Functions

# Let's say you have a table with sales. It's quite common. The first thing you might want to know is:

# - How much did we sell on a specific day?
# - What's the average price?
# - How many purchases do we have?
# - What are the min and max prices we sold a given SKU at?

# Well, using what we learned so far, we have no way of answering that question yet. Luckily, **Aggregate Functions** are here to help us!

# %% [markdown]
# # `SUM` ➕

# Using `SUM`, we need to specify the column we want to sum up. The result will be just one row, with the summed-up value. Pretty simple, right?

# %%
# Let's sum up the total spent after a certain date

%%sql
SELECT SUM(tot_spent) AS total_revenue
FROM sql_101_transactions_ext
WHERE transaction_date > '2024-07-01';

# %% [markdown]
# ### Make it Fancy!
# # Aliases 🎭

# The column name is a bit ugly.

# When we create new columns like the `SUM` here, we might want to give them a proper name. To do so, we use the **`AS`** statement.

# %%
# The previous query already uses an alias, but let's see another example

%%sql
SELECT SUM(amount) AS total_units_sold
FROM sql_101_transactions_ext
WHERE transaction_date > '2024-07-01';

# %% [markdown]
# # `MAX` & `MIN` 🔶🔸

# `MAX` and `MIN` will return the maximum or minimum value they encounter in the specified column. The result will be just one row, with that value.

# %%
# Finding the minimum and maximum total spent in transactions after July 1st

%%sql
SELECT MIN(tot_spent) AS min_spent,
       MAX(tot_spent) AS max_spent
FROM sql_101_transactions_ext
WHERE transaction_date > '2024-07-01';

# %% [markdown]
# # `AVG` ➗

# `AVG` will return the average value in the specified column. The result will be just one row, with that value.

# %%
# Calculating the average total spent after July 1st

%%sql
SELECT AVG(tot_spent) AS avg_spent
FROM sql_101_transactions_ext
WHERE transaction_date > '2024-07-01';

# %% [markdown]
# ### Make it Fancy!
# # `ROUND` 🎱 

# Uuuhhh look at that monstrosity!

# We have way too many decimals here. What we can do is use **`ROUND`** to make sure we get a fixed number of decimals.

# `ROUND` gets a value and the number of desired digits as inputs.

# %%
# Rounding the average total spent to 2 decimal places

%%sql
SELECT ROUND(AVG(tot_spent), 2) AS avg_spent
FROM sql_101_transactions_ext
WHERE transaction_date > '2024-07-01';

# %% [markdown]
# # `COUNT` ◼◼

# `COUNT` will simply return the number of lines we have selected.

# Since it counts lines instead of looking at a specific value, we can just ask it how many lines we have without specifying a column, using `COUNT(*)`.

# You can try to change the `WHERE` clause to get different results!

# %%
# Counting the number of transactions after July 1st

%%sql
SELECT COUNT(*) AS count_transactions,
       SUM(tot_spent) AS total_revenue
FROM sql_101_transactions_ext
WHERE transaction_date > '2024-07-01';

# %% [markdown]
# # 📚 Exercise!

# ### What is the Min, Max, Avg `tot_spent` for 'Spaghetti N5'?

# %%
# Let's check the data first

%%sql
SELECT * FROM sql_101_transactions_ext WHERE product_name = 'Spaghetti N5' LIMIT 5;

# %%
# Now, calculate the metrics

%%sql
SELECT
     MIN(tot_spent) AS min_spent,
     MAX(tot_spent) AS max_spent,
     ROUND(AVG(tot_spent), 2) AS avg_spent,
     SUM(tot_spent) AS total_spent
FROM sql_101_transactions_ext
WHERE product_name = 'Spaghetti N5';

# %% [markdown]
# # `GROUP BY` ⚫⚪

# Ok, so remember those *Aggregate Functions*? They sure are interesting, but they would be much more interesting if only we had a way of separating our data based on certain criteria and running the same *Aggregate Function* on each.

# Oh wait!

# For grouping, we insert the **`GROUP BY`** clause after the **`WHERE`** one, and we can list one or many columns we need to group by. It's very important to remember that:
# - Every column that appears in the **`GROUP BY`** needs to be also in the **`SELECT`**
# - In the **`SELECT`** there can only be the **`GROUP BY`** columns and **Aggregate Functions**

# %%
# Let's try to break down this fancy query in a few steps

# Final query

%%sql
SELECT brand, 
       category,
       COUNT(*) AS nr_transactions, 
       ROUND(AVG(price_per_unit), 2) AS avg_unit_price,
       ROUND(AVG(tot_spent), 2) AS avg_tot_spent,
       MAX(transaction_date) AS last_transaction
FROM sql_101_transactions_ext
GROUP BY brand, category
ORDER BY brand, category;

# %% [markdown]
# Let's start with the `GROUP BY` structure. We initially group by the `brand` column.
# This will result in a single row per brand, so here's where we change our data granularity.
# These lines will now support all of the Aggregate Functions we want.

# %%
# Grouping by brand

%%sql
SELECT brand
FROM sql_101_transactions_ext
GROUP BY brand
ORDER BY brand;

# %% [markdown]
# Now let's add an additional `GROUP BY` level. We can ideally group by as many fields as we want.
# The result will always be that each of those field values combinations will make up a new line.
# It's kind of the result you get with a `DISTINCT`, except we now can add all of the Aggregate Functions we want.

# %%
# Grouping by brand and category

%%sql
SELECT brand, category
FROM sql_101_transactions_ext
GROUP BY brand, category
ORDER BY brand, category;

# %% [markdown]
# And now we add all of the Aggregate Functions we want, and voilà, the final query.
# Adding a count is especially useful because it lets you understand how many lines of the original table are "hidden" within each line in the grouped-up one.

# %%
# Final query with aggregates

%%sql
SELECT brand, 
       category,
       COUNT(*) AS nr_transactions,
       SUM(tot_spent) AS sum_tot,
       ROUND(AVG(price_per_unit), 2) AS avg_unit_price,
       ROUND(AVG(tot_spent), 2) AS avg_tot_spent,
       MAX(transaction_date) AS last_transaction
FROM sql_101_transactions_ext
GROUP BY brand, category
ORDER BY brand, category;

# %% [markdown]
# Another useful example:
# Let's compute the same metrics, but on the two different stores we have.
# In order to do this, the `GROUP BY` fields will change (and consequently also the first `SELECT` will).

# %%
# Grouping by store_name

%%sql
SELECT store_name,
       COUNT(*) AS nr_transactions, 
       ROUND(AVG(price_per_unit), 2) AS avg_unit_price,
       ROUND(AVG(tot_spent), 2) AS avg_tot_spent,
       MAX(transaction_date) AS last_transaction
FROM sql_101_transactions_ext
GROUP BY store_name
ORDER BY store_name;

# %% [markdown]
# # 📚 Other Exercise!

# ### Calculate the Revenue for each `product_name`

# %%
# Calculating total revenue per product

%%sql
SELECT product_name,
       SUM(tot_spent) AS total_revenue
FROM sql_101_transactions_ext
GROUP BY product_name
ORDER BY total_revenue DESC;

# %% [markdown]
# **Spoilers Ahead!**

# Calculate the total revenue for each SKU starting from June 1st.

# %%
%%sql
SELECT brand, product_name,
       MAX(transaction_date) AS last_purchase_date,
       SUM(tot_spent) AS revenue
FROM sql_101_transactions_ext
WHERE transaction_date >= '2024-06-01'
GROUP BY brand, product_name
ORDER BY brand;

# %% [markdown]
# # Big Recap 💡

# Today we entered the magical world of the Grouped Queries, learning about:

# - **Aggregate Functions**, such as `SUM()`, `MAX()`, `MIN()`, `AVG()`, and `COUNT()`. The key idea with these functions is that the result won't be a table anymore, but just a single value (the result of the sum, average, etc.).
# - **`GROUP BY`**, which allows us to divide our table into groups, based on the values of one or more fields. For example, if we apply a `GROUP BY brand`, the result set will have one line per each brand.
# - **Applying Aggregate Functions to Groups**. When we use the `GROUP BY`, we can include in the **`SELECT`** clause:
#   - The fields used for grouping
#   - Any number of Aggregate Functions, and this allows us to produce all sorts of metrics related to specific groups

# %% [markdown]
# **Congratulations!** You've now mastered the basics of grouping and aggregating data using SQL. This is a powerful tool that will allow you to extract valuable insights from your data.
