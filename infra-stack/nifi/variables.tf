
variable "nomad_address" {
  description = "Address of the Nomad server"
  type        = string
}

variable "nifi_image" {
  description = "Docker image for NiFi"
  type        = string
  default     = "apache/nifi:latest"
}

variable "nifi_cpu" {
  description = "CPU resources for NiFi task"
  type        = number
  default     = 1000
}

variable "nifi_memory" {
  description = "Memory resources for NiFi task"
  type        = number
  default     = 2048
}

variable "nifi_http_port" {
  description = "HTTP port for NiFi"
  type        = number
  default     = 8080
}

variable "nifi_https_port" {
  description = "Port for NiFi HTTPS access"
  type        = number
  default     = 8443
}

variable "nifi_keystore" {
  description = "Path to NiFi keystore file"
  type        = string
}

variable "nifi_keystore_password" {
  description = "Password for the NiFi keystore"
  type        = string
  sensitive   = true
}

variable "nifi_truststore" {
  description = "Path to NiFi truststore file"
  type        = string
}

variable "nifi_truststore_password" {
  description = "Password for the NiFi truststore"
  type        = string
  sensitive   = true
}

variable "kafka_bootstrap_servers" {
  description = "Kafka bootstrap servers"
  type        = string
}

variable "kafka_topic" {
  description = "Kafka topic"
  type        = string
}

variable "clickhouse_host" {
  description = "ClickHouse host"
  type        = string
}

variable "clickhouse_port" {
  description = "ClickHouse port"
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
