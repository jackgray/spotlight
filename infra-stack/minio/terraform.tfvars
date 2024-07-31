minio_root_user         = "${env("MINIO_ROOT_USER")}"
minio_root_password     = "${env("MINIO_ROOT_PASSWORD")}"
minio_port              = "${env("MINIO_PORT")}"
minio_console_port      = "${env("MINIO_CONSOLE_PORT")}"
minio_server_url        = "${env("MINIO_SERVER_URL")}"

clickhouse_port         = "${env("CLICKHOUSE_PORT")}"
clickhouse_user         = "${env("CLICKHOUSE_USER")}"
clickhouse_password     = "${env("CLICKHOUSE_PASSWORD")}"
s3_bucket_url           = "${env("S3_BUCKET_URL")}"
