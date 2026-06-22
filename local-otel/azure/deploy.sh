#!/usr/bin/env zsh
set -euo pipefail

# Deploy the Azure side of the hybrid GitHub Copilot agent observability stack.
# This creates rg-agentobs-dev-eus-001 in East US and resources under it.
# It writes $HOME/frontier-cockpit/local-otel/azure/.env with the cloud Collector endpoint and local token.

script_dir="${0:A:h}"
location="${AZURE_LOCATION:-eastus}"
deployment_name="agentobs-dev-eus-001-$(date +%Y%m%d%H%M%S)"
resource_group="rg-agentobs-dev-eus-001"

if ! command -v az >/dev/null 2>&1; then
  print -u2 "Azure CLI was not found. Install Azure CLI and run az login."
  exit 1
fi

if ! az account show >/dev/null 2>&1; then
  print -u2 "Azure CLI is not logged in. Run az login first."
  exit 1
fi

if [[ -n "${AZURE_OTLP_TOKEN:-}" ]]; then
  collector_token="$AZURE_OTLP_TOKEN"
else
  collector_token="$(python3 - <<'PY'
import secrets
print(secrets.token_urlsafe(48))
PY
)"
fi
export AZURE_OTLP_TOKEN="$collector_token"

print "Running subscription deployment what-if for $resource_group in $location..."
az deployment sub what-if \
  --name "$deployment_name-whatif" \
  --location "$location" \
  --template-file "$script_dir/main.bicep" \
  --parameters "$script_dir/main.bicepparam"

print "Deploying Azure resources..."
outputs_json="$(az deployment sub create \
  --name "$deployment_name" \
  --location "$location" \
  --template-file "$script_dir/main.bicep" \
  --parameters "$script_dir/main.bicepparam" \
  --query properties.outputs \
  -o json)"

collector_fqdn="$(python3 -c 'import json, sys; print(json.loads(sys.argv[1])["containerAppCollectorFqdn"]["value"])' "$outputs_json")"
grafana_endpoint="$(python3 -c 'import json, sys; print(json.loads(sys.argv[1])["grafanaEndpoint"]["value"])' "$outputs_json")"

cat > "$script_dir/.env" <<EOF
AZURE_OTLP_ENDPOINT=https://${collector_fqdn}
AZURE_OTLP_TOKEN=${collector_token}
EOF
chmod 600 "$script_dir/.env"

print ""
print "Azure deployment complete."
print "  Resource group: $resource_group"
print "  Cloud Collector OTLP/HTTP endpoint: https://${collector_fqdn}"
print "  Azure Managed Grafana: ${grafana_endpoint}"
print "  Local hybrid env file written: $script_dir/.env"
print ""
print "Start local hybrid forwarding with:"
print "  $HOME/frontier-cockpit/local-otel/start-full-stack.sh --hybrid"
