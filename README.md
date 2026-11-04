# Who Said What

A multi-source news comparison project. This repository contains the EC2 deployment foundation.

## Current deployment

- Frontend application: https://whosaidwhat.duckdns.org after its DuckDNS record is created and the updated stack is deployed.
- n8n editor: https://whosaidwhat-n8n.duckdns.org (individual n8n account required).
- Caddy provides HTTPS and routes the application and n8n hostnames to separate containers; host port 5678 stays loopback-only.
- An internal ML API container provides a stable integration boundary at `/api/ml/`.
- Persistent n8n and certificate volumes, resource limits, health checks and bounded logs.
- The frontend runs as a production Vite build served by an unprivileged nginx container. Its search still uses mock data until the n8n API contract is connected.
- The real ML pipeline remains separate integration work.

See [deployment instructions](docs/deployment.md). Never commit `.env`, private keys or workflow credentials.
