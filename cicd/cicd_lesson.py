"""
CI/CD Lesson: What it is, how to set it up, and how to use it.

Run this file to print the lesson:  python cicd_lesson.py
"""

LESSON = """
=====================================================================
1. WHAT IS CI/CD?
=====================================================================
CI/CD stands for Continuous Integration / Continuous Delivery (or
Deployment). It means your code is tested, built and released
automatically every time you change it.

CI  (Continuous Integration): every time you push code, a robot
    runs your checks (tests, linting) and tells you if you broke
    something.

CD  (Continuous Delivery/Deployment): once the checks pass, the
    robot packages your code and releases it for you.

Think of a factory conveyor belt with quality checks. Each item (your
code change) goes through the same checks. Only items that pass reach
the end.

Why data engineers care:
  - Broken pipeline code never reaches production.
  - No more "I forgot to run the tests".
  - Releases are the same every time, with no manual steps.
  - Docker images, DAGs and Terraform changes can all be deployed
    this way.

=====================================================================
2. KEY WORDS
=====================================================================
PIPELINE    The full automated series of steps.
WORKFLOW    A pipeline file in GitHub Actions.
TRIGGER     What starts it (a push, a pull request, a schedule).
JOB         A group of steps that run on one machine.
STEP        One action or command inside a job.
RUNNER      The machine that runs the job.
ARTIFACT    A file produced by a pipeline (e.g. a built package).
SECRET      A stored password or key the pipeline can use safely.

This lesson uses GitHub Actions because it is free for most uses and
lives right in your GitHub repo. Ideas are the same in GitLab CI,
Jenkins, CircleCI and others.

=====================================================================
3. SETUP
=====================================================================
You need:
  - A GitHub repository.
  - Tests (see the unit_testing folder).

There is nothing to install. Add a YAML file in this folder of your
repo:

    .github/workflows/

Any .yml file in there is run by GitHub automatically.

=====================================================================
4. YOUR FIRST CI WORKFLOW
=====================================================================
Save as .github/workflows/ci.yml:

    name: CI

    on:                          # the trigger
      push:
        branches: [main]
      pull_request:

    jobs:
      test:
        runs-on: ubuntu-latest   # the runner
        steps:
          - uses: actions/checkout@v4          # get your code

          - uses: actions/setup-python@v5
            with:
              python-version: "3.12"

          - name: Install dependencies
            run: pip install -r requirements.txt pytest

          - name: Run tests
            run: pytest

Commit and push it. Then go to your repo's "Actions" tab on GitHub
and watch it run. Green tick = passed. Red cross = failed.

What each part does:
  on:        when to run
  jobs:      what to run
  uses:      re-use a ready-made action
  run:       run a shell command

=====================================================================
5. ADD CODE QUALITY CHECKS
=====================================================================
Add a linter and formatter check as extra steps (ruff is quick):

          - name: Lint
            run: |
              pip install ruff
              ruff check .
              ruff format --check .

If any step fails, the whole job fails and the pull request shows a
red cross.

=====================================================================
6. PROTECT YOUR MAIN BRANCH
=====================================================================
In GitHub: Settings -> Branches -> add a rule for `main`:
  - Require a pull request before merging.
  - Require status checks to pass (pick your "test" job).

Now nobody can merge code that fails the tests.

=====================================================================
7. ADD CD: BUILD AND PUSH A DOCKER IMAGE
=====================================================================
Run only after tests pass, and only on main:

      build:
        needs: test                          # wait for tests
        if: github.ref == 'refs/heads/main'
        runs-on: ubuntu-latest
        steps:
          - uses: actions/checkout@v4

          - uses: docker/login-action@v3
            with:
              username: ${{ secrets.DOCKERHUB_USER }}
              password: ${{ secrets.DOCKERHUB_TOKEN }}

          - uses: docker/build-push-action@v6
            with:
              push: true
              tags: myuser/my-pipeline:latest

Add DOCKERHUB_USER and DOCKERHUB_TOKEN under:
Settings -> Secrets and variables -> Actions.

Never write passwords directly in the YAML file.

=====================================================================
8. WHAT CD CAN DEPLOY IN DATA ENGINEERING
=====================================================================
  - Airflow DAGs: copy DAG files to the Airflow server or bucket.
  - Docker images: build and push to a registry.
  - Terraform: `terraform plan` on pull requests, `terraform apply`
    on merge to main.
  - Kubernetes: `kubectl apply -f` or Helm upgrades.

Example Terraform steps:

          - uses: hashicorp/setup-terraform@v3
          - run: terraform init
          - run: terraform plan

=====================================================================
9. GOOD HABITS
=====================================================================
  - Keep pipelines fast. Slow pipelines get ignored.
  - Cache dependencies where possible (setup-python has
    `cache: pip`).
  - Pin action versions (@v4), as shown above.
  - Keep secrets in the Secrets store, never in code.
  - Use separate environments (dev, prod). Require a manual
    approval step before deploying to prod.
  - Fix a red pipeline straight away. Do not merge on red.

=====================================================================
10. PRACTICE EXERCISE
=====================================================================
  1. Make a repo with a small function and a pytest test.
  2. Add the ci.yml workflow from section 4 and push it.
  3. Watch it pass in the Actions tab.
  4. Break the test on purpose in a pull request. See it fail.
  5. Add the ruff lint step.
  6. Turn on branch protection so failing PRs cannot merge.
  7. Add a Docker build job that runs only on main.

Next steps: learn environments and approvals, then use CI/CD to run
`terraform plan` on pull requests.
"""


def main():
    print(LESSON)


if __name__ == "__main__":
    main()
