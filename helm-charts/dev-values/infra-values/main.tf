# module "gke" {
#   source       = "./modules/gke"
#   project_id   = var.project_id
#   region       = var.region
#   cluster_name = var.cluster_name
# }

module "cloudsql" {
  source       = "./modules/cloudsql"
  project_id   = var.project_id
  region       = var.region
  db_instance_name = var.db_instance_name
}

module "jenkins_vm" {
  source     = "./modules/jenkins-vm"
  project_id = var.project_id
  zone       = var.zone
  vm_name    = var.vm_name
}

module "pubsub" {
  source     = "./modules/pubsub"
  pull_subscriptions = var.pull_subscriptions
  push_subscriptions = var.push_subscriptions
  topic_names = var.topic_names
  project_id = var.project_id
}
