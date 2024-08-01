resource "nomad_job" "zookeeper" {
  jobspec = templatefile("${path.module}/nomad.tpl", {
    service_name = var.service_name
    datacenters  = var.datacenters
    image        = var.image
    instance_count = var.instance_count
    cpu          = var.cpu
    memory       = var.memory
    tags         = jsonencode(var.tags)
    check_name   = var.check_name
    check_type   = var.check_type
    check_interval = var.check_interval
    check_timeout = var.check_timeout
    zookeeper_port = var.zookeeper_port
  })
}
