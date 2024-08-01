job "${service_name}" {
  datacenters = ["${datacenters}"]

  group "${service_name}" {
    count = ${instance_count}

    task "${service_name}" {
      driver = "docker"

      config {
        image = "${image}"
        port_map {
          kafka = ${kafka_port}
        }
        args = [
          "sh", "-c",
          "sleep 10 && \
          kafka-server-start.sh /etc/kafka/server.properties --override zookeeper.connect=${zookeeper_service_name}.${datacenters[0]}:${zookeeper_port}"
        ]
      }

      resources {
        cpu    = ${cpu}
        memory = ${memory}
      }

      service {
        name = "${service_name}-${index + 1}"
        tags = ${tags}
        port = "kafka"

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
