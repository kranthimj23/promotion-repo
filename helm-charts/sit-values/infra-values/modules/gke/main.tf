resource "google_container_cluster" "main" {
  name     = var.cluster_name
  location = var.region
  deletion_protection = false

  remove_default_node_pool = true
  initial_node_count       = 1
}