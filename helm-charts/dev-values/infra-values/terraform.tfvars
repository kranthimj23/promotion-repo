project_id   = "nice-virtue-463917-m0"
region       = "us-central1"
zone       = "us-central1-a"
cluster_name = "demo-gke-cluster"
db_instance_name = "demo-postgres-db"
vm_name = "demo-jenkins-vm"
topic_names = [
  "topic-1", "topic-2", "topic-3", "topic-4", "topic-5",
  "topic-6", "topic-7", "topic-8", "topic-9", "topic-10"
]
push_subscriptions = [
  "sub-1", "sub-2", "sub-3", "sub-4", "sub-5"
]
buckets = {
project-dev-bucket-1  = {

        storage_class               = "<<storage_class>>"

        force_destroy               = true

        uniform_bucket_level_access = true

        enable_versioning           = true

        retention_policy            = 3600

        labels                      = {
      environment = "dev"
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


project-dev-bucket-2  = {

        storage_class               = "<<storage_class>>"

        force_destroy               = false

        uniform_bucket_level_access = false

        enable_versioning           = false

        retention_policy            = 0


        lifecycle_rules = [

          {


            condition = {


            }

          }

        ]

        cors = [

          {





          }

        ]

  },


project-dev-bucket-3  = {

        storage_class               = "<<storage_class>>"

        force_destroy               = true

        uniform_bucket_level_access = true

        enable_versioning           = false

        retention_policy            = 86400

        labels                      = {
      project = "infra"
    }

        lifecycle_rules = [

          {

            action_type = "Delete"

            condition = {

              age = 60

            }

          }

        ]

        cors = [

          {





          }

        ]

  },


project-dev-bucket-4  = {

        storage_class               = "<<storage_class>>"

        force_destroy               = true

        uniform_bucket_level_access = true

        enable_versioning           = true

        retention_policy            = 0

        labels                      = {
      environment = "archive"
    }

        lifecycle_rules = [

          {


            condition = {


            }

          }

        ]

        cors = [

          {





          }

        ]

  },


project-dev-bucket-5  = {

        storage_class               = "<<storage_class>>"

        force_destroy               = false

        uniform_bucket_level_access = false

        enable_versioning           = false

        retention_policy            = 0


        lifecycle_rules = [

          {


            condition = {


            }

          }

        ]

        cors = [

          {





          }

        ]

  },


project-dev-bucket-6  = {

        storage_class               = "<<storage_class>>"

        force_destroy               = true

        uniform_bucket_level_access = true

        enable_versioning           = true

        retention_policy            = 7200

        labels                      = {
      managed = "yes"
    }

        lifecycle_rules = [

          {

            action_type = "Delete"

            condition = {

              age = 15

            }

          }

        ]

        cors = [

          {





          }

        ]

  },


project-dev-bucket-7  = {

        storage_class               = "<<storage_class>>"

        force_destroy               = true

        uniform_bucket_level_access = true

        enable_versioning           = false

        retention_policy            = 0


        lifecycle_rules = [

          {


            condition = {


            }

          }

        ]

        cors = [

          {

                origin          = ["https://myapp.com"]

                method          = ["PUT"]

                response_header = ["Authorization"]

                max_age_seconds = 1800

          }

        ]

  },


project-dev-bucket-8  = {

        storage_class               = "<<storage_class>>"

        force_destroy               = true

        uniform_bucket_level_access = true

        enable_versioning           = true

        retention_policy            = 2592000

        labels                      = {
      owner = "kranthi"
    }

        lifecycle_rules = [

          {


            condition = {


            }

          }

        ]

        cors = [

          {





          }

        ]

  },


}
pull_subscriptions = {
pull-sub-6 = {

    name                        = "pull-sub-6"

    topic                       = "topic-6"

    ack_deadline_seconds       = "10"

    message_retention_duration = "600s"

  },

pull-sub-7 = {

    name                        = "pull-sub-7"

    topic                       = "topic-7"

    ack_deadline_seconds       = "15"

    message_retention_duration = "1200s"

  },

pull-sub-8 = {

    name                        = "pull-sub-8"

    topic                       = "topic-8"

    ack_deadline_seconds       = "20"

    message_retention_duration = "1800s"

  },

}
