# Orders Pipeline — Two Tracks Spec

Same `raw_orders.csv` dataset, split into **two independent tracks** so
neither one blocks or risks the other:

- **Track A — Databricks/Delta**: Python → PySpark → Databricks Free
  Edition → Jobs → Delta Tables. Uses Databricks' own built-in storage.
  **Zero AWS involvement, zero billing risk.**
- **Track B — AWS/Terraform**: a small, standalone S3 + IAM + Terraform
  project, done independently, whenever you're ready. Not required for
  Track A to work.

Revised 2026-08-22 after concluding Databricks Free Edition and AWS don't
actually need to connect: Free Edition provides its own default storage
(confirmed via Databricks docs), so the earlier plan's Phase 3→4 link
(your S3 bucket feeding a Databricks workspace) only works on a **paid**
AWS-hosted Databricks workspace — not worth the cost/risk right now given
the recent AWS suspension. Decoupling removes that requirement entirely.

## Before either track: finish the PySpark gap

- [ ] **Joins + window functions** (pandas and PySpark): add a second
      lookup table, do a join and a window function (rank / running
      total). Real DE skill, untouched so far, zero new environment
      risk — pure skill-building before adding any new infrastructure.
      **Do this first.**
- [ ] Rename `07_pyspark_etl`'s aggregate output column from
      `total_aggregated` to `total` (small leftover nit).

## Track A — Databricks / Delta (no AWS)

1. **Databricks Free Edition workspace** — sign up (free, no AWS
   account needed). Upload `raw_orders.csv` directly into the workspace.
2. **Notebook**: import the `07_pyspark_etl` logic as a Databricks
   notebook, running against the uploaded file.
3. **Jobs**: schedule the notebook as a Databricks Job (Free Edition
   supports Jobs now, up to 5 concurrent tasks — this is new since the
   old Community Edition).
4. **Delta Tables**: rewrite bronze/silver/gold output as real Delta
   tables (not CSV) using Free Edition's own default storage — ACID
   writes, time travel, schema enforcement. Demonstrate time travel by
   querying an older table version after an update.
5. **Read your own repo**: as part of this phase, read
   `data_engineering/medallion_architecture/bronze_layer.py`,
   `silver_layer.py`, `gold_layer.py` — that's literally the
   bronze/silver/gold pattern you're implementing. Summarize each in
   your own words; find and apply one real improvement.
6. **Optional — OOP-lite refactor**: restructure the pipeline into a
   small class (`Pipeline` with `.validate()/.transform()/.load()`)
   once the Delta version is working.

**Definition of done for Track A:** a scheduled Databricks Job reads raw
data, produces bronze/silver/gold Delta tables in the workspace's own
storage, and you can demonstrate a time-travel query — all without an
AWS account.

## Track B — AWS / Terraform (standalone, separate timing)

Do this whenever you want to build cloud-infra skills specifically —
not gated on Track A, not required for it.

1. **AWS Budget alert** first (e.g. $1 threshold) — non-negotiable
   given the account was suspended for non-payment once already.
2. **Terraform, scoped to exactly two resource types**: one S3 bucket,
   one IAM role/policy (least-privilege, scoped to that bucket only).
   Nothing else — no EC2, no RDS, no NAT Gateway, no compute of any
   kind. Every `.tf` file gets reviewed by you before `terraform apply`.
3. **PySpark reads/writes that S3 bucket** via the `s3a://` connector
   (needs `hadoop-aws` + `aws-java-sdk-bundle` jars — a real new setup
   step, not just config).

**Definition of done for Track B:** `07_pyspark_etl`'s logic reads/writes
S3 instead of local disk, provisioned entirely by Terraform you reviewed.

## If you later want Track A and Track B connected

That requires a **paid** AWS-hosted Databricks workspace (Free Edition's
storage restriction is the blocker, not a Track B limitation). Revisit
this only after both tracks work independently, once you've got a real
sense of what a paid workspace costs for light personal use.
