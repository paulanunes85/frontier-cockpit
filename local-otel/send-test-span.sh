#!/usr/bin/env zsh
set -euo pipefail

base_endpoint="${OTEL_EXPORTER_OTLP_ENDPOINT:-http://localhost:4318}"
trace_endpoint="${base_endpoint%/}/v1/traces"

python3 <<'PY' | curl -fsS -X POST "$trace_endpoint" -H 'Content-Type: application/json' --data-binary @- >/dev/null
import json
import os
import secrets
import time

resource_attributes = [
    {"key": "service.name", "value": {"stringValue": "copilot-otel-local-test"}},
    {"key": "service.version", "value": {"stringValue": "1.0.0"}},
]

for item in os.environ.get("OTEL_RESOURCE_ATTRIBUTES", "").split(","):
    if not item or "=" not in item:
        continue
    key, value = item.split("=", 1)
    if key and value:
        resource_attributes.append({"key": key, "value": {"stringValue": value}})

start_time = time.time_ns()
end_time = start_time + 25_000_000
payload = {
    "resourceSpans": [
        {
            "resource": {"attributes": resource_attributes},
            "scopeSpans": [
                {
                    "scope": {"name": "copilot-otel-local-kit"},
                    "spans": [
                        {
                            "traceId": secrets.token_hex(16),
                            "spanId": secrets.token_hex(8),
                            "name": "local_validation_span",
                            "kind": 1,
                            "startTimeUnixNano": str(start_time),
                            "endTimeUnixNano": str(end_time),
                            "attributes": [
                                {"key": "validation.source", "value": {"stringValue": "send-test-span.sh"}},
                                {"key": "github.copilot.validation", "value": {"boolValue": True}}
                            ],
                            "status": {"code": 1}
                        }
                    ]
                }
            ]
        }
    ]
}
print(json.dumps(payload, separators=(",", ":")))
PY

print "Sent test span to $trace_endpoint with service.name=copilot-otel-local-test"
