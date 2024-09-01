# Hosting infrastrucutre for Spotlight

The Spotlight platform is built using Clickhouse resting on MinIO/S3, Kafka, NiFi, Spark, Airflow and Superset, which are provisioned and managed by Hashicorp's Nomad and Terraform.


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

##### Docker compose development

Use the provided docker-compose templates to run these services for development and testing

## S3 Data source: 

MinIO hosts S3 buckets on bare metal, with pooling and tiering support with AWS S3 support for overflow cold storage. One bucket will hold raw source data to be processed, while another bucket will hold a Clickhouse database. Tiering is leveraged to create cold back ups as well as extended caching beyond memory allotments.

Clickhouse instances can run in distributed mode and be completely agnostic to where the data is mounted, decoupling db endpoints from storage. Some db servers could be on the same machine as S3 and this would be quite fast, but it's also not a requirement, and allows better configurability over data replication and availability efforts, including expansion to other S3 sources or autoscaling via Equinox bare metal instances.

## Data Retrieval

Airflow and Spark will make API calls and either explicitly transform the data, or send responses to Apache NiFi for transformation and loading.

For endpoints that support notifications, Kafka producers will listen and push updates to topics which will be consumed either by custom Spark transformers or Apache NiFi. 



### Scheduling / Data retrieval

Batch-heavy pipelines are scheduled and run by Airflow

'Always running' streaming data pipelines run in containers managed and load balanced by Hashicorp's Nomad, a lighter, faster alternative to Kubernetes


## Processing
Apache NiFi will listen on Kafka topics the raw data is sent to and attempt to infer the proper type casts and insert the data into Clickhouse DB.





## Data Processor

Apache NiFi will listen on Kafka Topics, or receive data directly from batch processors when appropriate, then parse and load the data into Clickhouse using the Clickhouse sink connector

Data which needs more explicit transformation will be handled by custom python consumer/producers

NiFi can also be used as a failover for dead letter queues or custom batch jobs where if a transformer fails to process and/or load some data, NiFi will leniently parse and store the data into a failure reporting db.

When making batch requests, the data is processed mid-stream during the retreival process using asynchronous and parallel requests, by route of either asyncio and parallelism in the python code, or via Kafka

## Database

Combinations of Clickhouse and Postgresql are used leveraged to acheive both fast queries and robust data management.

Tables are synced across databases using change data capture via Debezium and Clickhouse and JDBC sink connectors. 

ParadeDB will be experimented with as an alternative to clickhouse to potentially afford a uniform postgres language with speeds comparable to Clickhouse.


### Syncing Clickhouse with Postgres

https://clickhouse.com/blog/clickhouse-postgresql-change-data-capture-cdc-part-1
https://clickhouse.com/blog/clickhouse-postgresql-change-data-capture-cdc-part-2

### Postgres with S3 backed OLAP and Elasticsearch capability
ParadeDB offers extensions to Postgresql which offer advantages of DuckDB and Elasticsearch free-tex indexing, which can make Postgres faster than Elasticsearch and almost as fast as DuckDB. Clickhouse is more mature but thsi project shows a lot of promise.


## Dashboards

Apache Superset connects with the Clickhouse database with caching and configurable data refresh.

