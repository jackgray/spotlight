job "nifi" {
  datacenters = ["dc1"]

  group "nifi" {
    count = 1

    task "nifi" {
      driver = "docker"

      config {
        image = var.nifi_image
        port_map {
          http = var.nifi_http_port
        }
      }

      resources {
        cpu    = var.nifi_cpu
        memory = var.nifi_memory
      }

      service {
        name = "nifi"
        tags = ["nifi"]
        port = "http"

        check {
          name     = "alive"
          type     = "tcp"
          interval = "10s"
          timeout  = "2s"
        }
      }

      env {
        NIFI_WEB_HTTP_PORT       = var.nifi_http_port
        KAFKA_BOOTSTRAP_SERVERS  = var.kafka_bootstrap_servers
        KAFKA_TOPIC              = var.kafka_topic
        CLICKHOUSE_HOST          = var.clickhouse_host
        CLICKHOUSE_PORT          = var.clickhouse_port
        CLICKHOUSE_DB            = var.clickhouse_db
        CLICKHOUSE_USER          = var.clickhouse_user
        CLICKHOUSE_PASSWORD      = var.clickhouse_password
        # Add other environment variables if needed
      }
    }
  }
}
