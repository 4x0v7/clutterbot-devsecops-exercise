variable "appsp_name" {
  description = "Name of Azure App Service plan."
  type        = string
  default     = "cb-webapp-svc"
}

variable "appsvc_name" {
  description = "Name of Azure App."
  type        = string
  default     = "cb-webapp"
}

variable "location" {
  type        = string
  description = "Azure location to create resources in"
  default     = "australiaeast"
}

variable "resource_group_name" {
  type        = string
  description = "Resource Group to house all created resources"
  default     = "cb-webapp-rg-test02" ### TEST02
}

variable "docker_image_name" {
  description = "Name of the deployed Docker image"
  type        = string
  default     = "4x0v7/clutterbot-webapp:v0.0.1"
}

variable "docker_registry_url" {
  description = "URL of the Docker registry"
  type        = string
  default     = "https://ghcr.io"
}

variable "docker_registry_username" {
  description = "Username for the Docker registry"
  type        = string
  default     = "4x0v7"
}

variable "docker_registry_password" {
  description = "Password for the Docker registry"
  type        = string
  sensitive   = true
}

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