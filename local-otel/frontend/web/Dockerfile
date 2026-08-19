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
COPY tsconfig*.json ./
COPY vite.config.ts ./
COPY index.html ./
COPY public ./public
COPY src ./src
RUN npm run build

FROM docker.io/library/nginx:1.27-alpine

COPY nginx.conf /etc/nginx/conf.d/default.conf
COPY --from=build /app/dist /usr/share/nginx/html

EXPOSE 80
