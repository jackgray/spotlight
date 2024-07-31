provider "docker" {
  host = "unix:///var/run/docker.sock"
}

resource "docker_network" "superset_network" {
  name = "superset_network"
}

resource "docker_volume" "superset_home" {
  name = "superset_home"
}

resource "docker_volume" "postgres_data" {
  name = "postgres_data"
}

resource "docker_volume" "clickhouse_data" {
  name = "clickhouse_data"
}


resource "docker_container" "minio" {
  image = "minio/minio"
  name  = "minio"
  ports {
    internal = var.minio_port
    external = var.minio_port
  }
  ports {
    internal = var.minio_console_port
    external = var.minio_console_port
  }
  env = [
    "MINIO_ROOT_USER=${var.minio_root_user}",
    "MINIO_ROOT_PASSWORD=${var.minio_root_password}"
  ]
  command = "server /data --console-address :${var.minio_console_port}"
  networks_advanced {
    name = docker_network.superset_network.name
  }
}

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

resource "docker_container" "nifi" {
  image = "apache/nifi:latest"
  name  = "nifi"
  ports {
    internal = var.nifi_port
    external = var.nifi_port
  }
  networks_advanced {
    name = docker_network.superset_network.name
  }
}

resource "docker_container" "postgres" {
  image = "postgres:12"
  name  = "postgres"
  env = [
    "POSTGRES_DB=${var.postgres_db}",
    "POSTGRES_USER=${var.postgres_user}",
    "POSTGRES_PASSWORD=${var.postgres_password}"
  ]
  volumes {
    host_path      = docker_volume.postgres_data.name
    container_path = "/var/lib/postgresql/data"
  }
  networks_advanced {
    name = docker_network.superset_network.name
  }
}

resource "docker_container" "superset" {
  image = "apache/superset:latest"
  name  = "superset"
  env = [
    "SUPERSET_LOAD_EXAMPLES=${var.superset_load_examples}",
    "SUPERSET_SECRET_KEY=${var.superset_secret_key}",
    "SUPERSET_WEBSERVER_PORT=${var.superset_webserver_port}"
  ]
  volumes {
    host_path      = docker_volume.superset_home.name
    container_path = "/app/superset_home"
  }
  ports {
    internal = var.superset_port
    external = var.superset_port
  }
  depends_on = [docker_container.postgres]
  networks_advanced {
    name = docker_network.superset_network.name
  }
}

resource "docker_container" "clickhouse" {
  image = "clickhouse/clickhouse-server:latest"
  name  = "clickhouse"
  ports {
    internal = var.clickhouse_port
    external = var.clickhouse_port
  }
  env = [
    "CLICKHOUSE_DB=${var.clickhouse_db}",
    "CLICKHOUSE_USER=${var.clickhouse_user}",
    "CLICKHOUSE_PASSWORD=${var.clickhouse_password}"
  ]
  volumes {
    host_path      = docker_volume.clickhouse_data.name
    container_path = "/var/lib/clickhouse"
  }
  networks_advanced {
    name = docker_network.superset_network.name
  }
}
