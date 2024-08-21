# Spotlight 

### Data aggregation and reporting for the public but on a platform that actually wants to be used


This goal of this project is to increase transparency over individuals in positions of notable power and influence. Financial and political conflicts of interests, illegal trading, abusive expendature of tax dollars, and regulative circumvention.

It aims largely to keep the focus of activist/investigative journalism on hard data, and encourage the community to engage in political and economic reform efforts.

It's also a way for me to hone some skills I am interested in, which is why you might see some 'over-engineered' components here. 

## Architecture
In an effort to optimize resource utilization through speed and efficiency of underlying platform infrastructure, servers couple database storage with distributed S3 storage on the same machine, and leverage parallel processing and Kafka streaming to handle retreival and transformation requests with optimal efficiency.

Clickhouse is a crazy fast columnar OLAP engine, and integrates with MinIO for remote s3 storage. Hosting both services together on the same cluster allows optimal handling of vast amounts of data at speeds exceeding the capabilities of traditional designs.

Kafka producers orchestrated by Airflow make requests to external data, and  either explicitly transform and publish to appropriate topics for table ingestion, or forward the responses to NiFI for automatic ingestion.


![Diagram](./architecture.png)


# Client Appliction

It is built on Next.js, React, next-ui, Node/Express, GrapQL, Prisma CRM, and PostgreSQL. 

## See producers directory for data retreival pipelines

## See infra-stack directory for more in-depth information about the backend architecture