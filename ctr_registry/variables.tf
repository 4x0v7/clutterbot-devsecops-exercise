
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

variable "gcloud_docker_image_name" {
  description = "Name of the deployed gcloud Docker image"
  type        = string
  default     = "clutterbot-webapp:v0.0.1"
}
