#!/usr/bin/env zsh
set -euo pipefail

# Configure or renew GitHub Enterprise audit log streaming to Azure Blob Storage.
# Uses a user delegation SAS because the storage account blocks Shared Key authentication.
# The SAS is encrypted with the GitHub Enterprise audit-log stream public key before it is
# sent to GitHub. The raw SAS is saved only in the local 0600 env file.

export PATH="/opt/homebrew/bin:/usr/local/bin:/usr/bin:/bin:/usr/sbin:/sbin:$HOME/.local/bin"

enterprise="${GITHUB_ENTERPRISE_SLUG:-your-enterprise-slug}"
subscription="${AZURE_SUBSCRIPTION_ID:-00000000-0000-0000-0000-000000000000}"
resource_group="${AZURE_RESOURCE_GROUP:-rg-agentobs-dev-eus-001}"
account_file="$HOME/frontier-cockpit/local-otel/azure/audit-storage-account.txt"
container_file="$HOME/frontier-cockpit/local-otel/azure/audit-storage-container.txt"
env_file="$HOME/frontier-cockpit/local-otel/azure/github-enterprise-audit-log-streaming.env"
state_file="$HOME/frontier-cockpit/local-otel/azure/github-enterprise-audit-stream-state.json"
python_bin="$HOME/frontier-cockpit/local-otel/.venv/bin/python"

if [[ ! -x "$python_bin" ]]; then
  print -u2 "Missing PyNaCl environment at $python_bin. Run the setup step first."
  exit 1
fi

if [[ ! -f "$account_file" || ! -f "$container_file" ]]; then
  print -u2 "Missing audit storage account/container files under $HOME/frontier-cockpit/local-otel/azure."
  exit 1
fi

account="$(cat "$account_file")"
container="$(cat "$container_file")"

az account set --subscription "$subscription"

# Ensure the signed-in user can generate a user-delegation SAS and validate blobs.
storage_id="$(az storage account show --subscription "$subscription" -g "$resource_group" -n "$account" --query id -o tsv)"
principal="$(az ad signed-in-user show --query id -o tsv)"
az role assignment create --assignee "$principal" --role "Storage Blob Data Contributor" --scope "$storage_id" -o none 2>/dev/null || true

# User delegation SAS maximum validity is limited by Azure. Use 7 days and renew daily.
start="$(date -u -v-5M '+%Y-%m-%dT%H:%MZ')"
expiry="$(date -u -v+7d '+%Y-%m-%dT%H:%MZ')"
az account set --subscription "$subscription"
sas="$(az storage container generate-sas \
  --account-name "$account" \
  --name "$container" \
  --auth-mode login \
  --as-user \
  --permissions acdlrw \
  --start "$start" \
  --expiry "$expiry" \
  --https-only \
  -o tsv)"
container_sas_url="https://${account}.blob.core.windows.net/${container}?${sas}"
blob_service_sas_url="https://${account}.blob.core.windows.net/?${sas}"

# Validate SAS before giving it to GitHub.
sas_token="${container_sas_url#*\?}"
test_file="$(/usr/bin/mktemp /tmp/github-audit-stream.XXXXXX)"
printf '{"test":"github-audit-stream","enterprise":"%s","time":"%s"}\n' "$enterprise" "$(date -u '+%Y-%m-%dT%H:%M:%SZ')" > "$test_file"
az storage blob upload \
  --account-name "$account" \
  --container-name "$container" \
  --name "_controltower/github-stream-connectivity.json" \
  --file "$test_file" \
  --sas-token "$sas_token" \
  --overwrite true \
  -o none
/bin/rm -f "$test_file"

stream_key_json="$(gh api -H 'Accept: application/vnd.github+json' -H 'X-GitHub-Api-Version: 2026-03-10' "/enterprises/${enterprise}/audit-log/stream-key")"
key_id="$(printf '%s' "$stream_key_json" | "$python_bin" -c 'import json,sys; print(json.load(sys.stdin)["key_id"])')"
public_key="$(printf '%s' "$stream_key_json" | "$python_bin" -c 'import json,sys; print(json.load(sys.stdin)["key"])')"

