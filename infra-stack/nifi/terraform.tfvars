nomad_address = "${env("NOMAD_ADDRESS")}"
nifi_image    = "${env("NIFI_IMAGE")}"
nifi_cpu      = "${env("NIFI_CPU")}"
nifi_memory   = "${env("NIFI_MEMORY")}"
nifi_http_port = "${env("NIFI_HTTP_PORT")}"

nifi_https_port           = "${env("NIFI_HTTPS_PORT")}"
nifi_keystore             = "${env("NIFI_KEYSTORE")}"
nifi_keystore_password    = "${env("NIFI_KEYSTORE_PASSWORD")}"
nifi_truststore           = "${env("NIFI_TRUSTSTORE")}"
nifi_truststore_password  = "${env("NIFI_TRUSTSTORE_PASSWORD")}"

kafka_bootstrap_servers = "kafka:9092"
kafka_topic             = "nifi-topic"
clickhouse_host         = "clickhouse"
clickhouse_port         = 9000
clickhouse_db           = "default"
clickhouse_user         = "default"
clickhouse_password     = "password"