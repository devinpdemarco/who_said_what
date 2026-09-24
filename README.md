# Who Said What

A multi-source news comparison project. This repository contains the EC2 deployment foundation.

## Current deployment

- n8n editor: https://whosaidwhat-n8n.duckdns.org (individual n8n account required).
- Caddy provides HTTPS and proxies requests to n8n; host port 5678 stays loopback-only.
- Persistent n8n and certificate volumes, resource limits, health checks and bounded logs.
- Frontend, data pipeline and ML integration remain separate work.

See [deployment instructions](docs/deployment.md). Never commit `.env`, private keys or workflow credentials.
