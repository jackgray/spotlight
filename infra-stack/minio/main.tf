resource "docker_volume" "minio_data" {
  name = "minio_data"
}

resource "docker_volume" "minio_config" {
  name = "minio_config"
}

resource "docker_container" "minio" {
  image = "minio/minio"
  name  = "minio"
  ports {
    internal = var.minio_port
    external = var.minio_port
  }
  ports {
    internal = var.minio_console_port
    external = var.minio_console_port
  }
  env = [
    "MINIO_ROOT_USER=${var.minio_root_user}",
    "MINIO_ROOT_PASSWORD=${var.minio_root_password}"
  ]
  volumes {
    host_path      = docker_volume.minio_data.name
    container_path = "/data"
  }
  volumes {
    host_path      = docker_volume.minio_config.name
    container_path = "/root/.minio"
  }
  command = "server /data --console-address :${var.minio_console_port}"
  networks_advanced {
    name = docker_network.superset_network.name
  }
}
