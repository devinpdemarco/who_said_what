# Who Said What

A multi-source news comparison project. This branch contains the initial EC2 deployment foundation, rebuilt from `dev`.

## Current scope

- Public Nginx development landing page and `/healthz` endpoint.
- Private n8n editor accessed through an SSH tunnel.
- Persistent n8n volume, memory/CPU limits, health checks and bounded logs.
- No article ingestion, Supabase connection, frontend application or ML model yet.

See [deployment instructions](docs/deployment.md). Never commit `.env` or SSH private keys.
