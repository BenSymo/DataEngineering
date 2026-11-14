# Data Engineering

A personal learning repo for data engineering technologies. Each technology has its own folder with a short, plain-English lesson written as a Python file.

## Repo structure

```
DataEngineering/
├── README.md
├── LEARNING_PATH.md
├── docker/
│   └── docker_lesson.py
├── unit_testing/
│   └── unit_testing_lesson.py
├── data_modelling/
│   └── data_modelling_lesson.py
├── spark/
│   └── spark_lesson.py
├── kafka/
│   └── kafka_lesson.py
├── dbt/
│   └── dbt_lesson.py
├── airflow/
│   └── airflow_lesson.py
├── data_quality/
│   └── data_quality_lesson.py
├── cicd/
│   └── cicd_lesson.py
├── kubernetes/
│   └── kubernetes_lesson.py
├── terraform/
│   └── terraform_lesson.py
├── data_governance/
│   └── data_governance_lesson.py
└── dsa/
    └── dsa_lesson.py
```

## The lessons

| Folder | Topic | What it covers |
|--------|-------|----------------|
| `docker/` | Docker | Containers, images, Dockerfiles, Docker Compose |
| `unit_testing/` | Unit testing | pytest, fixtures, mocking, testing pipelines |
| `data_modelling/` | Data modelling | Star schemas, facts and dimensions, SCDs |
| `spark/` | Apache Spark | Processing large data with PySpark |
| `kafka/` | Apache Kafka | Streaming events with topics, producers, consumers |
| `dbt/` | dbt | SQL transformations, tests and docs |
| `airflow/` | Apache Airflow | Scheduling and orchestrating pipelines |
| `data_quality/` | Data quality | Checks, freshness, what to do on failure |
| `cicd/` | CI/CD | GitHub Actions to test and deploy code |
| `kubernetes/` | Kubernetes | Running containers at scale |
| `terraform/` | Terraform | Infrastructure as code |
| `data_governance/` | Governance and security | Access control, PII, secrets, retention |
| `dsa/` | Data structures and algorithms | Big O, dicts and sets, sorting, graphs, with data pipeline examples |

## How to use it

1. Open [`LEARNING_PATH.md`](LEARNING_PATH.md) to see what each topic needs and the suggested order.
2. Run a lesson to read it in your terminal:

   ```
   python docker/docker_lesson.py
   ```

3. Follow the setup steps and do the practice exercise at the end of each lesson.

The lessons only print text, so they need Python 3 and nothing else. The tools they teach (Docker, Spark and so on) are installed separately, as each lesson explains.

## Adding a new topic

1. Create a folder named after the technology, in `snake_case`.
2. Add `<name>_lesson.py` with the lesson text in a `LESSON` string and a `main()` that prints it. Copy an existing lesson as a template.
3. Keep the same lesson layout: what it is, key words, install, hands-on examples, good habits, practice exercise.
4. Add the topic to the table above and to `LEARNING_PATH.md`.

Practice code you write while following a lesson can go in the same folder, next to the lesson file.
