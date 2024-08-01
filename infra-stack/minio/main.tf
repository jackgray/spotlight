provider "nomad" {
  address = "${var.nomad_addr}"
}

locals {
  nomad_job_template = file("${path.module}/nomad.tpl")
}

resource "nomad_job" "minio" {
  jobspec = templatefile(local.nomad_job_template, {
    datacenters      = var.datacenters
    image            = var.image
    http_port        = var.http_port
    console_port     = var.console_port
    cpu              = var.cpu
    memory           = var.memory
    service_name     = var.service_name
    tags             = var.tags
    check_name       = var.check_name
    check_type       = var.check_type
    check_interval   = var.check_interval
    check_timeout    = var.check_timeout
    instance_count   = var.instance_count
  })
}
