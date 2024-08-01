terraform {
  required_providers {
    nomad = {
      source  = "hashicorp/nomad"
      version = "~> 1.3"
    }
  }
}

provider "nomad" {
  address = var.nomad_address
}

module "nifi" {
  source = "./nifi"
}

module "superset" {
  source = "./superset"
  # provide vars from other modules if needed
  nifi_examplevar = module.nifi.examplevar # now this can be used in the module as var.examplevar
}

module "clickhouse" {
  source = "./clickhouse"
}

module "kafka" {
  source = "./kafka"
}

module "minio" {
  source = ".minio"
}