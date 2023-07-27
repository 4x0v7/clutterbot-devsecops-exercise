terraform {
  required_version = ">= 1.5.4"

  # constrained by modules
  required_providers {
    azurerm = {
      source  = "hashicorp/azurerm"
      version = "~> 3.66.0"
    }
    azuread = {
      source  = "hashicorp/azuread"
      version = "~> 2.40.0"
    }
    google = ">= 3.3"
  }
}

provider "azuread" {
  tenant_id = "047da47d-3089-4cb5-80d2-a35fddca14fa"
}

provider "azurerm" {
  # This is only required when the User, Service Principal, or Identity running Terraform lacks the permissions to register Azure Resource Providers.
  # My trial account has some providers stuck at "Registering" which may take hours to complete on the Azure side
  skip_provider_registration = true
  features {
  }
  subscription_id = "abc58b58-ce47-4819-b66e-7d1c4ec02b29" # Azure-trial-subscription
}
