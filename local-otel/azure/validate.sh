#!/usr/bin/env zsh
set -euo pipefail

script_dir="${0:A:h}"
location="${AZURE_LOCATION:-eastus}"
deployment_name="agentobs-dev-eus-001-validate-$(date +%Y%m%d%H%M%S)"

if ! command -v az >/dev/null 2>&1; then
  print -u2 "Azure CLI was not found."
  exit 1
fi

if ! az account show >/dev/null 2>&1; then
  print -u2 "Azure CLI is not logged in. Run az login first."
  exit 1
fi

collector_token="${AZURE_OTLP_TOKEN:-validation-only-token}"
export AZURE_OTLP_TOKEN="$collector_token"

print "Validating Bicep deployment at subscription scope..."
az deployment sub validate \
  --name "$deployment_name" \
  --location "$location" \
  --template-file "$script_dir/main.bicep" \
  --parameters "$script_dir/main.bicepparam"

print "Running what-if..."
az deployment sub what-if \
  --name "$deployment_name-whatif" \
  --location "$location" \
  --template-file "$script_dir/main.bicep" \
  --parameters "$script_dir/main.bicepparam"
