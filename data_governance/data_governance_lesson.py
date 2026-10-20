"""
Data Governance and Security Lesson: Keeping data safe, controlled
and well managed.

Run this file to print the lesson:  python data_governance_lesson.py
"""

LESSON = """
=====================================================================
1. WHAT ARE DATA GOVERNANCE AND DATA SECURITY?
=====================================================================
DATA GOVERNANCE is the set of rules and responsibilities for how
data is managed: who owns it, who can use it, how long it is kept,
and how its quality is ensured.

DATA SECURITY is the set of technical protections that enforce those
rules: access control, encryption, masking, monitoring.

Think of a bank. Governance is the policy ("only staff with a reason
may see account details; records are kept 7 years"). Security is the
locks, vault, cameras and logs that make the policy real.

Why data engineers care:
  - You build the pipelines that touch personal and sensitive data.
  - Mistakes can lead to leaks, fines and loss of trust.
  - Laws such as GDPR (EU/UK) and CCPA (California) have real
    penalties.
  - Good governance also makes data easier to find and trust.

=====================================================================
2. KEY WORDS
=====================================================================
PII         Personally Identifiable Information: names, emails,
            phone numbers, addresses, IDs, IP addresses.
SENSITIVE   Data needing extra care: health, financial, passwords,
            biometrics, children's data.
DATA OWNER  The person accountable for a dataset.
DATA STEWARD  Someone who looks after its quality and definitions.
CLASSIFICATION  Labelling data by sensitivity (public, internal,
            confidential, restricted).
LINEAGE     Where data came from and what it was turned into.
CATALOG     A searchable inventory of your data and its meaning.
RETENTION   How long data is kept before it is deleted.
AUDIT LOG   A record of who accessed or changed what, and when.

=====================================================================
3. THE LAWS IN SIMPLE TERMS
=====================================================================
GDPR (EU/UK) in short:
  - Only collect data you actually need (data minimisation).
  - Have a lawful reason to use it, and say what you use it for.
  - Do not keep it longer than needed.
  - People can ask to see, correct or DELETE their data.
  - Report serious breaches within 72 hours.
  - Protect data with suitable security measures.

Other rules you may meet: CCPA (California), HIPAA (US health data),
PCI-DSS (card payments). Ask your company's legal or privacy team
which apply. This lesson is not legal advice.

=====================================================================
4. THE SECURITY BASICS (THE CIA TRIAD)
=====================================================================
CONFIDENTIALITY  Only the right people can see it.
INTEGRITY        Data is not changed by mistake or by attackers.
AVAILABILITY     Data is there when people need it.

=====================================================================
5. ACCESS CONTROL: LEAST PRIVILEGE
=====================================================================
Give each person and each pipeline the minimum access they need.

Use ROLES, not individual grants:

    CREATE ROLE analyst;
    GRANT USAGE ON SCHEMA marts TO analyst;
    GRANT SELECT ON ALL TABLES IN SCHEMA marts TO analyst;

    GRANT analyst TO alice;

Analysts see the final marts but not the raw data containing PII.

Also:
  - Separate dev, test and prod, with different access.
  - Give pipelines their own service accounts, not a person's login.
  - Remove access when people change teams or leave.
  - Use multi-factor authentication (MFA) for people.
  - Review access regularly.

=====================================================================
6. PROTECTING PII IN PIPELINES
=====================================================================
Options, from strongest to weakest protection:

  DROP        Do not load the column at all if nobody needs it.
  MASK        Hide part of it:  j***@example.com
  HASH        Replace with a one-way fingerprint. Good for joining
              tables without exposing the value.
  TOKENISE    Swap for a random token, with the real value stored
              in a separate secure vault.
  ENCRYPT     Scramble it; only key holders can read it.

Hashing example in Python. Use a secret key (HMAC), not a plain
hash, because emails are easy to guess and reverse:

    import hashlib
    import hmac
    import os

    SECRET = os.environ["PII_HASH_KEY"]      # never hard-code this

    def hash_email(email):
        normalised = email.strip().lower().encode()
        return hmac.new(SECRET.encode(), normalised, hashlib.sha256).hexdigest()

Masking example:

    def mask_email(email):
        name, domain = email.split("@")
        return name[0] + "***@" + domain

SQL masking view:

    CREATE VIEW marts.customers_safe AS
    SELECT
        customer_id,
        left(email, 1) || '***@' || split_part(email, '@', 2) AS email,
        city
    FROM raw.customers;

Many warehouses (Snowflake, BigQuery, Databricks) also offer built-in
column-level security and dynamic masking policies.

=====================================================================
7. ENCRYPTION
=====================================================================
AT REST      Data stored on disk is encrypted. Turn on the cloud
             provider's encryption for buckets and databases (it is
             often on by default).
IN TRANSIT   Data moving over a network is encrypted with TLS.
             Use https:// and TLS connections to databases and
             Kafka.

Manage keys with a key service (AWS KMS, Azure Key Vault, Google
Cloud KMS), not in code.

=====================================================================
8. SECRETS MANAGEMENT
=====================================================================
Passwords, API keys and tokens must never be in code, git, Docker
images, or logs.

Where to put them instead:
  - Environment variables (simple, for local work).
  - A secrets manager: AWS Secrets Manager, HashiCorp Vault, Azure
    Key Vault.
  - CI/CD secrets (GitHub Actions Secrets).
  - Kubernetes Secrets.
  - Airflow Connections and Variables.

If a secret is committed to git by mistake, treat it as leaked:
rotate it straight away. Deleting the commit is not enough.
Add `.env` and `*.tfvars` to .gitignore, and consider a secret
scanner in CI.

=====================================================================
9. LINEAGE, CATALOGS AND DOCUMENTATION
=====================================================================
Governance needs people to be able to FIND data and UNDERSTAND it.

  - A data catalog lists datasets, owners, descriptions and tags
    (tools: DataHub, OpenMetadata, Atlan, Collibra, or your cloud's
    own catalog).
  - Lineage shows which sources feed a table, and so which reports
    break if a source changes. dbt docs gives you lineage for free.
  - Tag columns that hold PII so access rules can follow the tag.

=====================================================================
10. RETENTION AND DELETION
=====================================================================
  - Set a retention period per dataset (e.g. logs 90 days,
    transactions 7 years).
  - Automate it: bucket lifecycle rules, table partition expiry,
    scheduled delete jobs.
  - Plan for "delete my data" requests. This is hard if the same
    person's data is copied into many tables and backups. Keep
    track of where personal data lives, and use a stable ID so you
    can find it everywhere.

=====================================================================
11. AUDITING AND MONITORING
=====================================================================
  - Turn on audit logs: who queried what, who changed permissions.
  - Alert on odd behaviour: a huge export, access at 3am, a new
    user reading sensitive tables.
  - Keep logs safe and keep them for a defined period.
  - Never write PII or secrets into application logs.

=====================================================================
12. GOOD HABITS CHECKLIST
=====================================================================
  [ ] Know what personal data you hold and where it is.
  [ ] Collect and keep only what you need.
  [ ] Classify datasets by sensitivity.
  [ ] Give every dataset an owner.
  [ ] Least privilege, roles, and service accounts.
  [ ] Encrypt at rest and in transit.
  [ ] Mask or hash PII before it reaches analysts.
  [ ] No secrets in code. Rotate keys.
  [ ] Audit logs on, with alerts.
  [ ] Retention rules automated.
  [ ] Use fake or anonymised data in dev and test, not real
      customer data.

=====================================================================
13. PRACTICE EXERCISE
=====================================================================
  1. Make a CSV of 20 fake customers (name, email, phone, city,
     spend).
  2. Mark each column as public, internal or restricted.
  3. Write a Python function that outputs a "safe" version: drop
     the phone number, hash the email with HMAC, keep city and
     spend.
  4. Read the HMAC key from an environment variable. Check that
     your code fails clearly if it is missing.
  5. In Postgres (use Docker), create an `analyst` role that can
     only read a masked view, and test it by logging in as that
     role.
  6. Add `.env` to .gitignore and add a secret scan to your CI
     workflow (see cicd).
  7. Write a one-page retention policy for the dataset.

Next steps: add column-level tags and masking policies in a real
warehouse, and set up a data catalog such as OpenMetadata.
"""


def main():
    print(LESSON)


if __name__ == "__main__":
    main()
