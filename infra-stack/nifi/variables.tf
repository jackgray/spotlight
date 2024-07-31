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
