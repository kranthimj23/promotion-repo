project_id   = "devops-ai-labs-1"
region       = "us-central1"
zone       = "us-central1-a"
cluster_name = "demo-sit-gke-cluster"
db_instance_name = "demo-sit-postgres-db"
vm_name = "demo-sit-jenkins-vm"
topic_names = [
  "topic-sit-1", "topic-sit-2", "topic-sit-3", "topic-sit-4", "topic-sit-5",
  "topic-sit-6", "topic-sit-7", "topic-sit-8", "topic-sit-9", "topic-sit-10"
]
push_subscriptions = [
  "sub-sit-1", "sub-sit-2", "sub-sit-3", "sub-sit-4", "sub-sit-5"
]
buckets = {
project-sit-bucket-1  = {

        storage_class               = "STANDARD"

        force_destroy               = true

        uniform_bucket_level_access = true

        enable_versioning           = true

        retention_policy            = 3600

        labels                      = {
      environment = "sit"
      team        = "platform"
    }

        lifecycle_rules = [

          {

            action_type = "Delete"

            condition = {

              age = 30

            }

          }

        ]

        cors = [

          {

                origin          = ["*"]

                method          = ["GET"]

                response_header = ["Content-Type"]

                max_age_seconds = 3600

          }

        ]

  },


project-sit-bucket-2  = {

        storage_class               = "NEARLINE"

        force_destroy               = false

        uniform_bucket_level_access = false

        enable_versioning           = false

        retention_policy            = 0

        labels                      = {
      environment = "sit"
      team        = "platform"
    }

        lifecycle_rules = [

          {

            action_type = "Delete"

            condition = {

              age = 30

            }

          }

        ]

        cors = [

          {

                origin          = ["*"]

                method          = ["GET"]

                response_header = ["Content-Type"]

                max_age_seconds = 3600

          }

        ]

  },


project-sit-bucket-3  = {

        storage_class               = "STANDARD"

        force_destroy               = true

        uniform_bucket_level_access = true

        enable_versioning           = false

        retention_policy            = 86400

        labels                      = {
      environment = "sit"
      team        = "platform"
    }

        lifecycle_rules = [

          {

            action_type = "Delete"

            condition = {

              age = 30

            }

          }

        ]

        cors = [

          {

                origin          = ["*"]

                method          = ["GET"]

                response_header = ["Content-Type"]

                max_age_seconds = 3600

          }

        ]

  },


project-sit-bucket-4  = {

        storage_class               = "ARCHIVE"

        force_destroy               = true

        uniform_bucket_level_access = true

        enable_versioning           = true

        retention_policy            = 0

        labels                      = {
      environment = "sit"
      team        = "platform"
    }

        lifecycle_rules = [

          {

            action_type = "Delete"

            condition = {

              age = 30

            }

          }

        ]

        cors = [

          {

                origin          = ["*"]

                method          = ["GET"]

                response_header = ["Content-Type"]

                max_age_seconds = 3600

          }

        ]

  },


project-sit-bucket-5  = {

        storage_class               = "COLDLINE"

        force_destroy               = false

        uniform_bucket_level_access = false

        enable_versioning           = false

        retention_policy            = 0

        labels                      = {
      environment = "sit"
      team        = "platform"
    }

        lifecycle_rules = [

          {

            action_type = "Delete"

            condition = {

              age = 30

            }

          }

        ]

        cors = [

          {

                origin          = ["*"]

                method          = ["GET"]

                response_header = ["Content-Type"]

                max_age_seconds = 3600

          }

        ]

  },


project-sit-bucket-6  = {

        storage_class               = "STANDARD"

        force_destroy               = true

        uniform_bucket_level_access = true

        enable_versioning           = true

        retention_policy            = 7200

        labels                      = {
      environment = "sit"
      team        = "platform"
    }

        lifecycle_rules = [

          {

            action_type = "Delete"

            condition = {

              age = 30

            }

          }

        ]

        cors = [

          {

                origin          = ["*"]

                method          = ["GET"]

                response_header = ["Content-Type"]

                max_age_seconds = 3600

          }

        ]

  },


project-sit-bucket-7  = {

        storage_class               = "STANDARD"

        force_destroy               = true

        uniform_bucket_level_access = true

        enable_versioning           = false

        retention_policy            = 0

        labels                      = {
      environment = "sit"
      team        = "platform"
    }

        lifecycle_rules = [

          {

            action_type = "Delete"

            condition = {

              age = 30

            }

          }

        ]

        cors = [

          {

                origin          = ["*"]

                method          = ["GET"]

                response_header = ["Content-Type"]

                max_age_seconds = 3600

          }

        ]

  },


project-sit-bucket-8  = {

        storage_class               = "STANDARD"

        force_destroy               = true

        uniform_bucket_level_access = true

        enable_versioning           = true

        retention_policy            = 2592000

        labels                      = {
      environment = "sit"
      team        = "platform"
    }

        lifecycle_rules = [

          {

            action_type = "Delete"

            condition = {

              age = 30

            }

          }

        ]

        cors = [

          {

                origin          = ["*"]

                method          = ["GET"]

                response_header = ["Content-Type"]

                max_age_seconds = 3600

          }

        ]

  },


project-sit-bucket-9  = {

        storage_class               = "NEARLINE"

        force_destroy               = false

        uniform_bucket_level_access = false

        enable_versioning           = true

        retention_policy            = 0

        labels                      = {
      environment = "sit"
      team        = "platform"
    }

        lifecycle_rules = [

          {

            action_type = "Delete"

            condition = {

              age = 30

            }

          }

        ]

        cors = [

          {

                origin          = ["*"]

                method          = ["GET"]

                response_header = ["Content-Type"]

                max_age_seconds = 3600

          }

        ]

  },


project-sit-bucket-10  = {

        storage_class               = "COLDLINE"

        force_destroy               = false

        uniform_bucket_level_access = false

        enable_versioning           = false

        retention_policy            = 0

        labels                      = {
      environment = "sit"
      team        = "platform"
    }

        lifecycle_rules = [

          {

            action_type = "Delete"

            condition = {

              age = 30

            }

          }

        ]

        cors = [

          {

                origin          = ["*"]

                method          = ["GET"]

                response_header = ["Content-Type"]

                max_age_seconds = 3600

          }

        ]

  },


project-sit-bucket-11  = {

        storage_class               = "COLDLINE"

        force_destroy               = false

        uniform_bucket_level_access = false

        enable_versioning           = false

        retention_policy            = 0

        labels                      = {
      environment = "sit"
      team        = "platform"
    }

        lifecycle_rules = [

          {

            action_type = "Delete"

            condition = {

              age = 30

            }

          }

        ]

        cors = [

          {

                origin          = ["*"]

                method          = ["GET"]

                response_header = ["Content-Type"]

                max_age_seconds = 3600

          }

        ]

  },


}
pull_subscriptions = {
pull-sub-sit-6 = {

    name                        = "pull-sub-sit-6"

    topic                       = "topic-sit-6"

    ack_deadline_seconds       = "10"

    message_retention_duration = "600s"

  },

pull-sub-sit-7 = {

    name                        = "pull-sub-sit-7"

    topic                       = "topic-sit-7"

    ack_deadline_seconds       = "15"

    message_retention_duration = "1200s"

  },

pull-sub-sit-8 = {

    name                        = "pull-sub-sit-8"

    topic                       = "topic-sit-8"

    ack_deadline_seconds       = "20"

    message_retention_duration = "1800s"

  },

pull-sub-sit-9 = {

    name                        = "pull-sub-sit-9"

    topic                       = "topic-sit-9"

    ack_deadline_seconds       = "30"

    message_retention_duration = "2400s"

  },

pull-sub-sit-10 = {

    name                        = "pull-sub-sit-10"

    topic                       = "topic-sit-10"

    ack_deadline_seconds       = "60"

    message_retention_duration = "3600s"

  },

pull-sub-sit-12 = {

    name                        = "pull-sub-sit-12"

    topic                       = "topic-sit-10"

    ack_deadline_seconds       = "60"

    message_retention_duration = "3600s"

  },

pull-sub-sit-11 = {

    name                        = "pull-sub-sit-11"

    topic                       = "topic-sit-9"

    ack_deadline_seconds       = "60"

    message_retention_duration = "1200s"

  },

}
