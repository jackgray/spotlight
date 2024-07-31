job "clickhouse" {
  datacenters = ["dc1"]

  group "clickhouse" {
    count = 1

    task "clickhouse" {
      driver = "docker"

      config {
        image = "yandex/clickhouse-server:latest"
        port_map {
          http = 8123
          tcp  = 9000
        }
      }

      resources {
        cpu    = 1000
        memory = 2048
      }

      service {
        name = "clickhouse"
        tags = ["clickhouse"]
        port = "http"

        check {
          name     = "alive"
          type     = "tcp"
          interval = "10s"
          timeout  = "2s"
        }
      }
    }
  }
}
