job "superset" {
  datacenters = ["dc1"]

  group "superset" {
    count = 1

    task "superset" {
      driver = "docker"

      config {
        image = "${superset_image}"
        port_map {
          http = ${superset_http_port}
        }
      }

      resources {
        cpu    = ${superset_cpu}
        memory = ${superset_memory}
      }

      service {
        name = "superset"
        tags = ["superset"]
        port = "http"

        check {
          name     = "alive"
          type     = "tcp"
          interval = "10s"
          timeout  = "2s"
        }
      }

      env {
        SUPERSET_WEBSERVER_PORT = "${superset_http_port}"
        CLICKHOUSE_HOST         = "${clickhouse_host}"
        CLICKHOUSE_PORT         = "${clickhouse_port}"
        CLICKHOUSE_DB           = "${clickhouse_db}"
        CLICKHOUSE_USER         = "${clickhouse_user}"
        CLICKHOUSE_PASSWORD     = "${clickhouse_password}"
      }
    }
  }
}
