#!/usr/bin/env zsh
set -euo pipefail

# Import a VS Code Agent Debug Logs session export (OTLP JSON) into the local
# Frontier Cockpit stack. The export comes from the Agent Debug Logs panel's
# Export button. Spans are enriched with the current Git workspace attribution
# (workspace.name, workspace.kind, workspace.path_hash, repo, branch) when the
# export does not carry it, so the session shows up grouped by workspace and
# is inspectable in the mini app's Inspector view.
#
# Usage:
#   local-otel/import-agent-debug-session.sh <exported-session.json>
#
# Everything stays local: the file is posted to the local OTel Collector only.

if [[ $# -lt 1 || ! -f "${1:-}" ]]; then
  print -u2 "Usage: $0 <exported-session.json>"
  print -u2 "Export the session from the VS Code Agent Debug Logs panel (Export icon) first."
  exit 2
fi

input_file="$1"
traces_endpoint="${OTEL_EXPORTER_OTLP_TRACES_ENDPOINT:-http://localhost:4318/v1/traces}"
metrics_endpoint="${OTEL_EXPORTER_OTLP_METRICS_ENDPOINT:-http://localhost:4318/v1/metrics}"
logs_endpoint="${OTEL_EXPORTER_OTLP_LOGS_ENDPOINT:-http://localhost:4318/v1/logs}"

workspace_path=""
workspace_name=""
branch=""
remote=""
if git rev-parse --is-inside-work-tree >/dev/null 2>&1; then
  workspace_path="$(git rev-parse --show-toplevel)"
  workspace_name="${workspace_path:t}"
  branch="$(git branch --show-current 2>/dev/null || true)"
  remote="$(git config --get remote.origin.url 2>/dev/null || true)"
fi

WORKSPACE_PATH="$workspace_path" WORKSPACE_NAME="$workspace_name" GIT_BRANCH="$branch" GIT_REMOTE="$remote" \
TRACES_ENDPOINT="$traces_endpoint" METRICS_ENDPOINT="$metrics_endpoint" LOGS_ENDPOINT="$logs_endpoint" \
python3 - "$input_file" <<'PY'
import hashlib
import json
import os
import sys
import urllib.request

input_file = sys.argv[1]
with open(input_file, encoding="utf-8") as handle:
    payload = json.load(handle)

workspace_path = os.environ.get("WORKSPACE_PATH", "")
workspace_name = os.environ.get("WORKSPACE_NAME", "")
branch = os.environ.get("GIT_BRANCH", "")
remote = os.environ.get("GIT_REMOTE", "")
path_hash = hashlib.sha256(workspace_path.encode("utf-8")).hexdigest() if workspace_path else ""

def enrichment():
    attrs = []
    if workspace_name:
        attrs.append({"key": "workspace.name", "value": {"stringValue": workspace_name}})
        attrs.append({"key": "workspace.kind", "value": {"stringValue": "git"}})
    if path_hash:
        attrs.append({"key": "workspace.path_hash", "value": {"stringValue": path_hash}})
    if branch:
        attrs.append({"key": "git.branch", "value": {"stringValue": branch}})
    if remote:
        attrs.append({"key": "github.copilot.git.repository", "value": {"stringValue": remote}})
    attrs.append({"key": "frontier.import.source", "value": {"stringValue": "vscode-agent-debug-export"}})
    return attrs

def enrich_resources(items):
    enriched = 0
    for item in items:
        resource = item.setdefault("resource", {})
        attrs = resource.setdefault("attributes", [])
        existing = {attr.get("key") for attr in attrs}
        for attr in enrichment():
            if attr["key"] not in existing:
                attrs.append(attr)
                enriched += 1
    return enriched

def post(endpoint, body):
    data = json.dumps(body, separators=(",", ":")).encode("utf-8")
    request = urllib.request.Request(endpoint, data=data, headers={"Content-Type": "application/json"}, method="POST")
    with urllib.request.urlopen(request, timeout=30) as response:
        response.read()

sections = [
    ("resourceSpans", os.environ["TRACES_ENDPOINT"]),
    ("resourceMetrics", os.environ["METRICS_ENDPOINT"]),
    ("resourceLogs", os.environ["LOGS_ENDPOINT"]),
]

posted_any = False
for key, endpoint in sections:
    items = payload.get(key) or []
    if not items:
        continue
    enrich_resources(items)
    # Post in batches so very large exports do not exceed collector limits.
    batch_size = 50
    for start in range(0, len(items), batch_size):
        post(endpoint, {key: items[start:start + batch_size]})
    posted_any = True
    print(f"Imported {len(items)} {key} batch(es) to {endpoint}")

if not posted_any:
    print("The file contains no resourceSpans, resourceMetrics, or resourceLogs. Is this an Agent Debug Logs OTLP export?", file=sys.stderr)
    sys.exit(1)

if workspace_name:
    print(f"Attributed to workspace {workspace_name} (branch {branch or 'unknown'}).")
else:
    print("No Git workspace detected; the session was imported without workspace attribution. Run from inside the project repository to attribute it.")
print("The session lands in local Tempo/Prometheus. It appears in the mini app after the next materializer pass (up to 5 minutes) and is inspectable in the Inspector view via its trace id.")
PY
