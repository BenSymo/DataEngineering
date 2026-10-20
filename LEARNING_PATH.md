# Learning Path

The order to learn the technologies in this repo, based on what each one needs.

## Before you start

You should already be comfortable with Python and SQL, and know basic Git and the terminal.

## Dependencies

| Tech | Needs first | Also needs |
|------|-------------|------------|
| Docker | Terminal basics | Docker Desktop (or Docker Engine on Linux) |
| Unit testing | Python | `pytest` package |
| Data modelling | SQL | A database to practise on (DuckDB or Postgres in Docker) |
| Spark | Python, SQL | Java 11 or 17 (or Docker) |
| Kafka | Python, Docker | `confluent-kafka` Python package |
| dbt | SQL, data modelling | `dbt-duckdb` package (or a warehouse adapter) |
| Airflow | Python, Docker | Docker Compose, about 4 GB of free RAM |
| Data quality | Python, SQL, unit testing | Works best alongside dbt and Airflow |
| CI/CD | Git and GitHub, unit testing | A GitHub repo (Docker too, for the image build) |
| Kubernetes | Docker | `kubectl` and `minikube`, about 2 CPUs and 2 GB of free RAM |
| Terraform | Docker (for the practice project) | A cloud account (AWS etc.) for real use |
| Data governance and security | Data modelling, some cloud or database knowledge | Better with CI/CD, Terraform and a warehouse to practise on |

## Recommended order

1. **Docker** (`docker/`): Everything else is easier with it. Kafka, Airflow and Kubernetes build on it, and the Terraform practice project uses it.
2. **Unit testing** (`unit_testing/`): Learn this early. It makes all the code you write for the later steps safer.
3. **Data modelling** (`data_modelling/`): Learn how to design tables before you build pipelines that fill them.
4. **Spark** (`spark/`): Learn how to process large data. It has no tool dependencies except Java (or Docker).
5. **Kafka** (`kafka/`): Learn how live data is moved around. It pairs with Spark, which can read from Kafka for streaming jobs.
6. **dbt** (`dbt/`): Build your data models in SQL, with tests and docs. It puts your data modelling lesson into practice.
7. **Airflow** (`airflow/`): Schedule and run your jobs, including Spark scripts and dbt builds.
8. **Data quality** (`data_quality/`): Add checks to your pipelines. It is easiest to practise once you have dbt and Airflow, so you can add checks to both.
9. **CI/CD** (`cicd/`): Automatically test and release your code. It needs tests to run (step 2) and gets more useful once you have code to deploy.
10. **Kubernetes** (`kubernetes/`): Run your containers at scale. It is a big topic, so it comes after you are comfortable with Docker and the tools above.
11. **Terraform** (`terraform/`): Build the cloud infrastructure that the others run on.
12. **Data governance and security** (`data_governance/`): Protect and manage the data across all of the above. It ties everything together, so it is best learned last, once you have real pipelines to apply it to.

```
Terminal + Git, Python, SQL
            |
          Docker ---------- Unit testing
       /    |     \              |
   Spark  Kafka  Kubernetes      |
       \    |                    |
   Data modelling -> dbt         |
            |         \          |
            +--- Airflow ---- Data quality
                     |           |
                     +--- CI/CD -+
                            |
                       Terraform
                            |
              Data governance and security
```

## Notes

- Data modelling is mostly design work, so you can learn it at any time before dbt. Moving it first is fine.
- Terraform can be learned any time after Docker. If you want to try cloud tools early, move it up.
- Kafka can be learned before Spark. Do Spark first if you want to use Spark Structured Streaming with Kafka.
- Kubernetes can be moved earlier if you want to run Airflow, Spark or Kafka on it.
- CI/CD can be learned right after unit testing, so you can use it from the start on all the later projects.
- Data governance is placed last because it applies to everything. Read its lesson earlier if you work with personal data, and use the checklist (section 12) from the start.
- Start with the lesson in each folder (`python <folder>/<name>_lesson.py`) and do its practice exercise before moving on.
