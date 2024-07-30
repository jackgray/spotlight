Requirements: 

S3 Data source: 
- MinIO will host S3 buckets. One bucket will hold raw source data to be processed, while another bucket will hold a Clickhouse database

Data Reader: 
- Kafka producers will make API calls to externally hosted data and send them to Apache NiFi for transformation

Data Processor:
- Apache NiFi will receive the data from Kafka Topics, which recieve streaming data from the Kafka Producers, then parse and load the data into Clickhouse

Database:
- Clickhouse will hold structured aggregated data and use S3 bucket as remote storage

Dashboard:
- Apache Superset will connect with the Clickhouse database


Proxy tunneling: this will allow selective publication of local services to public DNS servers

Container host: 

This project is designed with containerization in mind, but clustering and service configuration to an extent is beyond the scope of this project at this time. Simple docker-compose files are provided for development and small-scale production purposes.

In the future, Hashicorp based provisioning will be defined with Terraform and Nomad for distributed deployments