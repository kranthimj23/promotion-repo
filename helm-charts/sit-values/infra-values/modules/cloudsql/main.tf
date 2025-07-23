resource "google_sql_database_instance" "postgres" {
  name             = var.db_instance_name
  database_version = "POSTGRES_13"
  region           = var.region
  deletion_protection = false
  settings {
    tier = "db-f1-micro"
  }
}