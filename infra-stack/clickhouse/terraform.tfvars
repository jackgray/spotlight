
datacenters         = "${env("DATACENTERS)}"
clickhouse_image    = "${env("IMAGE")}"
cpu                 = "${env("CPU")}"
memory              = 2048
service_name        = "clickhouse"
tags                = "clickhouse,production,db"
check_name          = "alive"
check_type          = "tcp"
check_interval      = "10s"
check_timeout       = "2s"


http_port    = "${env("HTTP_PORT")}"
tcp_port     = "${env("TCP_PORT")}"
user         = "${env("USER")}"
password     = "${env("PASSWORD")}"
minio_bucket = "${env("MINIO_BUCKET")}"
minio_endpoint = "${env("MINIO_ENDPOINT")}"
