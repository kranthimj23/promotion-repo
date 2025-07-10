resource "google_compute_instance" "jenkins" {
  name         = var.vm_name
  machine_type = "e2-micro"
  zone         = var.zone
  deletion_protection = false
  boot_disk {
    initialize_params {
      image = "ubuntu-os-cloud/ubuntu-2204-lts"
    }
  }

  network_interface {
    network = "default"
    access_config {}
  }
}