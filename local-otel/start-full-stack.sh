#!/usr/bin/env zsh
set -euo pipefail

# Start the full local observability stack: OTel Collector + Aspire + Tempo + Prometheus +
# Loki + Grafana + registry/jobs sidecars + the Frontier Cockpit Local mini app.
# Pass --hybrid to also forward telemetry to the Azure cloud Collector (requires
# local-otel/azure/.env with AZURE_OTLP_ENDPOINT and AZURE_OTLP_TOKEN).
# Pass --update after a git pull to upgrade in place: it first rebuilds the locally
# built images (dashboard API, web app, registry, jobs) against the new source and
# pulls newer pinned tags — so a failed build leaves the running stack untouched —
# then stops the stack, removes orphaned containers from older layouts, and starts
# everything again. Named volumes are never touched, so Prometheus history, Grafana
# settings, and the permanent DuckDB analytics survive the upgrade.

script_dir="${0:A:h}"
stack_dir="$script_dir/stack"
hybrid=0
update=0

for arg in "$@"; do
  case "$arg" in
    --hybrid) hybrid=1 ;;
    --update) update=1 ;;
    *) print -u2 "Unknown argument: $arg"; exit 2 ;;
  esac
done

if ! command -v docker >/dev/null 2>&1; then
  print -u2 "Docker CLI was not found. Install Docker Desktop, then run this script again."
  exit 1
fi

if ! docker info >/dev/null 2>&1; then
  print -u2 "Docker is installed, but the daemon is not running. Start Docker Desktop, wait until it is ready, then run this script again."
  exit 1
fi

# A leftover standalone Aspire container from older setups can publish host ports 4317/4318.
# In full-stack mode the OTel Collector owns those ports, so stop the standalone one first.
if docker ps --format '{{.Names}}' | grep -qx 'aspire-dashboard'; then
  standalone_owns_otlp="$(docker port aspire-dashboard 18890/tcp 2>/dev/null || true)"
  if [[ "$standalone_owns_otlp" == *":4318"* ]]; then
    print "Stopping the standalone Aspire container to free OTLP ports 4317/4318 for the Collector."
    docker stop aspire-dashboard >/dev/null 2>&1 || true
  fi
fi

cd "$stack_dir"

aspire_key_file="$stack_dir/aspire-api-key.env"
if [[ ! -f "$aspire_key_file" ]]; then
  umask 077
  python3 - <<'PY' > "$aspire_key_file"
import secrets
print(f"ASPIRE_DASHBOARD_API_KEY={secrets.token_urlsafe(32)}")
PY
fi

grafana_admin_file="$stack_dir/grafana-admin.env"
if [[ ! -f "$grafana_admin_file" ]]; then
  umask 077
  python3 - <<'PY' > "$grafana_admin_file"
import secrets
print(f"GF_SECURITY_ADMIN_PASSWORD={secrets.token_urlsafe(24)}")
PY
  print "Created Grafana admin credentials (user admin, password in $grafana_admin_file)."
fi

set -a
source "$aspire_key_file"
set +a

compose_files=(-f docker-compose.yml)
if [[ "$hybrid" -eq 1 ]]; then
  env_file="$script_dir/azure/.env"
  if [[ -f "$env_file" ]]; then
    set -a
    source "$env_file"
    set +a
  fi
  if [[ -z "${AZURE_OTLP_ENDPOINT:-}" || -z "${AZURE_OTLP_TOKEN:-}" ]]; then
    print -u2 "Hybrid mode needs AZURE_OTLP_ENDPOINT and AZURE_OTLP_TOKEN."
    print -u2 "Provision the Azure side first ($script_dir/azure/deploy.sh) and write $script_dir/azure/.env."
    exit 1
  fi
  compose_files+=(-f docker-compose.azure.yaml)
fi

if [[ "$update" -eq 1 ]]; then
  # Build before stopping anything: if the rebuild fails (offline, registry
  # rate limit), the currently running stack stays up untouched.
  print "Updating the local stack: rebuilding locally built images against the current source and pulling newer base images."
  docker compose "${compose_files[@]}" build --pull
  print "Stopping containers and removing orphans (named volumes are preserved)."
  docker compose "${compose_files[@]}" down --remove-orphans
fi

if [[ "$hybrid" -eq 1 ]]; then
  print "Starting full stack in hybrid mode (local backends + Azure forwarding)."
else
  print "Starting full local stack (offline, no Azure forwarding)."
fi
docker compose "${compose_files[@]}" up -d

print ""
print "Endpoints:"
print "  OTLP ingest (Collector):  http://localhost:4318  (HTTP)   http://localhost:4317  (gRPC)"
print "  Aspire Dashboard (live):  http://localhost:18888"
print "  Grafana (history):        http://localhost:3000  (user admin, password in stack/grafana-admin.env)"
print "  Prometheus:               http://localhost:9090"
print "  Tempo:                    http://localhost:3200"
print "  Loki:                     http://localhost:3100"
print ""
if [[ "$update" -eq 1 ]]; then
  print "Update complete. Hard-refresh the dashboard at http://localhost:3300 (Cmd/Ctrl+Shift+R) so the browser drops the cached app."
fi
print "Reload VS Code or VS Code Insiders, run a GitHub Copilot Chat agent request, then check Aspire and Grafana."
