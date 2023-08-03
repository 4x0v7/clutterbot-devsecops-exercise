provider "google" {
  project = var.project_id
  region  = var.region
}

resource "google_artifact_registry_repository" "registry" {
  location      = var.region
  repository_id = var.gcp_artifcat_registry_name
  description   = "Docker repository"
  format        = "DOCKER"

  depends_on = [google_project_service.apis]
}

variable "apis" {
  description = "List of apis to enable"
  type        = list(string)
  default = [
    "cloudresourcemanager.googleapis.com", // needed by terraform
    "artifactregistry.googleapis.com",
  ]
}

resource "google_project_service" "apis" {
  for_each = toset(var.apis)
  service  = each.value

  disable_dependent_services = true
}

// user with permission to pull from the Artifact registry
resource "google_service_account" "ctr_puller_user" {
  account_id   = "reader-user"
  display_name = "Container Reader User"
}

resource "google_project_iam_member" "ctr_puller_user" {
  project = var.project_id
  role    = "roles/artifactregistry.reader"
  member  = "serviceAccount:${google_service_account.ctr_puller_user.email}"
}

resource "google_service_account_key" "ctr_puller_key" {
  service_account_id = google_service_account.ctr_puller_user.name
}

// user with permission to psuh to the Artifact registry
resource "google_service_account" "ctr_pusher_user" {
  account_id   = "writer-user"
  display_name = "Container Writer User"
}

resource "google_project_iam_member" "ctr_pusher_user" {
  project = var.project_id
  role    = "roles/artifactregistry.writer"
  member  = "serviceAccount:${google_service_account.ctr_pusher_user.email}"
}

resource "google_service_account_key" "ctr_pusher_key" {
  service_account_id = google_service_account.ctr_pusher_user.name
}

// output service account keys
output "ctr_puller_key" {
  value     = google_service_account_key.ctr_puller_key.private_key
  sensitive = true
}

output "ctr_pusher_key" {
  value     = google_service_account_key.ctr_pusher_key.private_key
  sensitive = true
}
