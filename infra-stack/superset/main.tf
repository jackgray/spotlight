resource "docker_container" "superset" {
  image = "apache/superset:latest"
  name  = "superset"
  env = [
    "SUPERSET_LOAD_EXAMPLES=${var.superset_load_examples}",
    "SUPERSET_SECRET_KEY=${var.superset_secret_key}",
    "SUPERSET_WEBSERVER_PORT=${var.superset_webserver_port}"
  ]
  volumes {
    host_path      = docker_volume.superset_home.name
    container_path = "/app/superset_home"
  }
  ports {
    internal = var.superset_port
    external = var.superset_port
  }
  depends_on = [docker_container.postgres]
  networks_advanced {
    name = docker_network.superset_network.name
  }
}