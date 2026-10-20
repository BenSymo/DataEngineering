"""
dbt Lesson: What it is, how to set it up, and how to use it.

Run this file to print the lesson:  python dbt_lesson.py
"""

LESSON = """
=====================================================================
1. WHAT IS DBT?
=====================================================================
dbt (data build tool) lets you transform data inside your warehouse
using just SQL SELECT statements.

You write a SELECT. dbt turns it into a table or view, runs the
models in the right order, tests them, and writes documentation.

Think of it as a recipe book for your tables. Each recipe (model)
says how to make one table from others. dbt works out the cooking
order for you.

dbt does the "T" in ELT (Extract, Load, Transform). Other tools load
raw data into the warehouse. dbt reshapes it there.

Why data engineers care:
  - Transformations become version-controlled code.
  - Built-in tests catch bad data.
  - Documentation and lineage graphs come for free.
  - Works with Snowflake, BigQuery, Redshift, Postgres, DuckDB...

=====================================================================
2. KEY WORDS
=====================================================================
PROJECT      A folder of dbt files (dbt_project.yml is the config).
MODEL        A .sql file with one SELECT. Becomes a table or view.
SOURCE       A raw table loaded by something else.
SEED         A small CSV in your project, loaded as a table.
REF          {{ ref('model') }} - refer to another model. This sets
             the run order.
MATERIALIZATION  How a model is built: view, table, incremental,
             or ephemeral.
TEST         A check on your data (unique, not_null, etc).
PROFILE      Connection settings for your warehouse (profiles.yml).
DAG          The graph of models and how they depend on each other.

=====================================================================
3. INSTALL (LOCAL PRACTICE, NO WAREHOUSE NEEDED)
=====================================================================
We use DuckDB, a database that runs from a single local file.

    python -m venv .venv
    source .venv/bin/activate      # Windows: .venv\\Scripts\\activate
    pip install dbt-duckdb

Check it works:
    dbt --version

For a real warehouse install its adapter instead, e.g.
dbt-snowflake, dbt-bigquery, dbt-postgres.

=====================================================================
4. CREATE A PROJECT
=====================================================================
    dbt init shop
    cd shop

Edit the profile file profiles.yml (in ~/.dbt/ or the project
folder) to point at DuckDB:

    shop:
      target: dev
      outputs:
        dev:
          type: duckdb
          path: dev.duckdb
          threads: 4

Check the connection:
    dbt debug

=====================================================================
5. LOAD SOME DATA WITH A SEED
=====================================================================
Create seeds/raw_orders.csv:

    order_id,customer_id,amount,status
    1,10,25.00,completed
    2,11,40.00,completed
    3,10,15.00,cancelled
    4,12,60.00,completed

Load it:
    dbt seed

=====================================================================
6. YOUR FIRST MODELS
=====================================================================
Staging model (clean the raw data). models/staging/stg_orders.sql:

    select
        order_id,
        customer_id,
        amount,
        status
    from {{ ref('raw_orders') }}

Mart model (business-ready). models/marts/customer_revenue.sql:

    select
        customer_id,
        count(*)    as orders,
        sum(amount) as revenue
    from {{ ref('stg_orders') }}
    where status = 'completed'
    group by customer_id

Run them:
    dbt run

dbt sees that customer_revenue uses stg_orders (through ref), so it
builds stg_orders first. You never set the order by hand.

Set how models are built in dbt_project.yml:

    models:
      shop:
        staging:
          +materialized: view
        marts:
          +materialized: table

=====================================================================
7. TESTS
=====================================================================
Add models/staging/schema.yml:

    version: 2

    models:
      - name: stg_orders
        description: "One row per order, cleaned."
        columns:
          - name: order_id
            description: "Primary key."
            tests:
              - unique
              - not_null
          - name: status
            tests:
              - accepted_values:
                  values: ['completed', 'cancelled']
          - name: customer_id
            tests:
              - not_null

Run them:
    dbt test

The four built-in tests are: unique, not_null, accepted_values and
relationships (checks a foreign key exists in another table).

For your own rule, write a SQL file in tests/ that returns the BAD
rows. The test passes if it returns nothing:

    -- tests/no_negative_amounts.sql
    select * from {{ ref('stg_orders') }} where amount < 0

=====================================================================
8. INCREMENTAL MODELS (FOR BIG TABLES)
=====================================================================
Rebuilding a huge table every run is wasteful. An incremental model
only processes new rows:

    {{ config(materialized='incremental', unique_key='order_id') }}

    select * from {{ ref('stg_orders') }}

    {% if is_incremental() %}
      where order_date > (select max(order_date) from {{ this }})
    {% endif %}

(This example assumes the model has an order_date column.)

=====================================================================
9. SOURCES, DOCS AND LINEAGE
=====================================================================
Declare raw tables loaded by other tools as sources:

    sources:
      - name: app_db
        tables:
          - name: orders

Use them with {{ source('app_db', 'orders') }}.

Generate and view documentation with a lineage graph:
    dbt docs generate
    dbt docs serve

=====================================================================
10. THE COMMANDS YOU'LL USE MOST
=====================================================================
    dbt run                       # build all models
    dbt test                      # run all tests
    dbt build                     # seed + run + test, in order
    dbt run --select stg_orders   # one model
    dbt run --select +customer_revenue   # it and everything upstream
    dbt run --select stg_orders+         # it and everything downstream
    dbt compile                   # show the final SQL
    dbt clean                     # delete build outputs

=====================================================================
11. GOOD HABITS
=====================================================================
  - Use layers: staging (1:1 with raw, light cleaning) ->
    intermediate -> marts (business models).
  - One model, one clear job. Prefer many small models to one huge
    query.
  - Always use ref() and source(), never hard-code table names.
  - Add unique and not_null tests to every primary key.
  - Document models and columns in the YAML files.
  - Run `dbt build` in CI/CD on every pull request.
  - Add target/ and dbt_packages/ to .gitignore.

=====================================================================
12. PRACTICE EXERCISE
=====================================================================
  1. Install dbt-duckdb and create a project with dbt init.
  2. Add raw_orders and raw_customers as seeds.
  3. Build stg_orders and stg_customers models.
  4. Build a customer_revenue mart that joins them.
  5. Add unique, not_null and relationships tests.
  6. Write one custom test in tests/.
  7. Run `dbt build`, then `dbt docs serve` and look at the lineage.
  8. Make customer_revenue incremental.

Next steps: run dbt from Airflow, and try it on a real warehouse.
"""


def main():
    print(LESSON)


if __name__ == "__main__":
    main()
