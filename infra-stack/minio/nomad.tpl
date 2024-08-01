job "minio-cluster" {
  datacenters = ["${var.datacenters}"]

  group "minio" {
    count = ${var.instance_count}

    task "minio" {
      driver = "docker"

      config {
        image = "${var.image}"
        command = "server"
        args = [
          "--console-address", ":${var.port}",
          "http://minio{1...${var.instance_count}}/data{1...2}"
        ]
        port_map {
          http = ${var.http_port}
          console = ${var.console_port}
        }
        volumes = [
          for i in range(var.instance_count) : [
            "/mnt/data${i + 1}-1:/data1",
            "/mnt/data${i + 1}-2:/data2"
          ]
        ]
      }

      resources {
        cpu    = ${var.cpu}
        memory = ${var.memory}
      }

      service {
        name = "minio-${index + 1}"
        tags = ["minio"]
        port = "http"

        check {
          name     = "minio-${index + 1}-health"
          type     = "http"
          path     = "/minio/health/live"
          interval = "10s"
          timeout  = "2s"
        }
      }
    }
  }
}
