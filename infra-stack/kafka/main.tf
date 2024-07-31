resource "docker_container" "zookeeper" {
  image = "bitnami/zookeeper:latest"
  name  = "zookeeper"
  ports {
    internal = var.zookeeper_port
    external = var.zookeeper_port
  }
  env = [
    "ALLOW_ANONYMOUS_LOGIN=${var.allow_anonymous_login}"
  ]
  networks_advanced {
    name = docker_network.superset_network.name
  }
}

resource "docker_container" "kafka" {
  image = "bitnami/kafka:latest"
  name  = "kafka"
  ports {
    internal = var.kafka_port
    external = var.kafka_port
  }
  env = [
    "KAFKA_BROKER_ID=${var.kafka_broker_id}",
    "KAFKA_LISTENERS=${var.kafka_listeners}",
    "KAFKA_ZOOKEEPER_CONNECT=${var.kafka_zookeeper_connect}",
    "ALLOW_PLAINTEXT_LISTENER=${var.allow_plaintext_listener}"
  ]
  depends_on = [docker_container.zookeeper]
  networks_advanced {
    name = docker_network.superset_network.name
  }
}