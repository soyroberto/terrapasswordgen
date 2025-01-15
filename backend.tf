terraform {
  required_providers {
    azurerm = {
      source  = "hashicorp/azurerm"
      version = "=4.1.0"
    }
  }


  backend "azurerm" {
    resource_group_name  = "rgkvaus"           # Resource group of the storage account
    storage_account_name = "satfpwds"          # Name of the storage account
    container_name       = "terraform-state"   # Name of the container
    key                  = "terraform.tfstate" # Name of the state file
  }
}
provider "azurerm" {
  features {}
}

#USE ENVIRONMENT VARIABLES works better for security

# sh variable setting
# export ARM_CLIENT_ID=" "
# export ARM_CLIENT_SECRET=""
# export ARM_TENANT_ID=""
# export ARM_SUBSCRIPTION_ID=""
#export TF_VAR_client_secret="