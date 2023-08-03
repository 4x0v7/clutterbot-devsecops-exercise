variable "project_id" {
  type        = string
  description = "The GCP Project ID"
  default     = "maximal-relic-394118"
}

variable "region" {
  type        = string
  description = "The default region to use"
  default     = "australia-southeast1"
}

variable "gcp_artifcat_registry_name" {
  description = "Name of the Artifact registry, forms part of the registry url after the project ID eg. australia-southeast1-docker.pkg.dev/maximal-relic-394118/cbot/clutterbot-webapp:v0.0.1"
  type        = string
  default     = "cbot"
}

variable "gcp_docker_image_name" {
  description = "Name of the deployed GCP Docker image name"
  type        = string
  default     = "clutterbot-webapp"
}

variable "gcp_docker_image_tag" {
  description = "Name of the deployed GCP Docker image tag"
  type        = string
  default     = "v0.0.1"
}
