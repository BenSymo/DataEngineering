"""
Data Modelling Lesson: What it is and how to design tables for analytics.

Run this file to print the lesson:  python data_modelling_lesson.py
"""

LESSON = """
=====================================================================
1. WHAT IS DATA MODELLING?
=====================================================================
Data modelling is deciding how your data is organised: which tables
exist, what columns they have, and how they connect.

Think of building a library. You can throw all the books in a pile,
or you can plan shelves, sections and a catalogue. The books are the
same, but one library is easy to use and the other is not.

A good model makes queries simple, fast and correct. A bad model
leads to slow queries, wrong numbers and endless fixes.

=====================================================================
2. TWO KINDS OF SYSTEM: OLTP vs OLAP
=====================================================================
OLTP  (Online Transaction Processing)
      Runs the business: place an order, update an address.
      Many small reads and writes. Highly NORMALISED (data is split
      into many tables, with no repeated data).
      Examples: the database behind an app.

OLAP  (Online Analytical Processing)
      Answers questions: "Revenue by region by month?"
      Few, large reads over lots of history. DENORMALISED on
      purpose (fewer joins, easier queries).
      Examples: a data warehouse.

Data engineers mostly move data FROM OLTP systems TO OLAP systems,
and reshape it on the way.

=====================================================================
3. NORMALISATION IN ONE MINUTE
=====================================================================
Normalising means storing each fact once.

Bad (customer details repeated on every order row):

    order_id | customer_name | customer_city | amount

Better (split into two tables, joined by a key):

    customers: customer_id | name | city
    orders:    order_id | customer_id | amount

Benefit: change a city in one place. Cost: more joins. OLTP systems
accept that cost. Warehouses usually do not.

=====================================================================
4. THE STAR SCHEMA (THE MOST IMPORTANT PATTERN)
=====================================================================
A star schema has one central FACT table surrounded by DIMENSION
tables, like a star.

FACT TABLE       Records events or measurements. Mostly numbers.
                 Many rows. (sales, clicks, payments)
DIMENSION TABLE  Describes the context. Mostly text. Fewer rows.
                 (customer, product, date, store)

              dim_customer
                   |
    dim_date --- fact_sales --- dim_product
                   |
               dim_store

Fact table example:

    fact_sales
      sale_id
      date_key       -> dim_date
      customer_key   -> dim_customer
      product_key    -> dim_product
      quantity       (measure)
      amount         (measure)

Dimension example:

    dim_product
      product_key    (surrogate key)
      product_id     (the ID from the source system)
      name
      category
      brand

A typical query is simple and fast:

    SELECT d.month, p.category, SUM(f.amount) AS revenue
    FROM fact_sales f
    JOIN dim_date d    ON f.date_key = d.date_key
    JOIN dim_product p ON f.product_key = p.product_key
    GROUP BY d.month, p.category;

=====================================================================
5. THE GRAIN: DECIDE THIS FIRST
=====================================================================
The grain is what ONE row in the fact table means.

  "One row per order line item"    <- a clear grain
  "One row per customer per day"   <- also clear

Write the grain down before you design anything. Mixing grains in one
table is the most common cause of wrong totals.

=====================================================================
6. KEYS
=====================================================================
NATURAL KEY     The ID from the source system (customer_id = 'C42').
SURROGATE KEY   An ID you create in the warehouse (customer_key = 7).
PRIMARY KEY     Uniquely identifies a row.
FOREIGN KEY     Points to a primary key in another table.

Use surrogate keys in dimensions. They protect you if source IDs
change or are reused, and they make history tracking possible.

=====================================================================
7. SLOWLY CHANGING DIMENSIONS (SCD)
=====================================================================
What happens when a customer moves city? Do you overwrite it or keep
the history?

TYPE 1  Overwrite the old value. Simple, but history is lost.
TYPE 2  Add a new row and keep the old one. Full history.

Type 2 example:

    customer_key | customer_id | city   | valid_from | valid_to   | is_current
    1            | C42         | Leeds  | 2023-01-01 | 2024-06-30 | false
    2            | C42         | London | 2024-07-01 | 9999-12-31 | true

Old sales still point to key 1 (Leeds). New sales point to key 2
(London). Reports show the city as it was at the time.

=====================================================================
8. LAYERS: THE MEDALLION PATTERN
=====================================================================
Modern pipelines store data in stages:

  BRONZE   Raw data, exactly as it arrived. Never edited.
  SILVER   Cleaned, de-duplicated, correct types.
  GOLD     Business-ready models (star schemas, reports).

Benefits: you can always rebuild from raw, and each layer has one
clear job. (You may also see names like raw / staging / marts.)

=====================================================================
9. OTHER STYLES (JUST SO YOU KNOW)
=====================================================================
SNOWFLAKE SCHEMA  A star where dimensions are normalised further.
                  Saves space but needs more joins.
DATA VAULT        Hubs, links and satellites. Suited to large
                  enterprises with many changing sources.
ONE BIG TABLE     One wide denormalised table. Quick for BI tools
                  and cheap on modern columnar warehouses, but hard
                  to maintain.

Start with star schemas. They fit most analytics needs.

=====================================================================
10. GOOD HABITS
=====================================================================
  - Start from the business questions, then design the tables.
  - Write down the grain of every fact table.
  - Use clear names: fact_ and dim_ prefixes, snake_case, one
    meaning per column.
  - Keep a date dimension. It makes time reports easy.
  - Store money and measures in the fact table, descriptions in
    dimensions.
  - Document every table and column (dbt makes this easy).

=====================================================================
11. PRACTICE EXERCISE
=====================================================================
Design a model for an online shop. Orders have a customer, several
products, a date and a payment method.

  1. List 5 business questions (e.g. "best-selling category per
     month?").
  2. Choose the grain of the fact table.
  3. Draw the star: one fact table, 4 or more dimensions.
  4. List the columns and keys for each table.
  5. Decide which dimension needs SCD Type 2, and why.
  6. Write the SQL for 2 of your business questions.
  7. Bonus: create it in DuckDB or Postgres (use Docker) and load
     some sample data.

Next steps: build your model with dbt, and add data quality tests.
"""


def main():
    print(LESSON)


if __name__ == "__main__":
    main()
