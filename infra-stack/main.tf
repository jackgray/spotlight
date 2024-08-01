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
}
