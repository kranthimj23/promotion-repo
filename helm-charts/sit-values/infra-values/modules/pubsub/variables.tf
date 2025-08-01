variable "project_id" {}
variable "topic_names" { type = list(string) }
variable "push_subscriptions" { type = list(string) }
variable "pull_subscriptions" {
  type = map(object({
    name                        = string
    topic            = string   
    ack_deadline_seconds       = number
    message_retention_duration = string
  }))
}
