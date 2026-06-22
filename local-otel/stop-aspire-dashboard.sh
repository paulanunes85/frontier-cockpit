#!/usr/bin/env zsh
set -euo pipefail

container_name="aspire-dashboard"

if ! command -v docker >/dev/null 2>&1; then
  print -u2 "Docker CLI was not found."
  exit 1
fi

if ! docker info >/dev/null 2>&1; then
  print -u2 "Docker daemon is not running. Nothing was stopped."
  exit 0
fi

running_id="$(docker ps -q -f "name=^/${container_name}$" || true)"
if [[ -z "$running_id" ]]; then
  print "Aspire Dashboard is not running."
  exit 0
fi

docker stop "$container_name" >/dev/null
print "Aspire Dashboard stopped."
