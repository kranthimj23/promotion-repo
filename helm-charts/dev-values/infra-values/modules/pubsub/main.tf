resource "google_pubsub_topic" "topics" {
  for_each = toset(var.topic_names)
   name     = each.key
}

resource "google_pubsub_subscription" "push_subs" {
  for_each = { for i, name in var.push_subscriptions : name => var.topic_names[i] }
  name     = each.key
  topic    = google_pubsub_topic.topics[each.value].name
}
resource "google_pubsub_subscription" "pull_subs" {
  for_each = var.pull_subscriptions

  name                        = each.value.name
  topic                       = google_pubsub_topic.topics[each.value.topic].name
  ack_deadline_seconds       = each.value.ack_deadline_seconds
  message_retention_duration = each.value.message_retention_duration
}
