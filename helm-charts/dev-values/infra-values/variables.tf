variable "project_id" {}
variable "region" { default = "us-central1" }
variable "zone" { default = "us-central1-a" }
variable "cluster_name" { default = "gke-cluster" }
variable "db_instance_name" { default = "postgres-db" }
variable "vm_name" { default = "jenkins-vm" }

variable "buckets" {
  type = map(object({
    storage_class               = string
    force_destroy               = bool
    uniform_bucket_level_access = bool
    enable_versioning           = bool
    retention_policy            = number
    labels                      = map(string)
    lifecycle_rules = list(object({
      action_type = string
      condition   = map(number)
    }))
    cors = list(object({
      origin          = list(string)
      method          = list(string)
      response_header = list(string)
      max_age_seconds = number
    }))
  }))
}

variable "topic_names" {
  type = list(string)
}

variable "push_subscriptions" {
  type = list(string)
}

variable "pull_subscriptions" {
  type = map(object({
    name                        = string
    topic                       = string
    ack_deadline_seconds       = number
    message_retention_duration = string
  }))
}
