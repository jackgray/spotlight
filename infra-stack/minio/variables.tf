variable "minio_root_user" {
  description = "MinIO root user"
}

variable "minio_root_password" {
  description = "MinIO root password"
}

variable "minio_port" {
  description = "Port for MinIO"
}

variable "minio_console_port" {
  description = "Console port for MinIO"
}

variable "minio_server_url" {
  description = "MinIO server URL"
}

variable "clickhouse_port" {
  description = "Port for ClickHouse"
}

variable "clickhouse_user" {
  description = "ClickHouse user"
}

variable "clickhouse_password" {
  description = "ClickHouse password"
}

variable "s3_bucket_url" {
  description = "S3 Bucket URL for MinIO"
}
