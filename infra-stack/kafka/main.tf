module "zookeeper" {
  source = "./zookeeper"

  nomad_addr            = var.nomad_addr
  datacenters           = var.datacenters
  image                 = var.zookeeper_image
  instance_count        = var.zookeeper_instance_count
  cpu                   = var.zookeeper_cpu
  memory                = var.zookeeper_memory
  service_name          = var.zookeeper_service_name
  tags                  = var.zookeeper_tags
  check_name            = var.zookeeper_check_name
  check_type            = var.zookeeper_check_type
  check_interval        = var.zookeeper_check_interval
  check_timeout         = var.zookeeper_check_timeout
  zookeeper_port        = var.zookeeper_port
}

module "broker" {
  source = "./broker"

  nomad_addr            = var.nomad_addr
  datacenters           = var.datacenters
  image                 = var.kafka_image
  instance_count        = var.kafka_instance_count
  cpu                   = var.kafka_cpu
  memory                = var.kafka_memory
  service_name          = var.kafka_service_name
  tags                  = var.kafka_tags
  check_name            = var.kafka_check_name
  check_type            = var.kafka_check_type
  check_interval        = var.kafka_check_interval
  check_timeout         = var.kafka_check_timeout
  kafka_port            = var.kafka_port
  zookeeper_service_name = var.zookeeper_service_name
  zookeeper_port        = var.zookeeper_port
}
