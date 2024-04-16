terraform {
  required_providers {
    google = {
      source  = "hashicorp/google"
      version = "5.2.0"
    }
  }
}

provider "google" {
  project     = ""
  credentials = file("credentials.json")
  region      = "us-central1"
  zone        = "us-central1-c"
}

resource "google_compute_instance" "web_server" {
  machine_type              = "c3-standard-4"
  name                      = "web-server-instance"
  description               = "FASTAPI RASI web server"
  allow_stopping_for_update = true


  boot_disk {
    initialize_params {
      image = "ubuntu-os-cloud/ubuntu-minimal-2204-lts"
    }
  }

  network_interface {
    network = "default"
    access_config {
      // Ephemeral public IP
    }
  }
}

resource "google_compute_instance" "db_server" {
  machine_type              = "c3-standard-4"
  name                      = "db-server-instance"
  description               = "PostgreSQL server"
  allow_stopping_for_update = true

  boot_disk {
    initialize_params {
      image = "ubuntu-os-cloud/ubuntu-minimal-2204-lts"
    }
  }

  network_interface {
    network = "default"
    access_config {
      // Ephemeral public IP
    }
  }
}
