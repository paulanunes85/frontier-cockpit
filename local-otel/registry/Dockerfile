FROM docker.io/library/alpine:3.24

RUN set -eux; \
  for attempt in 1 2 3 4 5; do \
  apk add --no-cache curl python3 zsh && break; \
  [ "${attempt}" -eq 5 ] && exit 1; \
  sleep $((attempt * 5)); \
  done

WORKDIR /app/local-otel

COPY register-model-price.sh \
  register-all-workspaces.sh \
  seed-model-prices.sh \
  ./
COPY registry/registry-loop.zsh /app/registry-loop.zsh

RUN chmod +x \
  /app/registry-loop.zsh \
  /app/local-otel/register-all-workspaces.sh \
  /app/local-otel/register-model-price.sh \
  /app/local-otel/seed-model-prices.sh

ENV FRONTIER_SKIP_ENV_ZSH=true
ENV OTEL_EXPORTER_OTLP_METRICS_ENDPOINT=http://otel-collector:4318/v1/metrics
ENV REGISTRY_REFRESH_SECONDS=300

CMD ["zsh", "/app/registry-loop.zsh"]
