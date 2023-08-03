
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
  description = "Name of the Artifact registry, forms part of the registry url eg. australia-southeast1-docker.pkg.dev/maximal-relic-394118/cbot/clutterbot-webapp:v0.0.1"
  type        = string
  default     = "cbot"
}
