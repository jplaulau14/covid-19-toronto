#!/bin/bash

# Get the absolute path of the script
SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" &> /dev/null && pwd )"
# Print SCRIPT_DIR

cd "$SCRIPT_DIR/.."

# Export the GCP credentials
export GOOGLE_APPLICATION_CREDENTIALS="/Users/pats/Desktop/covid-19-toronto/gcp_key.json"

cd terraform
# Run the requested Terraform command
terraform init
terraform apply
