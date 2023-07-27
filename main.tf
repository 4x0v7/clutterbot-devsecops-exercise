
provider "google" {
  project = var.project_id
  region  = var.region
}
resource "google_project_service" "run" {
  service = "run.googleapis.com"
}

resource "google_cloud_run_service" "app_svc" {
  name     = "webapp"
  location = var.region

  template {
    spec {
      containers {
        image = "${var.region}-docker.pkg.dev/${var.project_id}/cbot/${var.gcloud_docker_image_name}"
        ports {
          container_port = 2772
        }
      }
    }
  }

  traffic {
    percent         = 100
    latest_revision = true
  }

  depends_on = [google_project_service.run]
}

resource "google_cloud_run_service_iam_member" "public_access" {
  service  = google_cloud_run_service.app_svc.name
  location = google_cloud_run_service.app_svc.location
  role     = "roles/run.invoker"
  member   = "allUsers"
}
