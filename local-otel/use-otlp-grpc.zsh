# Source this file only for apps or SDKs that require OTLP/gRPC.
# GitHub Copilot Chat should stay on the default OTLP/HTTP configuration.

export OTEL_EXPORTER_OTLP_ENDPOINT="http://localhost:4317"
export OTEL_EXPORTER_OTLP_PROTOCOL="grpc"
unset OTEL_EXPORTER_OTLP_TRACES_ENDPOINT
unset OTEL_EXPORTER_OTLP_METRICS_ENDPOINT
unset OTEL_EXPORTER_OTLP_LOGS_ENDPOINT
unset OTEL_EXPORTER_OTLP_TRACES_PROTOCOL
unset OTEL_EXPORTER_OTLP_METRICS_PROTOCOL
unset OTEL_EXPORTER_OTLP_LOGS_PROTOCOL

print "Using OTLP/gRPC for this shell: http://localhost:4317"
