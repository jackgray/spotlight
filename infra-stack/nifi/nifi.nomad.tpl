job "nifi" {
  datacenters = ["dc1"]

  group "nifi" {
    count = 1

    task "nifi" {
      driver = "docker"

      config {
        image = "${nifi_image}"
        port_map {
          http = ${nifi_http_port}
        }
      }

      resources {
        cpu    = ${nifi_cpu}
        memory = ${nifi_memory}
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
        NIFI_WEB_HTTP_PORT       = "${nifi_http_port}"
        KAFKA_BOOTSTRAP_SERVERS  = "${kafka_bootstrap_servers}"
        KAFKA_TOPIC              = "${kafka_topic}"
        CLICKHOUSE_HOST          = "${clickhouse_host}"
        CLICKHOUSE_PORT          = "${clickhouse_port}"
        CLICKHOUSE_DB            = "${clickhouse_db}"
        CLICKHOUSE_USER          = "${clickhouse_user}"
        CLICKHOUSE_PASSWORD      = "${clickhouse_password}"
      }
    }
  }
}
