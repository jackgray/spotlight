variable "nomad_addr" {
  description = "Address of the Nomad server"
  type        = string
}

variable "datacenters" {
  description = "Nomad datacenters"
  type        = list(string)
}

variable "kafka_image" {
  description = "Docker image for Kafka"
  type        = string
}

variable "kafka_instance_count" {
  description = "Number of Kafka instances"
  type        = number
}

variable "kafka_cpu" {
  description = "CPU allocation for Kafka"
  type        = number
}

variable "kafka_memory" {
  description = "Memory allocation for Kafka"
  type        = string
}

variable "kafka_service_name" {
  description = "Service name for Kafka"
  type        = string
}

variable "kafka_tags" {
  description = "Tags for the Kafka service"
  type        = list(string)
}

variable "kafka_check_name" {
  description = "Name of the health check"
  type        = string
}

variable "kafka_check_type" {
  description = "Type of health check"
  type        = string
}

variable "kafka_check_interval" {
  description = "Interval for the health check"
  type        = string
}

variable "kafka_check_timeout" {
  description = "Timeout for the health check"
  type        = string
}

variable "kafka_port" {
  description = "Port for Kafka"
  type        = number
}

variable "zookeeper_image" {
  description = "Docker image for Zookeeper"
  type        = string
}

variable "zookeeper_instance_count" {
  description = "Number of Zookeeper instances"
  type        = number
}

variable "zookeeper_cpu" {
  description = "CPU allocation for Zookeeper"
  type        = number
}

variable "zookeeper_memory" {
  description = "Memory allocation for Zookeeper"
  type        = string
}

variable "zookeeper_service_name" {
  description = "Service name for Zookeeper"
  type        = string
}

variable "zookeeper_tags" {
  description = "Tags for the Zookeeper service"
  type        = list(string)
}

variable "zookeeper_check_name" {
  description = "Name of the health check"
  type        = string
}

variable "zookeeper_check_type" {
  description = "Type of health check"
  type        = string
}

variable "zookeeper_check_interval" {
  description = "Interval for the health check"
  type        = string
}

variable "zookeeper_check_timeout" {
  description = "Timeout for the health check"
  type        = string
}

variable "zookeeper_port" {
  description = "Port for Zookeeper"
  type        = number
}
