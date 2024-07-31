variable "nomad_addr" {
    description = "Endpoint for Nomad cluster"
}

variable "datacenters" {
  description = "The datacenters for the job."
}

variable "image" {
  description = "Docker image for ClickHouse."
}

variable "http_port" {
  description = "HTTP port for ClickHouse."
}

variable "tcp_port" {
  description = "TCP port for ClickHouse."
}

variable "cpu" {
  description = "CPU resources for ClickHouse task."
}

variable "memory" {
  description = "Memory resources for ClickHouse task."
}

variable "service_name" {
  description = "Service name for ClickHouse."
}

variable "tags" {
  description = "Tags for the ClickHouse service."
}

variable "check_name" {
  description = "Name for the health check."
}

variable "check_type" {
  description = "Type for the health check."
}

variable "check_interval" {
  description = "Interval for the health check."
}

variable "check_timeout" {
  description = "Timeout for the health check."
}
