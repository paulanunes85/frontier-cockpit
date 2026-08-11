#!/usr/bin/env zsh
set -euo pipefail

resource_group="${AZURE_RESOURCE_GROUP:-rg-agentobs-dev-eus-001}"

if ! command -v az >/dev/null 2>&1; then
  print -u2 "Azure CLI was not found."
  exit 1
fi

if ! az account show >/dev/null 2>&1; then
  print -u2 "Azure CLI is not logged in. Run az login first."
  exit 1
fi

print "This will delete the Azure resource group and stop all Azure cost for this demo environment: $resource_group"
print -n "Type DELETE to continue: "
read answer
if [[ "$answer" != "DELETE" ]]; then
  print "Cancelled."
  exit 0
fi

az group delete --name "$resource_group" --yes --no-wait
print "Delete requested for $resource_group. It may take a few minutes to complete."
