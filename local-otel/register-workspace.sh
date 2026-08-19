#!/usr/bin/env zsh
set -euo pipefail

# Register the current directory or Git repository as a friendly workspace in local OTel.
# This emits a small OTLP metric with labels that Grafana can use to map
# workspace_path_hash back to a human-readable workspace/repository name.

source "${0:A:h}/env.zsh"

endpoint="${OTEL_EXPORTER_OTLP_METRICS_ENDPOINT:-http://localhost:4318/v1/metrics}"
current_dir="$PWD"
workspace_kind="directory"
workspace_name="${current_dir:t}"
workspace_path="$current_dir"
git_branch=""
git_remote=""
git_repo_name=""
git_repo_owner=""
git_head_commits=""

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
  # Capture the HEAD commit of every local branch. GitHub Copilot emits the
  # per-window HEAD commit hash, which is the only reliable signal to attribute
  # a workspace when VS Code is launched from the GUI and inherits a shared
  # global environment. The materializer matches these commits back to this repo.
  git_head_commits="$(git for-each-ref --format='%(objectname)' refs/heads 2>/dev/null | sort -u | tr '\n' ' ' | sed -e 's/  */ /g' -e 's/^ //' -e 's/ $//')"
  git_head="$(git rev-parse HEAD 2>/dev/null || true)"
  if [[ -n "$git_head" && " $git_head_commits " != *" $git_head "* ]]; then
    git_head_commits="$git_head $git_head_commits"
  fi
fi

workspace_hash="$(print -rn -- "$workspace_path" | shasum -a 256 | awk '{print $1}')"
state_dir="${0:A:h}/workspaces"
registry_cache="$state_dir/registry-cache.tsv"
mkdir -p "$state_dir"

# Persist the same metadata published below so the registry sidecar can keep
# the gauge alive after Collector restarts and Prometheus-exporter expiration.
FRONTIER_WORKSPACE_HASH="$workspace_hash" \
FRONTIER_WORKSPACE_NAME="$workspace_name" \
FRONTIER_WORKSPACE_KIND="$workspace_kind" \
FRONTIER_GIT_BRANCH="$git_branch" \
FRONTIER_GIT_REPO_OWNER="$git_repo_owner" \
FRONTIER_GIT_REPO_NAME="$git_repo_name" \
FRONTIER_GIT_REMOTE="$git_remote" \
FRONTIER_GIT_HEAD_COMMITS="$git_head_commits" \
python3 - "$registry_cache" <<'PY'
import os
import pathlib
import time
import sys

cache_path = pathlib.Path(sys.argv[1])


def clean(value):
  return str(value or "unknown").replace("\t", " ").replace("\r", " ").replace("\n", " ")


rows = {}
if cache_path.exists():
  for line in cache_path.read_text(encoding="utf-8").splitlines():
    parts = line.split("\t")
    if len(parts) >= 9:
      rows[parts[0]] = parts[:9]

row = [
  clean(os.environ.get("FRONTIER_WORKSPACE_HASH")),
  clean(os.environ.get("FRONTIER_WORKSPACE_NAME")),
  clean(os.environ.get("FRONTIER_WORKSPACE_KIND")),
  clean(os.environ.get("FRONTIER_GIT_BRANCH")),
  clean(os.environ.get("FRONTIER_GIT_REPO_OWNER")),
  clean(os.environ.get("FRONTIER_GIT_REPO_NAME")),
  clean(os.environ.get("FRONTIER_GIT_REMOTE")),
  clean(os.environ.get("FRONTIER_GIT_HEAD_COMMITS")),
  str(int(time.time())),
]
rows[row[0]] = row

tmp = cache_path.with_suffix(".tmp")
tmp.write_text("".join("\t".join(item) + "\n" for item in sorted(rows.values(), key=lambda item: item[1].lower())), encoding="utf-8")
tmp.replace(cache_path)
PY

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
    "git_head_commit": "${git_head_commits}",
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
                    attr("git.head_commit", attrs["git_head_commit"]),
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

# Intentionally do NOT push workspace tags into the global launchd environment.
# macOS launchd holds a single global OTEL_RESOURCE_ATTRIBUTES, so exporting one
# workspace there would mislabel every other GUI-launched VS Code window. Per-window
# attribution comes from the per-shell environment (terminal-launched windows) and
# from commit-hash matching against this registry in materialize-copilot-sessions.sh.

print "Registered workspace for local OTel dashboards:"
print "  workspace_name=$workspace_name"
print "  workspace_kind=$workspace_kind"
print "  workspace_path_hash=$workspace_hash"
print "  git_repository_name=${git_repo_name:-unknown}"
print "  git_branch=${git_branch:-unknown}"
