FROM docker.io/library/node:26-alpine AS build

ARG NPM_REGISTRY=https://registry.npmjs.org/

WORKDIR /app
COPY package*.json ./
RUN npm ci \
  --registry="${NPM_REGISTRY}" \
  --fetch-retries=10 \
  --fetch-retry-mintimeout=10000 \
  --fetch-retry-maxtimeout=120000 \
  --fetch-timeout=120000 \
  --no-audit \
  --no-fund
COPY tsconfig.json ./
COPY src ./src
RUN npm run build

FROM docker.io/library/node:26-alpine

ARG NPM_REGISTRY=https://registry.npmjs.org/

WORKDIR /app
ENV NODE_ENV=production
COPY package*.json ./
RUN npm ci \
  --omit=dev \
  --registry="${NPM_REGISTRY}" \
  --fetch-retries=10 \
  --fetch-retry-mintimeout=10000 \
  --fetch-retry-maxtimeout=120000 \
  --fetch-timeout=120000 \
  --no-audit \
  --no-fund
COPY --from=build /app/dist ./dist

EXPOSE 8080
CMD ["node", "dist/server.js"]
