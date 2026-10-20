"""
Docker Lesson: What it is, how to set it up, and how to use it.

Run this file to print the lesson:  python docker_lesson.py
"""

LESSON = """
=====================================================================
1. WHAT IS DOCKER?
=====================================================================
Docker lets you package an app, plus everything it needs to run
(Python, libraries, settings), into one box called a CONTAINER.

The classic problem: "It works on my machine!" but breaks on someone
else's. Docker fixes this. The container runs the same everywhere.

Think of it like a shipping container: it doesn't matter what ship or
truck carries it, the contents inside stay the same.

Why data engineers care:
  - Run databases (Postgres, MySQL) without installing them.
  - Run tools like Airflow, Spark or Kafka in minutes.
  - Share a pipeline that works the same on every laptop and server.

=====================================================================
2. KEY WORDS
=====================================================================
IMAGE       A read-only blueprint (recipe) for a container.
CONTAINER   A running instance of an image. Like an app that is open.
DOCKERFILE  A text file with steps to build your own image.
REGISTRY    A store for images. Docker Hub is the main one.
VOLUME      Storage that keeps data after a container is deleted.

Image vs container: an image is the recipe, a container is the meal.

=====================================================================
3. INSTALL DOCKER
=====================================================================
  - Mac / Windows: install "Docker Desktop" from docker.com
  - Linux: follow the guide at https://docs.docker.com/engine/install/

Check it works:
    docker --version
    docker run hello-world

=====================================================================
4. BASIC COMMANDS
=====================================================================
    docker pull postgres           # download an image
    docker images                  # list images you have
    docker run postgres            # create + start a container
    docker ps                      # list running containers
    docker ps -a                   # list all containers (incl. stopped)
    docker stop <name_or_id>       # stop a container
    docker start <name_or_id>      # start it again
    docker rm <name_or_id>         # delete a container
    docker rmi <image>             # delete an image
    docker logs <name_or_id>       # see a container's output
    docker exec -it <name> bash    # open a shell inside a container

=====================================================================
5. USEFUL FLAGS FOR `docker run`
=====================================================================
    -d              run in the background ("detached")
    --name NAME     give the container a friendly name
    -p 5432:5432    map a port: HOST_PORT:CONTAINER_PORT
    -e KEY=VALUE    set an environment variable
    -v VOL:/path    attach a volume so data is kept
    --rm            auto-delete the container when it stops

=====================================================================
6. EXAMPLE: RUN A POSTGRES DATABASE
=====================================================================
    docker run -d \\
      --name my-postgres \\
      -e POSTGRES_PASSWORD=secret \\
      -p 5432:5432 \\
      -v pgdata:/var/lib/postgresql/data \\
      postgres:16

You now have a database at localhost:5432. No install needed.
Because of the volume (pgdata), your data survives if you delete
and re-create the container.

Stop and clean up:
    docker stop my-postgres
    docker rm my-postgres

=====================================================================
7. BUILD YOUR OWN IMAGE WITH A DOCKERFILE
=====================================================================
Create a file named "Dockerfile" (no extension):

    FROM python:3.12-slim          # start from an existing image
    WORKDIR /app                   # set the working folder
    COPY requirements.txt .        # copy the dependency list
    RUN pip install -r requirements.txt
    COPY . .                       # copy your code
    CMD ["python", "main.py"]      # the command to run

Build it and run it:
    docker build -t my-pipeline .
    docker run --rm my-pipeline

=====================================================================
8. DOCKER COMPOSE: RUN SEVERAL CONTAINERS TOGETHER
=====================================================================
Real projects need more than one container (app + database).
Docker Compose describes them all in one file: docker-compose.yml

    services:
      db:
        image: postgres:16
        environment:
          POSTGRES_PASSWORD: secret
        ports:
          - "5432:5432"
        volumes:
          - pgdata:/var/lib/postgresql/data

      app:
        build: .
        depends_on:
          - db

    volumes:
      pgdata:

Commands:
    docker compose up -d      # start everything
    docker compose ps         # see what's running
    docker compose logs       # see output
    docker compose down       # stop and remove containers

=====================================================================
9. CLEAN UP (DOCKER CAN USE LOTS OF DISK)
=====================================================================
    docker system prune       # remove stopped containers, unused data

=====================================================================
10. PRACTICE EXERCISE
=====================================================================
  1. Run `docker run hello-world`.
  2. Start a Postgres container with the command from section 6.
  3. Open a shell in it:  docker exec -it my-postgres psql -U postgres
  4. Create a table, then stop and remove the container.
  5. Re-create it with the same volume. Is your table still there?
  6. Write a small Dockerfile for a Python script and run it.

Next steps: learn Docker Compose in depth, then try running Airflow
or Kafka with it.
"""


def main():
    print(LESSON)


if __name__ == "__main__":
    main()
