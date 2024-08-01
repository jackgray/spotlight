
datacenters         = "${env("DATACENTERS)}"
image               = "${env("IMAGE")}"
host                = "clickhouse"
cpu                 = "${env("CPU")}"
port                = "${env("CLICKHOUSE_PORT")}"
memory              = 2048
service_name        = "clickhouse"
tags                = "clickhouse,production,db"
check_name          = "alive"
check_type          = "tcp"
check_interval      = "10s"
check_timeout       = "2s"


db           = "default"
user         = "default"
password     = "password"


http_port    = "${env("HTTP_PORT")}"
tcp_port     = "${env("TCP_PORT")}"
user         = "${env("USER")}"
password     = "${env("PASSWORD")}"

minio_bucket = "${env("MINIO_BUCKET")}"
