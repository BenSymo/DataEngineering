"""
Data Quality Lesson: What it is and how to check your data.

Run this file to print the lesson:  python data_quality_lesson.py
"""

LESSON = """
=====================================================================
1. WHAT IS DATA QUALITY?
=====================================================================
Data quality means your data is correct, complete and trustworthy
enough to use.

Think of food safety. A restaurant checks ingredients before cooking.
A data pipeline should check data before it reaches reports.

Why it matters:
  - Pipelines can succeed with no errors and still produce wrong
    data. "Green" does not mean "correct".
  - Bad data leads to bad decisions, and trust is hard to win back.
  - It is far cheaper to catch problems early than after a CEO
    notices a wrong number in a dashboard.

Unit tests (see unit_testing) check your CODE. Data quality checks
check your DATA. You need both.

=====================================================================
2. THE SIX DIMENSIONS OF QUALITY
=====================================================================
COMPLETENESS   Is anything missing? (nulls, missing rows)
UNIQUENESS     Are there duplicates?
VALIDITY       Does it follow the rules? (formats, ranges, types)
ACCURACY       Does it match reality?
CONSISTENCY    Does it agree across systems and tables?
TIMELINESS     Is it fresh enough? Did it arrive on time?

Examples:
  completeness  customer_id is never null
  uniqueness    order_id appears only once
  validity      email contains "@"; age is between 0 and 120
  consistency   order totals equal the sum of their line items
  timeliness    the table was updated in the last 24 hours

=====================================================================
3. WHERE TO CHECK
=====================================================================
  1. At INGESTION     Check raw data when it arrives. Stop bad
                      files before they spread.
  2. During TRANSFORM Check after each major step.
  3. Before PUBLISHING Check the final tables people will use.

Fail fast: the earlier you find a problem, the less damage it does.

=====================================================================
4. SIMPLE CHECKS IN PYTHON
=====================================================================
You do not need a special tool to start. Plain pandas works:

    import pandas as pd

    def check_orders(df):
        problems = []

        if df["order_id"].isna().any():
            problems.append("order_id has nulls")

        if df["order_id"].duplicated().any():
            problems.append("order_id has duplicates")

        if (df["amount"] < 0).any():
            problems.append("amount has negative values")

        if not df["status"].isin(["completed", "cancelled"]).all():
            problems.append("status has unexpected values")

        if len(df) == 0:
            problems.append("table is empty")

        return problems

    problems = check_orders(df)
    if problems:
        raise ValueError(f"Data quality failed: {problems}")

Raising an error stops the pipeline (and in Airflow, marks the task
failed so you get alerted).

=====================================================================
5. SCHEMA CHECKS
=====================================================================
Many failures happen because a source silently changed: a column
was renamed, or a number turned into text.

    EXPECTED = {"order_id": "int64", "amount": "float64"}

    def check_schema(df):
        for col, dtype in EXPECTED.items():
            assert col in df.columns, f"missing column: {col}"
            assert str(df[col].dtype) == dtype, f"{col} is wrong type"

Libraries such as pandera and pydantic let you declare schemas
instead of writing these by hand.

=====================================================================
6. FRESHNESS AND VOLUME CHECKS
=====================================================================
Also watch for data that is late or the wrong size:

  - FRESHNESS  max(updated_at) is within the last N hours.
  - VOLUME     Today's row count is within, say, 50% to 150% of the
               usual count. A sudden drop often means a broken
               upstream job.

SQL example:

    select
      case when max(updated_at) < now() - interval '24 hours'
           then 'STALE' else 'OK' end as freshness
    from orders;

=====================================================================
7. TOOLS
=====================================================================
dbt tests         Built into dbt: unique, not_null,
                  accepted_values, relationships, plus custom SQL
                  tests. A great first choice if you use dbt.
Great Expectations  A Python library of "expectations" with
                  readable reports. Good for files and DataFrames.
Soda              Checks written in simple YAML-like syntax, run
                  against many databases.
pandera           Declare DataFrame schemas in Python.
Monitoring tools  Tools like Monte Carlo watch tables and alert on
                  odd changes without you writing every rule.

All of these work on the same ideas covered in this lesson.

=====================================================================
8. WHAT TO DO WHEN CHECKS FAIL
=====================================================================
Decide in advance, per check:

  STOP      Fail the pipeline. Use for serious problems (a null
            primary key, an empty table).
  WARN      Continue, but alert someone. Use for minor issues.
  QUARANTINE  Move the bad rows to a separate "rejected" table and
            continue with the good rows. Review the rejects later.

Always log what failed, how many rows, and when. Alert a human
through email, Slack, or your orchestrator.

=====================================================================
9. DATA CONTRACTS
=====================================================================
A data contract is a written agreement between the team that
produces data and the team that uses it: which columns, which types,
what rules, how fresh. Checks enforce the contract. When a producer
wants to change something, the contract makes everyone talk first.

=====================================================================
10. GOOD HABITS
=====================================================================
  - Start with the basics: not null, unique, accepted values, row
    count, freshness.
  - Add a check each time you find a new kind of bad data.
  - Put checks in the pipeline, not in someone's head.
  - Do not alert on everything. Too many alerts get ignored.
  - Keep checks version-controlled and run them in CI/CD.
  - Assign an owner to every important dataset.

=====================================================================
11. PRACTICE EXERCISE
=====================================================================
  1. Make a CSV of 20 orders with a few deliberate problems: a
     null id, a duplicate, a negative amount, a bad status.
  2. Write check_orders() from section 4 and run it.
  3. Add a schema check and a freshness check.
  4. Change it so bad rows go to a rejected.csv file and good rows
     continue.
  5. Write pytest tests for your checks (see unit_testing).
  6. Try the same checks as dbt tests on a dbt model.
  7. Bonus: try Great Expectations or Soda on the same data.

Next steps: add checks to an Airflow DAG so failures alert you.
"""


def main():
    print(LESSON)


if __name__ == "__main__":
    main()
