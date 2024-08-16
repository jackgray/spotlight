

variable "zookeeper_port" {
  description = "Port for Zookeeper service"
  type        = number
}

variable "allow_anonymous_login" {
  description = "Allow anonymous login to Zookeeper"
  type        = string
}

variable "kafka_port" {
  description = "Port for Kafka service"
  type        = number
}

variable "kafka_broker_id" {
  description = "Broker ID for Kafka"
  type        = number
}

variable "kafka_listeners" {
  description = "Listeners for Kafka service"
  type        = string
}

variable "kafka_zookeeper_connect" {
  description = "Zookeeper connect string for Kafka"
  type        = string
}

variable "allow_plaintext_listener" {
  description = "Allow plaintext listener for Kafka"
  type        = string
}

variable "nifi_port" {
  description = "Port for NiFi service"
  type        = number
}

variable "postgres_db" {
  description = "Postgres database name"
  type        = string
}

variable "postgres_user" {
  description = "Postgres user"
  type        = string
}

variable "postgres_password" {
  description = "Postgres password"
  type        = string
}

variable "superset_load_examples" {
  description = "Load example data in Superset"
  type        = string
}

variable "superset_secret_key" {
  description = "Secret key for Superset"
  type        = string
}

variable "superset_webserver_port" {
  description = "Webserver port for Superset"
  type        = number
}

variable "superset_port" {
  description = "Port for Superset service"
  type        = number
}

variable "clickhouse_port" {
  description = "Port for ClickHouse service"
  type        = number
}

variable "clickhouse_db" {
  description = "ClickHouse database name"
  type        = string
}

variable "clickhouse_user" {
  description = "ClickHouse user"
  type        = string
}

variable "clickhouse_password" {
  description = "ClickHouse password"
  type        = string
}

variable "clickhouse_s3_endpoint" {
  description = "S3 endpoint for ClickHouse"
  type        = string
}

variable "clickhouse_s3_access_key_id" {
  description = "S3 access key ID for ClickHouse"
  type        = string
}

variable "clickhouse_s3_secret_access_key" {
  description = "S3 secret access key for ClickHouse"
  type        = string
}

variable "clickhouse_s3_bucket" {
  description = "S3 bucket for ClickHouse"
  type        = string
}

variable "clickhouse_s3_region" {
  description = "S3 region for ClickHouse"
  type        = string
}
