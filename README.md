# Spotlight 

### Data aggregation and reporting for the public but on a platform that actually wants to be used


This goal of this project is to shine a light on nefarious activities by those we have entrusted with great power. This could be insider trading or voting activity by politicians, stock manipulation by institutions, self-interested lobbying, or super pac donations by corporations and ultra-wealthy.

Many public datasets are managed by entities that may be required to make data publicly available to satisfy transparency requirements, but make it intentionally difficult to consume.

This project also aims to provide a platform for users to host and play with data, and share their datasets and underlying code.


## Architecture
This is achieved by making transmission speads the top priority. Servers will couple database storage with distributed S3 storage on the same machine, and leverage parallel processing and Kafka streaming to handle retreival and transformation requests with optimal efficiency.

Clickhouse is a crazy fast columnar OLAP engine, and integrates with MinIO for remote s3 storage, and since bare metal machines will join aspects of both services onto a single machine, they will be able to handle vast amounts of data exceeding the capabilities of traditional designs.

Kafka producers will run as microservices to make requests to data or send user blob storage uploads of their own data files to be ingested to Clickhouse via NiFi

When a user creates a custom ETL, it will be converted into it's own microservice fitting this design

![Diagram](./architecture.png)


# Front end

I am merging my GovTrackr project with this to serve as the user client. It is built on Next.js, React, material-ui, Node/Express, GrapQL, Prisma CRM, and PostgreSQL. Currently Prisma does not support Clickhouse, but that is likely to change soon as the feature has a lot of community support. Until then, Clickhouse DB will be replicated to a supported DB, such as postgres.


## See producers directory for data retreival pipelines

## See infra-stack directory for more in-depth information about the backend architecture