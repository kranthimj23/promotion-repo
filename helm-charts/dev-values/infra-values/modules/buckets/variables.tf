variable "project_id" {}
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
