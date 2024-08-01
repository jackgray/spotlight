job "${service_name}" {
  datacenters = ["${datacenters}"]

  group "${service_name}" {
    count = ${instance_count}

    task "${service_name}" {
      driver = "docker"

      config {
        image = "${image}"
        port_map {
          zk = ${zookeeper_port}
        }
        args = [
          "sh", "-c",
          "sleep 10 && \
          zookeeper-server-start.sh /etc/zookeeper/zookeeper.properties"
        ]
      }

      resources {
        cpu    = ${cpu}
        memory = ${memory}
      }

      service {
        name = "${service_name}-${index + 1}"
        tags = ${tags}
        port = "zk"

        check {
          name     = "${check_name}-${index + 1}"
          type     = "${check_type}"
          interval = "${check_interval}"
          timeout  = "${check_timeout}"
        }
      }
    }
  }
}
