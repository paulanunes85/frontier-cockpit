#!/usr/bin/env zsh
set -euo pipefail

# User-login autostart for the GitHub Copilot OTel stack.
# It applies the user environment, waits for Docker Desktop, then starts:
# - full local stack by default
# - hybrid stack automatically when $HOME/frontier-cockpit/local-otel/azure/.env exists

log_dir="$HOME/frontier-cockpit/local-otel"
log_file="$log_dir/auto-start.log"
mkdir -p "$log_dir"
export PATH="/opt/homebrew/bin:/usr/local/bin:/usr/bin:/bin:/usr/sbin:/sbin:$HOME/.local/bin"
timestamp() { date '+%Y-%m-%dT%H:%M:%S%z'; }

{
  print "[$(timestamp)] Starting GitHub Copilot OTel autostart."

  if [[ -x "$HOME/frontier-cockpit/local-otel/enable-user-env.sh" ]]; then
    "$HOME/frontier-cockpit/local-otel/enable-user-env.sh" || true
  fi

  if ! command -v docker >/dev/null 2>&1; then
    print "[$(timestamp)] Docker CLI not found. Autostart skipped."
    exit 0
  fi

  # Launch Docker Desktop if it is installed and not yet running.
  open -a Docker >/dev/null 2>&1 || true

  ready=0
  for attempt in {1..60}; do
    if docker info >/dev/null 2>&1; then
      ready=1
      break
    fi
    sleep 5
  done

  if [[ "$ready" -ne 1 ]]; then
    print "[$(timestamp)] Docker did not become ready after 5 minutes. Autostart skipped."
    exit 0
  fi

  if [[ -f "$HOME/frontier-cockpit/local-otel/azure/.env" ]]; then
    print "[$(timestamp)] Azure env found. Starting hybrid stack."
    "$HOME/frontier-cockpit/local-otel/start-full-stack.sh" --hybrid
  else
    print "[$(timestamp)] Azure env not found. Starting full local stack."
    "$HOME/frontier-cockpit/local-otel/start-full-stack.sh"
  fi

  print "[$(timestamp)] GitHub Copilot OTel autostart completed."
} >> "$log_file" 2>&1
