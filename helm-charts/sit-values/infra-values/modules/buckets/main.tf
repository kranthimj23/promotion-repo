resource "google_storage_bucket" "buckets" {
  for_each = var.buckets

  name     = each.key
  location = "US"

  storage_class               = each.value.storage_class
  force_destroy               = each.value.force_destroy
  uniform_bucket_level_access = each.value.uniform_bucket_level_access

  dynamic "versioning" {
    for_each = each.value.enable_versioning ? [1] : []
    content {
      enabled = true
    }
  }

  dynamic "retention_policy" {
    for_each = each.value.retention_policy > 0 ? [1] : []
    content {
      retention_period = each.value.retention_policy
    }
  }

  labels = each.value.labels

  dynamic "lifecycle_rule" {
    for_each = each.value.lifecycle_rules
    content {
      action {
        type = lifecycle_rule.value.action_type
      }
      condition = lifecycle_rule.value.condition
    }
  }

  dynamic "cors" {
    for_each = each.value.cors
    content {
      origin          = cors.value.origin
      method          = cors.value.method
      response_header = cors.value.response_header
      max_age_seconds = cors.value.max_age_seconds
    }
  }
}
