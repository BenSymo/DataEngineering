"""
Airflow Lesson: What it is, how to set it up, and how to use it.

Run this file to print the lesson:  python airflow_lesson.py
"""

LESSON = """
=====================================================================
1. WHAT IS APACHE AIRFLOW?
=====================================================================
Airflow is a tool that schedules and runs your data jobs in the
right order, and tells you when something fails.

Think of it as a smart to-do list for your data pipelines:
  "Every day at 6am: download the file, clean it, load it to the
   database. Only start step 2 when step 1 succeeds. Retry if it
   fails."

You write the pipeline as Python code, and Airflow handles the
scheduling, retries, logging and monitoring. It also has a web page
where you can watch everything run.

=====================================================================
2. KEY WORDS
=====================================================================
DAG        "Directed Acyclic Graph". Simply: a pipeline. A set of
           tasks with an order and no loops.
TASK       One step in a pipeline (e.g. "download file").
OPERATOR   A template for a task type (run Python, run Bash, etc).
SCHEDULE   When the DAG runs (e.g. daily, hourly).
SCHEDULER  The Airflow process that starts tasks at the right time.
WEBSERVER  The Airflow web page (UI) at localhost:8080.

=====================================================================
3. INSTALL (EASIEST WAY: DOCKER)
=====================================================================
This uses what you learned in the docker folder.

    mkdir airflow-demo && cd airflow-demo
    curl -LfO 'https://airflow.apache.org/docs/apache-airflow/stable/docker-compose.yaml'
    mkdir -p dags logs plugins config
    echo "AIRFLOW_UID=$(id -u)" > .env
    docker compose up airflow-init
    docker compose up -d

Open http://localhost:8080
Default login: username airflow / password airflow

Your DAG files go in the `dags/` folder. Airflow picks them up
automatically.

=====================================================================
4. YOUR FIRST DAG
=====================================================================
Save this as dags/hello_dag.py:

    from datetime import datetime
    from airflow.decorators import dag, task

    @dag(
        schedule="@daily",
        start_date=datetime(2025, 1, 1),
        catchup=False,
    )
    def hello_pipeline():

        @task
        def extract():
            return [1, 2, 3]

        @task
        def transform(numbers):
            return [n * 10 for n in numbers]

        @task
        def load(numbers):
            print(f"Loading {numbers}")

        load(transform(extract()))

    hello_pipeline()

What it does: extract -> transform -> load. Passing the output of one
task into the next also sets the order.

Key settings:
  schedule="@daily"   run once a day
  start_date          the first date the DAG is valid from
  catchup=False       don't run for every missed past day

=====================================================================
5. USING THE UI
=====================================================================
  1. Find "hello_pipeline" in the DAG list.
  2. Flip the toggle to un-pause it.
  3. Click the play button to trigger a run.
  4. Click the DAG, then the Graph view to see the tasks.
  5. Green = success, red = failed. Click a task, then Logs.

=====================================================================
6. USEFUL COMMANDS
=====================================================================
    docker compose up -d          # start Airflow
    docker compose down           # stop Airflow
    docker compose logs -f        # follow the logs

    # Run an Airflow command inside the container:
    docker compose run airflow-cli airflow dags list
    docker compose run airflow-cli airflow dags test hello_pipeline

=====================================================================
7. RETRIES AND ORDER
=====================================================================
Add retries to make tasks more robust:

    @task(retries=3, retry_delay=timedelta(minutes=5))
    def extract(): ...

Set order by hand with >>:

    task_a >> task_b >> task_c       # a, then b, then c
    task_a >> [task_b, task_c]       # b and c run in parallel

=====================================================================
8. GOOD HABITS
=====================================================================
  - Keep tasks small and re-runnable (same result if run twice).
  - Do heavy work in other tools (Spark, a database), not in Airflow.
    Airflow is the conductor, not the orchestra.
  - Never put passwords in DAG files. Use Connections and Variables
    (Admin menu in the UI).

=====================================================================
9. PRACTICE EXERCISE
=====================================================================
  1. Get Airflow running with Docker and log in.
  2. Add the hello_pipeline DAG and run it.
  3. Make `extract` read a small CSV file instead.
  4. Add retries to one task and make it fail on purpose.
     Watch the retries in the UI.
  5. Add a fourth task that runs after `load`.

Next steps: learn about Connections, sensors (waiting for a file),
and running Spark jobs from Airflow.
"""


def main():
    print(LESSON)


if __name__ == "__main__":
    main()
