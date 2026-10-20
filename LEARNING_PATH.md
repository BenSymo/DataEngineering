# Learning Path

The order to learn the technologies in this repo, based on what each one needs.

## Dependencies

| Tech | Needs first | Also needs |
|------|-------------|------------|
| Docker | Python and terminal basics | Docker Desktop (or Docker Engine on Linux) |
| Unit testing | Python | `pytest` package |
| Spark | Python, basic SQL | Java 11 or 17 (or Docker) |
| Kafka | Python, Docker | `confluent-kafka` Python package |
| Airflow | Python, Docker | Docker Compose, about 4 GB of free RAM |
| CI/CD | Git and GitHub, unit testing | A GitHub repo (Docker too, for the image build) |
| Terraform | Docker (for the practice project) | A cloud account (AWS etc.) for real use |
| Kubernetes | Docker | `kubectl` and `minikube`, about 2 CPUs and 2 GB of free RAM |

## Recommended order

1. **Docker** (`docker/`): Everything else is easier with it. Kafka, Airflow and Kubernetes all build on it, and the Terraform practice project uses it.
2. **Unit testing** (`unit_testing/`): Learn this early. It makes all the code you write for the later steps safer.
3. **Spark** (`spark/`): Learn how to process data. It has no tool dependencies except Java (or Docker). This gives you something real to test and schedule later.
4. **Kafka** (`kafka/`): Learn how live data is moved around. It pairs with Spark, which can read from Kafka for streaming jobs.
5. **Airflow** (`airflow/`): Schedules and runs your jobs, such as Spark scripts. It is easier to follow once you know what jobs you want to run.
6. **CI/CD** (`cicd/`): Automatically tests and releases your code. It needs tests to run (step 2) and gets more useful once you have code to deploy.
7. **Kubernetes** (`kubernetes/`): Runs your containers at scale. It is a big topic, so it comes after you are comfortable with Docker and the tools above.
8. **Terraform** (`terraform/`): Builds the cloud infrastructure that the others run on. It makes the most sense last, once you know what you need to build.

```
Python + SQL + Git basics
          |
        Docker ----------- Unit testing
     /   |    \                 |
 Spark Kafka  Kubernetes      CI/CD
     \   |                      |
     Airflow  ------------------+
          |
      Terraform  (builds the cloud setup for all of them)
```

## Notes

- Terraform can be learned any time after Docker. If you want to try cloud tools early, move it up.
- Kafka can be learned before Spark. Do Spark first if you want to use Spark Structured Streaming with Kafka.
- Kubernetes can be moved earlier if you want to run Airflow, Spark or Kafka on it. Airflow and Kafka both have Kubernetes installs.
- CI/CD can be learned right after unit testing. You can then use it from the start on all the later projects.
- Python, SQL and Git are not in this repo, but you need basic skills in all three before you start.
- Start with the lesson in each folder (`python <folder>/<name>_lesson.py`) and do its practice exercise before moving on.
