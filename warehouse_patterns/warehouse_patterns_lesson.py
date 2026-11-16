"""
Warehouse Patterns Lesson: How data warehouses are built and loaded.

Run this file to print the lesson:  python warehouse_patterns_lesson.py
"""

LESSON = """
=====================================================================
1. WHAT IS A DATA WAREHOUSE?
=====================================================================
A data warehouse is a central database built for ANALYSIS. It brings
together data from many systems (apps, CRM, payments, files) so
people can ask questions across all of it.

Think of a supermarket's central warehouse. Goods arrive from many
suppliers, get checked, sorted and labelled, then go out to shops
in a tidy, predictable way. A data warehouse does the same with
data, and the "shops" are dashboards, reports and models.

This lesson covers the PATTERNS used to organise and load a
warehouse. Table design (star schemas, facts, dimensions, SCDs) is
in the data_modelling lesson. Read that one first.

Why data engineers care:
  - Building and loading the warehouse is a core part of the job.
  - The right patterns keep it fast, cheap, correct and easy to fix.

=====================================================================
2. KEY WORDS
=====================================================================
WAREHOUSE    A database for analytics on structured, cleaned data
             (Snowflake, BigQuery, Redshift, Databricks SQL).
DATA LAKE    Cheap file storage (S3, GCS, ADLS) holding raw data
             of any kind: CSV, JSON, Parquet, images.
LAKEHOUSE    A lake with warehouse features on top (tables, SQL,
             ACID updates) using open table formats such as Delta
             Lake, Apache Iceberg or Apache Hudi.
DATA MART    A smaller, subject-focused part of the warehouse, e.g.
             a finance mart or a marketing mart.
STAGING      A landing area where raw data is loaded before it is
             cleaned and reshaped.
COLUMNAR     Storing data column by column instead of row by row.
PARTITION    Splitting a table into chunks, usually by date.
IDEMPOTENT   Running a load twice gives the same result as once.
UPSERT       Update the row if it exists, insert it if it does not.

=====================================================================
3. OLTP DATABASE vs WAREHOUSE vs LAKE vs LAKEHOUSE
=====================================================================
                 OLTP DB        WAREHOUSE       LAKE         LAKEHOUSE
  Built for      the app        analytics       storage      both
  Data           current state  clean history   raw, any     raw + clean
  Storage        row-based      columnar        files        files (Parquet)
  Schema         strict         on write        on read      both
  Cost           medium         higher          cheapest     low-medium

SCHEMA ON WRITE  Data must fit the table's structure when loaded.
                 (Warehouses.)
SCHEMA ON READ   Store anything. Apply a structure when you read it.
                 (Lakes.)

Many companies use a lake for raw data and a warehouse (or
lakehouse) for cleaned, modelled data.

=====================================================================
4. WHY WAREHOUSES ARE FAST: COLUMNAR STORAGE
=====================================================================
A row store keeps whole rows together. Great for "get order 42".
A column store keeps each column together. Great for "sum of amount
over 1 billion rows".

    SELECT region, SUM(amount) FROM sales GROUP BY region;

A column store reads only the `region` and `amount` columns and skips
the rest. Similar values sit together, so they also compress very
well.

Consequences:
  - Avoid SELECT *. You pay to read every column.
  - Wide, denormalised tables are fine (see data_modelling).
  - Single-row updates are slow. Load in batches instead.

Modern cloud warehouses also SEPARATE STORAGE AND COMPUTE: data sits
in cheap storage, and you start compute (a "warehouse" in Snowflake,
"slots" in BigQuery) only when you query. You can scale each one on
its own and pay for what you use.

=====================================================================
5. THE BIG ARCHITECTURES: INMON vs KIMBALL
=====================================================================
Two classic ways to build a warehouse:

INMON (top-down)
  Build one central, normalised "enterprise data warehouse" first.
  Then build data marts from it for each department.
  + One source of truth, consistent.
  - Slow to build. Value comes late.

KIMBALL (bottom-up)
  Build star-schema data marts one business process at a time.
  Share "conformed dimensions" (the same dim_customer and dim_date
  used by every mart) so they fit together.
  + Fast to deliver. Easy for analysts.
  - Needs discipline to keep dimensions shared and consistent.

Most modern teams use a Kimball-style approach with layers.

CONFORMED DIMENSION  One dimension, used the same way by many fact
                     tables, so "customer" means the same thing in
                     sales and in support.

=====================================================================
6. LAYERS: THE STANDARD WAREHOUSE FLOW
=====================================================================
Data moves through layers, each with one job:

    sources -> RAW / BRONZE -> STAGING / SILVER -> MARTS / GOLD -> BI

  RAW       An exact copy of the source. Never edited. Lets you
            rebuild everything if a bug is found later.
  STAGING   One cleaned table per raw table: renamed columns,
            correct types, duplicates removed.
  INTERMEDIATE (optional)  Joins and business logic shared by marts.
  MARTS     Facts and dimensions ready for users.

This is the medallion pattern (data_modelling) and the dbt layout
(dbt). Use separate schemas: raw, staging, marts. Give users access
to marts only (see data_governance).

=====================================================================
7. LOADING PATTERNS
=====================================================================
How do you get new data into a table? Pick one per table.

FULL REFRESH (truncate and reload)
    Drop everything and load it all again.
    + Simplest, always correct.
    - Slow and costly for big tables.
    Use for: small tables, dimensions with a few thousand rows.

APPEND ONLY (insert)
    Add new rows, never change old ones.
    + Fast and cheap.
    - Duplicates if a load runs twice.
    Use for: event and log data that never changes.

INCREMENTAL / UPSERT (MERGE)
    Load only new or changed rows, update existing ones by key.
    + Fast and handles changes.
    - Needs a reliable key and an "updated_at" column.
    Use for: big tables where rows change (orders, customers).

    MERGE INTO marts.orders AS t
    USING staging.orders_new AS s
      ON t.order_id = s.order_id
    WHEN MATCHED THEN UPDATE SET
      status = s.status, amount = s.amount, updated_at = s.updated_at
    WHEN NOT MATCHED THEN INSERT (order_id, status, amount, updated_at)
      VALUES (s.order_id, s.status, s.amount, s.updated_at);

HIGH-WATER MARK: remember the latest updated_at you loaded, and next
time only fetch rows newer than it.

    SELECT * FROM source.orders
    WHERE updated_at > :last_loaded_at;

=====================================================================
8. MAKE LOADS IDEMPOTENT
=====================================================================
Jobs fail and get re-run. A re-run must not create duplicates or
double the totals.

Ways to do it:
  - MERGE on a unique key instead of plain INSERT.
  - DELETE-then-INSERT for one partition:

        DELETE FROM fact_sales WHERE sale_date = '2025-06-01';
        INSERT INTO fact_sales SELECT ... WHERE sale_date = '2025-06-01';

    (Run both in one transaction.) Re-running the day just replaces
    the same day. This also makes BACKFILLS easy: re-run any past
    date to fix it.
  - Write to a new table, then swap it in (blue-green / swap).

=====================================================================
9. PARTITIONING AND CLUSTERING
=====================================================================
PARTITIONING  Split a big table into chunks, usually by date. A query
              with WHERE sale_date = '2025-06-01' reads only that
              chunk. This is called PARTITION PRUNING.

    -- BigQuery
    CREATE TABLE sales (...) PARTITION BY DATE(sale_ts);

CLUSTERING    Sort data inside the table by columns you filter on a
              lot (e.g. customer_id), so the engine can skip blocks.

Tips:
  - Partition by the column most queries filter on (often a date).
  - Do not make partitions too small. Millions of tiny files or
    partitions are slow.
  - Always filter on the partition column in big queries.

=====================================================================
10. SNAPSHOTS AND HISTORY
=====================================================================
Sources often only show the current state. To keep history:

  DAILY SNAPSHOT  Copy the whole table every day with a snapshot_date
                  column. Simple, uses more storage.
  SCD TYPE 2      Keep a new row only when something changes, with
                  valid_from / valid_to (see data_modelling).
                  dbt snapshots do this for you.

Fact table types you will meet:
  TRANSACTION       One row per event (each sale).
  PERIODIC SNAPSHOT One row per thing per period (stock level per
                    product per day).
  ACCUMULATING SNAPSHOT  One row per process, updated as it moves
                    through steps (order placed, shipped, delivered).

=====================================================================
11. SPEEDING UP QUERIES
=====================================================================
  - Pre-aggregate: build summary tables (daily revenue per region)
    so dashboards do not scan raw facts each time.
  - MATERIALIZED VIEWS: views whose results are stored and kept up
    to date by the warehouse.
  - Only select the columns you need. Filter on partitions.
  - Watch the cost: in pay-per-query warehouses, a careless
    SELECT * on a huge table costs real money.

=====================================================================
12. GOOD HABITS
=====================================================================
  - Keep raw data forever (or as long as policy allows). It lets you
    rebuild.
  - Use layers and separate schemas: raw, staging, marts.
  - Make every load idempotent and safe to re-run.
  - Add load metadata columns: _loaded_at, _source_file, _batch_id.
  - Choose a loading pattern per table and write it down.
  - Partition big fact tables by date.
  - Share conformed dimensions across marts.
  - Test the data after every load (see data_quality).

=====================================================================
13. PRACTICE EXERCISE
=====================================================================
Use DuckDB (pip install duckdb) or Postgres in Docker.
  1. Create schemas raw, staging and marts.
  2. Load a CSV of orders into raw.orders, adding a _loaded_at
     column.
  3. Build staging.orders: correct types, duplicates removed.
  4. Load marts.fact_orders with a MERGE on order_id.
  5. Change a few rows in the CSV, reload, and check the MERGE
     updated them without duplicates.
  6. Run the load twice. Is the row count the same? (Idempotent.)
  7. Build a daily revenue summary table.
  8. Bonus: rebuild the same thing as dbt models (see dbt).

Next steps: read the ETL vs ELT lesson (etl_vs_elt), then try a
cloud warehouse's free tier (BigQuery sandbox or Snowflake trial).
"""


def main():
    print(LESSON)


if __name__ == "__main__":
    main()
