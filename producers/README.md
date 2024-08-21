# Data Pipelines

Airflow is used to run Kafka producers on schedule which pull external sources with Python code and send the results to Kafka topics 

Kafka Consumers listen on the topics and insert results into Clickhouse database

Clickhouse connects to Apache Superset and updates charts as underlying tables are updated

React/Next.js client application embeds dashboards from the Superset instance, showing a live representation of the data.

Clickhouse stores the data on Minio running on the same host machine for fast transmission