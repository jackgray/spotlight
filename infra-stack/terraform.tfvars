minio_root_user         = "${env("MINIO_ROOT_USER")}"
minio_root_password     = "${env("MINIO_ROOT_PASSWORD")}"
minio_port              = "${env("MINIO_PORT")}"
minio_console_port      = "${env("MINIO_CONSOLE_PORT")}"

kafka_broker_id         = "${env("KAFKA_BROKER_ID")}"
kafka_listeners         = "${env("KAFKA_LISTENERS")}"
kafka_port              = "${env("KAFKA_PORT")}"
kafka_zookeeper_connect = "${env("KAFKA_ZOOKEEPER_CONNECT")}"
allow_plaintext_listener = "${env("ALLOW_PLAINTEXT_LISTENER")}"
zookeeper_port          = "${env("ZOOKEEPER_PORT")}"

allow_anonymous_login   = "${env("ALLOW_ANONYMOUS_LOGIN")}"

nifi_port               = "${env("NIFI_PORT")}"

superset_load_examples  = "${env("SUPERSET_LOAD_EXAMPLES")}"
superset_secret_key     = "${env("SUPERSET_SECRET_KEY")}"
superset_webserver_port = "${env("SUPERSET_WEBSERVER_PORT")}"
superset_port           = "${env("SUPERSET_PORT")}"


postgres_db             = "${env("POSTGRES_DB")}"
postgres_user           = "${env("POSTGRES_USER")}"
postgres_password       = "${env("POSTGRES_PASSWORD")}"
postgres_port           = "${env("POSTGRES_PORT")}"