encrypted_sas_url="$("$python_bin" - "$public_key" "$container_sas_url" <<'PY'
import base64
import sys
from nacl.public import PublicKey, SealedBox
public_key_b64 = sys.argv[1]
secret_value = sys.argv[2]
public_key = PublicKey(base64.b64decode(public_key_b64))
sealed_box = SealedBox(public_key)
encrypted = sealed_box.encrypt(secret_value.encode('utf-8'))
print(base64.b64encode(encrypted).decode('utf-8'))
PY
)"

body_file="$(/usr/bin/mktemp /tmp/github-audit-stream-body.XXXXXX)"
cat > "$body_file" <<JSON
{
  "enabled": true,
  "stream_type": "Azure Blob Storage",
  "vendor_specific": {
    "key_id": "$key_id",
    "encrypted_sas_url": "$encrypted_sas_url",
    "container": "$container"
  }
}
JSON

streams_file="$(/usr/bin/mktemp /tmp/github-audit-streams.XXXXXX)"
gh api -H 'Accept: application/vnd.github+json' -H 'X-GitHub-Api-Version: 2026-03-10' "/enterprises/${enterprise}/audit-log/streams" > "$streams_file"
stream_id="$("$python_bin" - "$streams_file" <<'PY'
import json, sys
try:
  streams = json.load(open(sys.argv[1]))
except Exception:
    streams = []
for stream in streams:
    if stream.get('stream_type') == 'Azure Blob Storage':
        print(stream.get('id'))
        break
PY
)"
      /bin/rm -f "$streams_file"

if [[ -n "$stream_id" ]]; then
  result_json="$(gh api -X PUT -H 'Accept: application/vnd.github+json' -H 'X-GitHub-Api-Version: 2026-03-10' "/enterprises/${enterprise}/audit-log/streams/${stream_id}" --input "$body_file")"
  action="updated"
else
  result_json="$(gh api -X POST -H 'Accept: application/vnd.github+json' -H 'X-GitHub-Api-Version: 2026-03-10' "/enterprises/${enterprise}/audit-log/streams" --input "$body_file")"
  action="created"
fi
/bin/rm -f "$body_file"

new_stream_id="$(printf '%s' "$result_json" | "$python_bin" -c 'import json,sys; print(json.load(sys.stdin).get("id", ""))')"
stream_enabled="$(printf '%s' "$result_json" | "$python_bin" -c 'import json,sys; print(json.load(sys.stdin).get("enabled", ""))')"
stream_type="$(printf '%s' "$result_json" | "$python_bin" -c 'import json,sys; print(json.load(sys.stdin).get("stream_type", ""))')"

cat > "$env_file" <<EOF
AZURE_AUDIT_STORAGE_ACCOUNT=$(printf '%q' "$account")
AZURE_AUDIT_STORAGE_CONTAINER=$(printf '%q' "$container")
AZURE_AUDIT_CONTAINER_SAS_URL=$(printf '%q' "$container_sas_url")
AZURE_AUDIT_BLOB_SAS_URL=$(printf '%q' "$blob_service_sas_url")
AZURE_AUDIT_SAS_START=$(printf '%q' "$start")
AZURE_AUDIT_SAS_EXPIRY=$(printf '%q' "$expiry")
AZURE_AUDIT_SAS_KIND=user_delegation
GITHUB_ENTERPRISE_SLUG=$(printf '%q' "$enterprise")
GITHUB_AUDIT_STREAM_ID=$(printf '%q' "$new_stream_id")
EOF
chmod 600 "$env_file"

cat > "$state_file" <<JSON
{
  "enterprise": "$enterprise",
  "storage_account": "$account",
  "container": "$container",
  "stream_id": "$new_stream_id",
  "stream_type": "$stream_type",
  "enabled": "$stream_enabled",
  "action": "$action",
  "sas_kind": "user_delegation",
  "sas_start": "$start",
  "sas_expiry": "$expiry",
  "updated_at": "$(date -u '+%Y-%m-%dT%H:%M:%SZ')"
}
JSON
chmod 600 "$state_file"

printf '%s' "$container_sas_url" | /usr/bin/pbcopy

echo "enterprise=$enterprise"
echo "action=$action"
echo "stream_id=$new_stream_id"
echo "stream_type=$stream_type"
echo "enabled=$stream_enabled"
echo "storage_account=$account"
echo "container=$container"
echo "sas_expiry=$expiry"
echo "container_sas_url_copied_to_clipboard=true"
echo "env_file=$env_file"
echo "state_file=$state_file"
