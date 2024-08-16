nomad_address = "${env("NOMAD_ADDRESS")}"
image    = "${env("IMAGE")}"
cpu      = "${env("CPU")}"
memory   = "${env("MEMORY")}"
http_port = "${env("HTTP_PORT")}"

https_port           = "${env("HTTPS_PORT")}"
keystore             = "${env("KEYSTORE")}"
keystore_password    = "${env("KEYSTORE_PASSWORD")}"
truststore           = "${env("TRUSTSTORE")}"
truststore_password  = "${env("TRUSTSTORE_PASSWORD")}"

kafka_topic         = "${env("NIFI_KAFKA_TOPIC")}