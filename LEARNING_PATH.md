# Learning Path

The order to learn the technologies in this repo, based on what each one needs.

## Dependencies

| Tech | Needs first | Also needs |
|------|-------------|------------|
| Docker | Python and terminal basics | Docker Desktop (or Docker Engine on Linux) |
| Spark | Python, basic SQL | Java 11 or 17 (or Docker) |
| Kafka | Python, Docker | `confluent-kafka` Python package |
| Airflow | Python, Docker | Docker Compose, about 4 GB of free RAM |
| Terraform | Docker (for the practice project) | A cloud account (AWS etc.) for real use |

## Recommended order

1. **Docker** (`docker/`): Everything else is easier with it. Kafka and Airflow are installed with it, and the Terraform practice project uses it.
2. **Spark** (`spark/`): Learn how to process data. It has no tool dependencies except Java (or Docker). This gives you something real to schedule later.
3. **Kafka** (`kafka/`): Learn how live data is moved around. It pairs with Spark, which can read from Kafka for streaming jobs.
4. **Airflow** (`airflow/`): Schedules and runs your jobs, such as Spark scripts. It is easier to follow once you know what jobs you want to run.
5. **Terraform** (`terraform/`): Builds the cloud infrastructure that the others run on. It makes the most sense last, once you know what you need to build.

```
Python + SQL basics
        |
      Docker
     /  |   \
Spark Kafka  Terraform (practice project)
     \  |   /
     Airflow  ->  Terraform builds the cloud setup for all of them
```

## Notes

- Terraform can be learned any time after Docker. If you want to try cloud tools early, move it up to second.
- Kafka can be learned before Spark. Do Spark first if you want to use Spark Structured Streaming with Kafka.
- Python and SQL are not in this repo, but you need basic skills in both before you start.
- Start with the lesson in each folder (`python <folder>/<name>_lesson.py`) and do its practice exercise before moving on.
