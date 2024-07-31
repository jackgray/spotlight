resource "docker_container" "nifi" {
  image = "apache/nifi:latest"
  name  = "nifi"
  ports {
    internal = var.nifi_port
    external = var.nifi_port
  }
  volumes {
    host_path      = "./nifi/conf"
    container_path = "/opt/nifi/nifi-current/conf"
  }
  volumes {
    host_path      = "./nifi/logs"
    container_path = "/opt/nifi/nifi-current/logs"
  }
  volumes {
    host_path      = "./nifi/data"
    container_path = "/opt/nifi/nifi-current/data"
  }
  volumes {
    host_path      = "./setup-nifi.sh"
    container_path = "/opt/nifi/setup-nifi.sh"
  }
  entrypoint = ["/opt/nifi/setup-nifi.sh"]
  env = [
    "NIFI_HTTP_PORT=${var.nifi_http_port}",
    "NIFI_HTTPS_PORT=${var.nifi_https_port}",
    "NIFI_KEYSTORE=${var.nifi_keystore}",
    "NIFI_KEYSTORE_PASSWORD=${var.nifi_keystore_password}",
    "NIFI_TRUSTSTORE=${var.nifi_truststore}",
    "NIFI_TRUSTSTORE_PASSWORD=${var.nifi_truststore_password}"
  ]
  networks_advanced {
    name = docker_network.superset_network.name
  }
}
