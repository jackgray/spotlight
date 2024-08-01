job "nifi" {
  datacenters = ["dc1"]

  group "nifi" {
    count = 1

    task "nifi" {
      driver = "docker"

      config {
        image = "${image}"
        port_map {
          http = ${http_port}
        }
      }

      resources {
        cpu    = ${cpu}
        memory = ${memory}
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
        WEB_HTTP_PORT       = "${http_port}"
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
