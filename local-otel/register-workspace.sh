#!/usr/bin/env zsh
set -euo pipefail

# Register the current directory or Git repository as a friendly workspace in local OTel.
# This emits a small OTLP metric with labels that Grafana can use to map
# workspace_path_hash back to a human-readable workspace/repository name.

source "$HOME/frontier-cockpit/local-otel/env.zsh"

endpoint="${OTEL_EXPORTER_OTLP_METRICS_ENDPOINT:-http://localhost:4318/v1/metrics}"
current_dir="$PWD"
workspace_kind="directory"
workspace_name="${current_dir:t}"
workspace_path="$current_dir"
git_branch=""
git_remote=""
git_repo_name=""
git_repo_owner=""

if git_root="$(git rev-parse --show-toplevel 2>/dev/null)"; then
  workspace_kind="git"
  workspace_path="$git_root"
  workspace_name="${git_root:t}"
  git_branch="$(git branch --show-current 2>/dev/null || true)"
  git_remote="$(git config --get remote.origin.url 2>/dev/null || true)"
  if [[ "$git_remote" == git@github.com:* ]]; then
    slug="${git_remote#git@github.com:}"
  elif [[ "$git_remote" == https://github.com/* ]]; then
    slug="${git_remote#https://github.com/}"
  elif [[ "$git_remote" == ssh://git@github.com/* ]]; then
    slug="${git_remote#ssh://git@github.com/}"
  else
    slug="${git_remote:t}"
  fi
  slug="${slug%.git}"
  if [[ "$slug" == */* ]]; then
    git_repo_owner="${slug%%/*}"
    git_repo_name="${slug#*/}"
  else
    git_repo_name="${slug:-$workspace_name}"
  fi
fi

workspace_hash="$(print -rn -- "$workspace_path" | shasum -a 256 | awk '{print $1}')"

python3 <<PY | curl -fsS -X POST "$endpoint" -H 'Content-Type: application/json' --data-binary @- >/dev/null
import json
import time

now = str(time.time_ns())
attrs = {
    "workspace_name": "${workspace_name}",
    "workspace_kind": "${workspace_kind}",
    "workspace_path_hash": "${workspace_hash}",
    "git_branch": "${git_branch}",
    "git_repository_owner": "${git_repo_owner}",
    "git_repository_name": "${git_repo_name}",
    "git_repository_remote": "${git_remote}",
}

def attr(key, value):
    return {"key": key, "value": {"stringValue": value or "unknown"}}

payload = {
    "resourceMetrics": [
        {
            "resource": {
                "attributes": [
                    attr("service.name", "copilot-workspace-registry"),
                    attr("service.version", "1.0.0"),
                    attr("workspace.name", attrs["workspace_name"]),
                    attr("workspace.kind", attrs["workspace_kind"]),
                    attr("workspace.path_hash", attrs["workspace_path_hash"]),
                    attr("git.branch", attrs["git_branch"]),
                    attr("git.repository.owner", attrs["git_repository_owner"]),
                    attr("git.repository.name", attrs["git_repository_name"]),
                    attr("github.copilot.git.repository", attrs["git_repository_remote"]),
                ]
            },
            "scopeMetrics": [
                {
                    "scope": {"name": "copilot-otel-workspace-registry"},
                    "metrics": [
                        {
                            "name": "copilot_workspace_registry",
                            "description": "Friendly workspace registry for local GitHub Copilot OTel dashboards",
                            "unit": "1",
                            "gauge": {
                                "dataPoints": [
                                    {
                                        "timeUnixNano": now,
                                "asInt": "1",
                                "attributes": [],
                                    }
                                ]
                            },
                        }
                    ],
                }
            ],
        }
    ]
}
print(json.dumps(payload, separators=(",", ":")))
PY

if command -v launchctl >/dev/null 2>&1; then
  launchctl setenv OTEL_RESOURCE_ATTRIBUTES "$OTEL_RESOURCE_ATTRIBUTES" 2>/dev/null || true
fi

print "Registered workspace for local OTel dashboards:"
print "  workspace_name=$workspace_name"
print "  workspace_kind=$workspace_kind"
print "  workspace_path_hash=$workspace_hash"
print "  git_repository_name=${git_repo_name:-unknown}"
print "  git_branch=${git_branch:-unknown}"
