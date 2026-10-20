"""
Terraform Lesson: What it is, how to set it up, and how to use it.

Run this file to print the lesson:  python terraform_lesson.py
"""

LESSON = """
=====================================================================
1. WHAT IS TERRAFORM?
=====================================================================
Terraform lets you create and manage infrastructure (servers,
databases, storage buckets, networks) by writing code, instead of
clicking around in a cloud web console.

This is called "Infrastructure as Code" (IaC).

Think of it like a blueprint for a house. You describe what you want
("3 bedrooms, 1 kitchen") and Terraform builds it. Change the
blueprint, and Terraform changes the house to match.

Why data engineers care:
  - Create the same data platform again and again (dev, test, prod).
  - Changes are tracked in git, so you can review and undo them.
  - No more "who clicked what in the console?".
  - Works with AWS, Azure, Google Cloud, and many other tools.

=====================================================================
2. KEY WORDS
=====================================================================
PROVIDER    A plugin that lets Terraform talk to a platform
            (e.g. aws, google, azurerm, docker).
RESOURCE    One thing you want to exist (a bucket, a database).
VARIABLE    An input, so you can reuse code with different values.
OUTPUT      A value Terraform prints after it finishes.
STATE       A file (terraform.tfstate) where Terraform remembers what
            it has built. Never edit it by hand.
PLAN        A preview of what Terraform is about to change.
APPLY       Actually make the changes.

Terraform is DECLARATIVE: you say what you want, not the steps.
Terraform works out the steps.

=====================================================================
3. INSTALL
=====================================================================
  - Mac:     brew tap hashicorp/tap && brew install hashicorp/tap/terraform
  - Windows: choco install terraform
  - Linux:   see https://developer.hashicorp.com/terraform/install

Check it works:
    terraform -version

=====================================================================
4. THE FOUR MAIN COMMANDS
=====================================================================
    terraform init       # download providers, set up the folder
    terraform plan       # preview the changes (safe, changes nothing)
    terraform apply      # make the changes (asks you to confirm)
    terraform destroy    # delete everything Terraform built

The usual loop: edit code -> plan -> check -> apply.

=====================================================================
5. YOUR FIRST PROJECT (NO CLOUD ACCOUNT NEEDED)
=====================================================================
We use the Docker provider, so you can practise on your own laptop.
You need Docker running (see the docker folder).

Create a file called main.tf:

    terraform {
      required_providers {
        docker = {
          source  = "kreuzwerker/docker"
          version = "~> 3.0"
        }
      }
    }

    provider "docker" {}

    resource "docker_image" "postgres" {
      name = "postgres:16"
    }

    resource "docker_container" "db" {
      name  = "tf-postgres"
      image = docker_image.postgres.image_id

      env = ["POSTGRES_PASSWORD=secret"]

      ports {
        internal = 5432
        external = 5432
      }
    }

Run it:
    terraform init
    terraform plan
    terraform apply        # type "yes" to confirm

Check with `docker ps`. You now have a Postgres container built from
code. Clean up with:
    terraform destroy

Notice docker_image.postgres.image_id: one resource refers to another,
so Terraform knows to build the image first.

=====================================================================
6. VARIABLES AND OUTPUTS
=====================================================================
Make code reusable with variables (variables.tf):

    variable "db_password" {
      type      = string
      sensitive = true          # hides it in the output
    }

Use it in a resource:

    env = ["POSTGRES_PASSWORD=${var.db_password}"]

Set it without hard-coding, e.g. with an environment variable:
    export TF_VAR_db_password="secret"

Print a value after apply (outputs.tf):

    output "container_name" {
      value = docker_container.db.name
    }

=====================================================================
7. A REAL CLOUD EXAMPLE (AWS S3 BUCKET)
=====================================================================
    provider "aws" {
      region = "eu-west-2"
    }

    resource "aws_s3_bucket" "raw_data" {
      bucket = "my-company-raw-data-12345"   # must be unique globally
    }

Same four commands: init, plan, apply, destroy. You need AWS
credentials set up first (for example with `aws configure`).

Watch out: cloud resources can cost money. Always run
`terraform destroy` when you finish practising.

=====================================================================
8. GOOD HABITS
=====================================================================
  - Always run `terraform plan` and read it before `apply`.
  - Keep your code in git. Do NOT commit these:
        .terraform/      terraform.tfstate      *.tfvars (secrets)
    Add them to .gitignore.
  - Never hard-code passwords or keys in .tf files.
  - For teams, store state remotely (e.g. an S3 bucket) so everyone
    shares the same state.
  - Run `terraform fmt` to tidy code and `terraform validate` to
    catch mistakes.

=====================================================================
9. PRACTICE EXERCISE
=====================================================================
  1. Install Terraform and run `terraform -version`.
  2. Build the Docker Postgres example from section 5.
  3. Move the password into a variable and set it via TF_VAR_.
  4. Add an output that prints the container name.
  5. Change the external port to 5433 and run `terraform plan`.
     What does Terraform say it will do?
  6. Run `terraform destroy`.

Next steps: learn modules (reusable bundles of resources) and remote
state. Then use Terraform to create the cloud infrastructure for the
Airflow and Spark projects.
"""


def main():
    print(LESSON)


if __name__ == "__main__":
    main()
