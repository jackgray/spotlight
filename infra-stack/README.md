# Hosting infrastrucutre for Spotlight

The Spotlight platform is built using Clickhouse resting on MinIO/S3, Kafka, NiFi, Spark, Airflow and Superset, which are provisioned and managed by Hashicorp's Nomad and Terraform.

## S3 Data source: 

MinIO hosts S3 buckets on bare metal, with pooling and tiering support with AWS S3 support for overflow cold storage. One bucket will hold raw source data to be processed, while another bucket will hold a Clickhouse database. Tiering is leveraged to create cold back ups as well as extended caching beyond memory allotments

## Data Retrieval

Airflow and Spark will make API calls and either explicitly transform the data, or send responses to Apache NiFi for transformation and loading.

For endpoints that support notifications, Kafka producers will listen and push updates to topics which will be consumed either by custom Spark transformers or Apache NiFi. 


## Data Processor

Apache NiFi will receive the data from Kafka Topics, or directly from batch processors, then parse and load the data into Clickhouse

NiFi can also be used as a failover for dead letter queues or custom batch jobs where if a transformer fails to process and/or load some data, NiFi will attempt to parse and store it in either the intended db or a failure reporting db.

When making batch requests, the data will be processed mid-stream during the retreival process using asynchronous and parallel requests. 

## Database

Clickhouse holds structured aggregated data and uses S3 buckets as distributed remote storage

## Dashboards

Apache Superset connects with the Clickhouse database with caching and configurable data refresh.


## Proxy tunneling

Cloudflare Argo tunnels allow selective publication of local services to public DNS servers. 

## Container host

These services should run in any container environment by pulling the image and setting the required env variables in a docker compose or swarm template.

#### Deployment method 
Terraform plans build nomad job files on the fly by injecting environment variables into Nomad job template files and feeding those directly into the Terraform plan, giving .env the single source of truth for config variables in the entire deployment cycle. 

It also makes the infrastructure have an extremely small footprint, particularly in hosting requirements: 
(1) At least one Nomad worker and manager with 
(2) a container runtime setup and
(3) Terraform installed. 
(4) Configuring the example.env file
(5) An S3 endpoint -- Minio is the default here because it allows Clickhouse to run on the same physical cluster that the data is stored on), and reduces sharding complexity by handling object distribution, versioning, access, and tiering.

The rest should be pulled and handled between Terraform and Nomad (Note if using a different container repo hub than Docker, you may have to modify the Terraform plan.)

tfvars uses env variables as inputs and main.tf holds Nomad job template code with placeholder variables defined by the tfvars file. This mitigates problems caused by schema modification and allows highly scalable development by abstracting configuration code into  templates and .env vars reducing complexity and required coding.
