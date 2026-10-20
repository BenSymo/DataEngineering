"""
Spark Lesson: What it is, how to set it up, and how to use it.

Run this file to print the lesson:  python spark_lesson.py
"""

LESSON = """
=====================================================================
1. WHAT IS APACHE SPARK?
=====================================================================
Spark is a tool for processing very large amounts of data quickly.

The idea: one computer is too slow for huge data. Spark splits the
data into chunks and spreads the work across many CPU cores or many
machines, then combines the results.

Think of it like marking 1,000 exam papers. One teacher takes days.
Ten teachers each marking 100 papers finish ten times faster. Spark
is the head teacher handing out the papers.

You can use Spark with Python through PySpark. It works a lot like
pandas, but on data too big for one machine.

=====================================================================
2. KEY WORDS
=====================================================================
DATAFRAME      A table of rows and columns. Your main tool.
SPARKSESSION   The entry point. You create one to use Spark.
TRANSFORMATION A step that changes data (filter, select, groupBy).
               It is LAZY: nothing runs yet.
ACTION         A step that gets a result (show, count, write).
               This is when Spark actually does the work.
PARTITION      One chunk of the data, processed in parallel.
CLUSTER        A group of machines running Spark together.

Lazy evaluation: Spark first builds a plan from your transformations,
then optimises it, then runs it when you call an action.

=====================================================================
3. INSTALL
=====================================================================
You need Java 17 (or 11) installed. Check with:  java -version

Then install PySpark:

    pip install pyspark

Check it works:

    python -c "import pyspark; print(pyspark.__version__)"

(Or use Docker: docker run -it apache/spark-py /opt/spark/bin/pyspark)

=====================================================================
4. YOUR FIRST SPARK PROGRAM
=====================================================================
    from pyspark.sql import SparkSession

    spark = (
        SparkSession.builder
        .appName("first-app")
        .master("local[*]")      # use all cores on this computer
        .getOrCreate()
    )

    data = [
        ("Alice", "UK", 30),
        ("Bob", "US", 25),
        ("Cara", "UK", 41),
    ]
    df = spark.createDataFrame(data, ["name", "country", "age"])

    df.show()                    # action: print the table
    df.printSchema()             # show column types

    spark.stop()                 # always stop when finished

=====================================================================
5. COMMON DATAFRAME OPERATIONS
=====================================================================
    from pyspark.sql import functions as F

    df.select("name", "age")                  # pick columns
    df.filter(F.col("age") > 28)              # keep some rows
    df.withColumn("age_next", F.col("age") + 1)   # add a column
    df.orderBy(F.col("age").desc())           # sort

    # Group and aggregate
    df.groupBy("country").agg(
        F.count("*").alias("people"),
        F.avg("age").alias("avg_age"),
    ).show()

=====================================================================
6. READING AND WRITING FILES
=====================================================================
    # Read
    df = spark.read.csv("data.csv", header=True, inferSchema=True)
    df = spark.read.json("data.json")
    df = spark.read.parquet("data.parquet")

    # Write (Parquet is the usual choice: fast and compact)
    df.write.mode("overwrite").parquet("output/")

Note: Spark writes a FOLDER of part-files, one per partition.

=====================================================================
7. USING SQL
=====================================================================
If you know SQL, you can use it directly:

    df.createOrReplaceTempView("people")

    spark.sql(
        "SELECT country, COUNT(*) AS n FROM people GROUP BY country"
    ).show()

=====================================================================
8. GOOD HABITS
=====================================================================
  - Use built-in functions (pyspark.sql.functions), not Python loops.
    Built-ins are much faster.
  - Filter and select early, so less data moves around.
  - Avoid .collect() on big data. It pulls everything into memory.
  - Prefer Parquet over CSV for storage.
  - Use the Spark UI at http://localhost:4040 while a job runs to
    see how it is executing.

=====================================================================
9. PRACTICE EXERCISE
=====================================================================
  1. Install PySpark and run the first program.
  2. Create a CSV with 10 rows (name, country, salary).
  3. Read it into a DataFrame.
  4. Find the average salary per country.
  5. Write the result as Parquet and read it back.
  6. Repeat step 4 using spark.sql().

Next steps: learn joins, window functions, and partitioning. Then try
running a Spark job from Airflow.
"""


def main():
    print(LESSON)


if __name__ == "__main__":
    main()
