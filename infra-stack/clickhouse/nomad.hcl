job "${var.service_name}" {
  datacenters = ["${var.datacenters}"]

  group "${var.service_name}" {
    count = 1

    task "${var.service_name}" {
      driver = "docker"

      config {
        image = "${var.clickhouse_image}"
        port_map {
          http = ${var.clickhouse_http_port}
          tcp  = ${var.clickhouse_tcp_port}
        }
      }

      resources {
        cpu    = ${var.cpu}
        memory = ${var.memory}
      }

      service {
        name = "${var.service_name}"
        tags = ${jsonencode(split(",", var.tags))}
        port = "http"

        check {
          name     = "${var.check_name}"
          type     = "${var.check_type}"
          interval = "${var.check_interval}"
          timeout  = "${var.check_timeout}"
        }
      }
    }
  }
}
