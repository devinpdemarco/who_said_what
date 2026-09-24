# EC2 deployment

Owner: Xiaopei. This is the team's development environment.

## Architecture and access

Ubuntu 24.04 on EC2 runs Docker Compose: Caddy serves HTTPS and forwards to n8n over the Compose network. The n8n host binding is `127.0.0.1:5678`; do not expose this port publicly. Named volumes retain n8n data and Caddy certificates. The old `infra/nginx` files are unused historical bootstrap assets.

Open https://whosaidwhat-n8n.duckdns.org and sign in with your n8n account. Devin can work in the editor without SSH or AWS console access. Workflow changes are stored in the n8n database, independently of Git. Export workflows for version control after removing sensitive content; pulling JSON files does not import them automatically.

The instance is `Who_Said_What` (`i-0b8b92301be98a6dc`) in Ohio. It has 4 GiB RAM, 30 GiB gp3 storage and 4 GiB swap. The last verified public IP was `3.137.137.57` on September 23, 2026. This is not an Elastic IP: after stop/start, confirm the new IP and update DuckDNS manually. No automatic DNS updater is configured.

SSH from an allowed network:

```sh
ssh -i ~/Downloads/who-said-what-xiaopei.pem ubuntu@CURRENT_PUBLIC_IP
```

AWS IAM access does not itself grant SSH or n8n login access.

## Configuration

The server checkout is `/home/ubuntu/who_said_what`. The shared integration branch is `dev`.

For a fresh deployment only, create `.env` from `.env.example`, generate a key with `openssl rand -hex 32`, and set `N8N_ENCRYPTION_KEY`. Restrict `.env` to mode 600. On an existing deployment, retain its original key: saved credentials depend on it. Never commit this file.

Before a fresh deployment, point DuckDNS to the instance and allow inbound TCP 80 and 443. Keep SSH 22 limited to approved source IPs. Complete owner setup before sharing a newly initialized n8n instance.

```sh
sudo docker compose config --quiet
sudo docker compose up -d --wait --wait-timeout 180
sudo docker compose ps
curl -f https://whosaidwhat-n8n.duckdns.org/healthz
```

The n8n image is digest-pinned; Caddy currently uses `caddy:2-alpine`. Pulling Caddy can update its version. Back up and schedule service changes with teammates before upgrades.

## Routine updates

First check `git status --short --branch`. Preserve local edits before switching or pulling. Merge reviewed team changes into `dev`; a branch switch does not combine different teammates' branches.

With a clean checkout and deployment-ready changes:

```sh
git switch dev
git pull --ff-only origin dev
sudo docker compose config --quiet
sudo docker compose up -d --build --wait --wait-timeout 180
sudo docker compose ps
```

This can recreate changed services: coordinate with teammates using n8n. There is no automatic deployment pipeline. Frontend and ML need their Dockerfiles and Compose integration before these commands can deploy them.

For read-only checks:

```sh
sudo docker compose ps
sudo docker compose logs --tail=100
sudo docker stats --no-stream
```

Docker starts at boot; services use `restart: unless-stopped`. Closing SSH does not stop the instance. Stop EC2 only when teammates do not need the editor or running workflows. Do not use `docker compose down -v`: it deletes named volumes, including workflows and credentials.

## Backups and school restrictions

A pre-HTTPS backup was verified at `/home/ubuntu/wsw-backups/20260923-052412`: Compose configuration, `.env`, and n8n data copied while n8n was stopped. It predates Devin's subsequent work. It is on the same disk, so it is not disaster recovery. Automated off-host backups and restore testing remain to be implemented. Keep each database backup together with its matching encryption key, privately.

Required school resource tag: `Group=Who_Said_What`. Only manage this team's resources. The TA controls permissions and spending visibility. Requests to modify security-group rules may require `ec2:ModifySecurityGroupRules`; changing CPU credits was denied for missing `ec2:ModifyInstanceCreditSpecification`. CPU credit mode was last observed as Unlimited. Coordinate with the TA before heavy tests. EBS charges continue while EC2 is stopped.

## Remaining integrations

- Devin: n8n workflows; Nidya: Supabase schema and connection requirements.
- Ben: frontend runtime and build requirements; Kynnedy: ML runtime and interface.
- Xiaopei: integrate services, add off-host backups, deployment automation and measured resource/load tests.

## Verification on September 23, 2026

Compose configuration and Caddy validation passed. Both running services were healthy; public HTTPS returned 200 and `/healthz` returned `{"status":"ok"}`. Saving and merging this configuration does not require restarting containers or changing the n8n database.
