# Hosting infrastrucutre for Spotlight

The spotlight platform is built using Minio/S3, Clickhouse resting on S3, Kafka, NiFi, Spark, Airflow and Superset, which are provisioned and managed by Hashicorp's Nomad and Terraform.

## S3 Data source: 

MinIO hosts S3 buckets on bare metal, with pooling and tiering support with AWS S3 support for overflow cold storage. One bucket will hold raw source data to be processed, while another bucket will hold a Clickhouse database. Tiering is leveraged to create cold back ups as well as extended caching beyond memory allotments

## Data Retrieval

Airflow and Spark will make API calls and either explicitly transform the data, or send responses to Apache NiFi for transformation and loading.

## Data Processor

Apache NiFi will receive the data from Kafka Topics, or directly from batch processors, then parse and load the data into Clickhouse

## Database

Clickhouse holds structured aggregated data and uses S3 buckets as distributed remote storage

## Dashboards

Apache Superset connects with the Clickhouse database with caching and configurable data refresh.


## Proxy tunneling

Cloudflare Argo tunnels allow selective publication of local services to public DNS servers. 

## Container host

These services should run in any container environment by pulling the image and setting the required env variables in a docker compose or swarm template.

The deployment method used here is Terraform plans which build nomad job files on the fly from environment variables and Nomad job template files. This allows system agnostic deployment anywhere nomad is available with a single source of truth for the specification variables. tfvars uses env variables as inputs and main.tf holds nomad job template code with placeholder variables defined by the tfvars file. This mitigates problems caused by schema drift.
