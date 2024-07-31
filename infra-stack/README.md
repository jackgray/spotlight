# Hosting infrastrucutre for Spotlight

This platform is built on top of Minio, Clickhouse, Kafka, NiFi, and Superset, which will cover data storage, streaming, processing, lightning fast queries, and dashboarding.

Later, multi-tenancy will be incorporated to alot secure work spaces to end users

## S3 Data source: 

MinIO hosts S3 buckets on bare metal, with pooling and tiering support with AWS S3 support for overflow cold storage. One bucket will hold raw source data to be processed, while another bucket will hold a Clickhouse database. Tiering is leveraged to create cold back ups as well as extended caching beyond memory allotments

## Data Retrieval

Kafka producers will make API calls to externally hosted data and send them to Apache NiFi for transformation

## Data Processor

Apache NiFi will receive the data from Kafka Topics, which recieve streaming data from the Kafka Producers, then parse and load the data into Clickhouse

## Database

Clickhouse holds structured aggregated data and uses S3 bucket as remote storage

## Dashboards

Apache Superset connects with the Clickhouse database to 


## Proxy tunneling

Cloudflare Argo tunnels allow selective publication of local services to public DNS servers

## Container host

These services should run in any container environment by pulling the image and setting the required env variables in a docker compose or swarm template.

The deployment method used here is Terraform plans which build nomad job files on the fly from environment variables and Nomad job template files. This allows system agnostic deployment anywhere nomad is available with a single source of truth for the specification variables. tfvars uses env variables as inputs and main.tf holds nomad job template code with placeholder variables defined by the tfvars file