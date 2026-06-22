#!/usr/bin/env zsh
set -euo pipefail

# Inspect content-capture attributes in Tempo traces.
# Default mode lists attribute keys and lengths only. Use --show-content to print raw captured
# content in trusted local demos. Raw content may include prompts, code, file contents, tool
# arguments, and tool results.

show_content=0
trace_id=""

for arg in "$@"; do
  case "$arg" in
    --show-content) show_content=1 ;;
    *) trace_id="$arg" ;;
  esac
done

if [[ -z "$trace_id" ]]; then
  trace_id="$(curl -fsS 'http://localhost:3200/api/search?limit=1' | python3 -c 'import json,sys; d=json.load(sys.stdin); print(d["traces"][0]["traceID"] if d.get("traces") else "")')"
fi

if [[ -z "$trace_id" ]]; then
  print -u2 "No traces found in Tempo."
  exit 1
fi

tmp_file="$(mktemp)"
trap 'rm -f "$tmp_file"' EXIT
curl -fsS "http://localhost:3200/api/traces/$trace_id" > "$tmp_file"

python3 - "$show_content" "$tmp_file" "$trace_id" <<'PY'
import base64
import json
import sys

show_content = sys.argv[1] == "1"
with open(sys.argv[2], "r", encoding="utf-8") as handle:
    data = json.load(handle)
selected_trace_id = sys.argv[3]
interesting = (
    "gen_ai.input.messages",
    "gen_ai.output.messages",
    "gen_ai.system_instructions",
    "gen_ai.tool.definitions",
    "gen_ai.tool.call.arguments",
    "gen_ai.tool.call.result",
    "github.copilot.tool.parameters.command",
    "github.copilot.tool.parameters.file_path",
    "copilot_chat.user_request",
)

def value_to_python(value):
    if "stringValue" in value:
        return value["stringValue"]
    if "intValue" in value:
        return value["intValue"]
    if "doubleValue" in value:
        return value["doubleValue"]
    if "boolValue" in value:
        return value["boolValue"]
    if "arrayValue" in value:
        return value["arrayValue"]
    if "kvlistValue" in value:
        return value["kvlistValue"]
    return value

print(f"trace_id={data.get('traceID') or selected_trace_id}")
found = False
for batch in data.get("batches", []):
    for scope in batch.get("scopeSpans", []):
        for span in scope.get("spans", []):
            span_id = span.get("spanId", "")
            if span_id:
                try:
                    span_id = base64.b64decode(span_id).hex()
                except Exception:
                    pass
            span_name = span.get("name", "")
            for attr in span.get("attributes", []):
                key = attr.get("key", "")
                if key not in interesting:
                    continue
                found = True
                raw = value_to_python(attr.get("value", {}))
                text = json.dumps(raw, ensure_ascii=False) if not isinstance(raw, str) else raw
                print(f"\nspan={span_name} span_id={span_id}")
                print(f"attribute={key}")
                print(f"chars={len(text)}")
                if show_content:
                    print("--- content start ---")
                    print(text)
                    print("--- content end ---")
                else:
                    print("content_hidden=true")

if not found:
    print("No content-capture attributes found in this trace. Confirm captureContent is enabled and inspect a newer copilot-chat trace.")
elif not show_content:
    print("\nRaw content hidden. Re-run with --show-content only in a trusted local environment.")
PY
