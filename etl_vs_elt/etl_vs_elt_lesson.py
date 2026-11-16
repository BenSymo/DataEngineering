"""
ETL vs ELT Lesson: Two ways to move and shape data, and when to use each.

Run this file to print the lesson:  python etl_vs_elt_lesson.py
"""

LESSON = """
=====================================================================
1. WHAT ARE ETL AND ELT?
=====================================================================
Every data pipeline does three things:

  EXTRACT    Get data out of a source (database, API, files).
  TRANSFORM  Clean and reshape it (fix types, join, aggregate).
  LOAD       Put it into the target (a warehouse or lake).

The difference is the ORDER:

  ETL   Extract -> Transform -> Load
        Transform on a separate server BEFORE loading. Only clean
        data reaches the warehouse.

  ELT   Extract -> Load -> Transform
        Load the raw data first, then transform it INSIDE the
        warehouse using SQL.

Think of cooking. ETL is a takeaway: the food is cooked in the
restaurant kitchen and arrives ready to eat. ELT is a meal kit: the
raw ingredients are delivered to your kitchen and you cook them
there, any way you like, as often as you like.

=====================================================================
2. KEY WORDS
=====================================================================
SOURCE         Where data comes from.
TARGET / SINK  Where data goes.
STAGING AREA   A temporary place to hold data mid-pipeline.
BATCH          Moving data in chunks on a schedule (e.g. nightly).
STREAMING      Moving data continuously as events happen.
CDC            Change Data Capture: read only the changes (inserts,
               updates, deletes) from a database's log.
REVERSE ETL    Copy data FROM the warehouse back INTO business tools
               (CRM, ad platforms).
ORCHESTRATOR   A tool that schedules and runs the steps (Airflow).
CONNECTOR      A ready-made extractor/loader for one source.

=====================================================================
3. A SHORT HISTORY: WHY ELT TOOK OVER
=====================================================================
ETL came first (1990s-2000s). Warehouses were expensive and slow,
storage was costly, and their compute was limited. So data was
cleaned on a separate ETL server (Informatica, SSIS, Talend) and
only the final result was loaded.

Then cloud warehouses arrived (BigQuery, Snowflake, Redshift):
  - Storage became very cheap.
  - Compute became huge, elastic and pay-as-you-go.
  - Storage and compute were separated.

Now it is cheaper and easier to load everything raw and let the
warehouse do the heavy lifting with SQL. Tools like dbt made SQL
transformations testable and version-controlled. ELT is now the
default for most analytics work.

=====================================================================
4. ETL IN DETAIL
=====================================================================
    source -> [ ETL server: clean, join, aggregate ] -> warehouse

Example in Python:

    import pandas as pd

    def extract():
        return pd.read_csv("orders.csv")

    def transform(df):
        df = df.dropna(subset=["order_id"])
        df = df.drop_duplicates("order_id")
        df["amount"] = df["amount"].astype(float)
        df["email"] = df["email"].str[0] + "***"   # mask PII
        return df[df["status"] == "completed"]

    def load(df, conn):
        df.to_sql("orders", conn, if_exists="append", index=False)

    load(transform(extract()), conn)

Pros:
  + Sensitive data can be removed or masked BEFORE it lands. Good
    for strict privacy rules (see data_governance).
  + Less data stored in the warehouse.
  + Works when the target cannot transform well (an old database,
    an app, a file).
  + Handles non-SQL work: images, complex parsing, ML features.

Cons:
  - Raw data is not kept. If the logic was wrong, you must
    re-extract from the source, which may no longer have it.
  - Every new question needs a change to the pipeline, often by an
    engineer.
  - The ETL server can become a bottleneck.

Tools: Informatica, SSIS, Talend, AWS Glue, Spark jobs, plain Python.

=====================================================================
5. ELT IN DETAIL
=====================================================================
    source -> warehouse (raw) -> [ SQL inside warehouse ] -> marts

Step 1, Extract and Load (no changes):

    raw = pd.read_csv("orders.csv")
    raw["_loaded_at"] = pd.Timestamp.now(tz="UTC")
    raw.to_sql("orders", conn, schema="raw",
               if_exists="append", index=False)

Step 2, Transform with SQL (often as a dbt model):

    -- models/staging/stg_orders.sql
    select distinct
        order_id,
        cast(amount as numeric) as amount,
        status
    from {{ source('raw', 'orders') }}
    where order_id is not null

Pros:
  + Raw data is kept, so you can rebuild or change logic any time.
  + Loading is fast and simple (often a no-code connector).
  + Analysts who know SQL can build models themselves.
  + Uses the warehouse's large, scalable compute.
  + Fits well with dbt: tests, docs, lineage.

Cons:
  - Raw sensitive data lands in the warehouse. You must lock down
    the raw schema and mask data in later layers.
  - Storage and compute costs can grow if nobody watches them.
  - SQL is not great for every task (complex parsing, ML).
  - Raw areas can turn into a messy "data swamp" without rules.

Tools:
  EL:  Fivetran, Airbyte, Stitch, dlt, Meltano, cloud native loaders
  T:   dbt, SQLMesh, the warehouse's own SQL

=====================================================================
6. SIDE BY SIDE
=====================================================================
                    ETL                        ELT
  Transform where   separate server/engine     inside the warehouse
  Load what         clean data only            raw data, then clean
  Raw data kept?    usually not                yes
  Speed to load     slower                     faster
  Flexibility       low (change pipeline)      high (change SQL)
  Main skill        Python/Java, ETL tools     SQL (+ dbt)
  Privacy           easier (mask before load)  needs care in raw
  Best for          strict privacy, small or   cloud warehouses,
                    weak targets, non-SQL work analytics, fast change

=====================================================================
7. WHICH SHOULD I CHOOSE?
=====================================================================
Choose ELT when:
  - You have a modern cloud warehouse or lakehouse.
  - Needs change often and analysts work in SQL.
  - You want to keep raw history to rebuild from.

Choose ETL when:
  - Law or policy says some data must never land in the warehouse
    (e.g. card numbers, health data).
  - The target is limited (an operational database, a file, an
    app that cannot run transforms).
  - The work is not a good fit for SQL (images, NLP, heavy Python).
  - You must shrink huge raw data before storing it (e.g. IoT
    sensor readings averaged per minute).

In practice most teams mix them. A common mix is "EtLT": do small
transforms on the way in (drop or hash PII, fix encodings, flatten
JSON), load, then do the main business logic in the warehouse.

=====================================================================
8. RELATED PATTERNS
=====================================================================
CDC (Change Data Capture)
    Instead of copying a whole table every night, read the
    database's change log and send only inserts, updates and
    deletes. Low load on the source, near real time. Tools:
    Debezium (often with Kafka), Fivetran, AWS DMS.

STREAMING ETL
    Transform events as they flow (Kafka + Spark Structured
    Streaming or Flink), then load. Used for real-time needs like
    fraud alerts.

REVERSE ETL
    Send modelled data from the warehouse back to tools people use:
    customer scores into Salesforce, audiences into ad platforms.
    Tools: Hightouch, Census.

ZERO-ETL
    Cloud features that copy data from an operational database to
    the warehouse automatically, with no pipeline to build.

=====================================================================
9. GOOD HABITS (BOTH STYLES)
=====================================================================
  - Keep Extract simple. Do not mix business logic into extractors.
  - Make each step idempotent: safe to re-run (see
    warehouse_patterns).
  - Load incrementally where possible (high-water mark or CDC).
  - Add metadata: _loaded_at, _source, _batch_id.
  - Check data quality after load and after transform (see
    data_quality).
  - Lock down raw data, and mask PII before analysts see it.
  - Orchestrate all steps with a tool like Airflow, with retries
    and alerts.
  - Keep transformations in git and test them (dbt, pytest).

=====================================================================
10. PRACTICE EXERCISE
=====================================================================
Use DuckDB (pip install duckdb pandas) for both versions.
  1. Make a CSV of 20 orders with some problems: a missing id, a
     duplicate, an amount stored as text, and an email column.
  2. ETL: write extract(), transform() and load() in Python. Clean
     and mask emails in pandas, then load only clean rows to an
     `orders` table.
  3. ELT: load the CSV unchanged into raw.orders. Then write a SQL
     query (or a dbt model) that builds a clean staging.orders.
  4. Change a rule (e.g. also keep cancelled orders). Which version
     was easier to fix? Which one needed the source file again?
  5. Write down where PII ends up in each version.
  6. Bonus: run both pipelines from an Airflow DAG.

Next steps: try an EL tool like Airbyte or dlt to load data, and
dbt to transform it.
"""


def main():
    print(LESSON)


if __name__ == "__main__":
    main()
