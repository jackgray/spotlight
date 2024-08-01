locals {
  all_vars = {
    nifi_image              = var.nifi_image
    nifi_cpu                = var.nifi_cpu
    nifi_memory             = var.nifi_memory
    nifi_http_port          = var.nifi_http_port
    kafka_bootstrap_servers = var.kafka_bootstrap_servers
    kafka_topic             = var.kafka_topic
    clickhouse_host         = var.clickhouse_host
    clickhouse_port         = var.clickhouse_port
    clickhouse_db           = var.clickhouse_db
    clickhouse_user         = var.clickhouse_user
    clickhouse_password     = var.clickhouse_password
  }
}

data "template_file" "nifi_nomad" {
  template = file("${path.module}/nifi.nomad.tpl")
  vars     = local.all_vars
}

resource "nomad_job" "nifi" {
  jobspec = data.template_file.nifi_nomad.rendered
}
