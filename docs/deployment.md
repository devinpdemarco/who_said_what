# EC2 deployment

Owner: Xiaopei. This is the team's development environment.

## Architecture and access

Ubuntu 24.04 on EC2 runs Docker Compose. Caddy serves HTTPS for two hostnames: `whosaidwhat.duckdns.org` routes to the frontend container, while `whosaidwhat-n8n.duckdns.org` routes to n8n and sends `/api/ml/*` to the internal ML API. The n8n host binding is `127.0.0.1:5678`; do not expose this port publicly. The frontend and ML API have no host ports. Named volumes retain n8n data and Caddy certificates. The old `infra/nginx` files are unused historical bootstrap assets.

Open https://whosaidwhat-n8n.duckdns.org and sign in with your n8n account. Devin can work in the editor without SSH or AWS console access. Workflow changes are stored in the n8n database, independently of Git. Export workflows for version control after removing sensitive content; pulling JSON files does not import them automatically.

Open https://whosaidwhat.duckdns.org for the frontend after the DuckDNS record points to the EC2 public IP. The frontend currently displays mock search results until its request contract is connected to Devin's n8n webhook.

The instance is `Who_Said_What` (`i-0b8b92301be98a6dc`) in Ohio. It has 4 GiB RAM, 30 GiB gp3 storage and 4 GiB swap. The last verified public IP was `3.137.137.57` on September 23, 2026. This is not an Elastic IP: after stop/start, confirm the new IP and update DuckDNS manually. No automatic DNS updater is configured.

SSH from an allowed network:

```sh
ssh -i ~/Downloads/who-said-what-xiaopei.pem ubuntu@CURRENT_PUBLIC_IP
```

AWS IAM access does not itself grant SSH or n8n login access.

## Configuration

The active server checkout is `/home/ubuntu/who_said_what_deploy`. The shared integration branch is `dev`. The older `/home/ubuntu/who_said_what` checkout is retained because it contains the previous deployment state; do not use it for routine updates.

For a fresh deployment only, create `.env` from `.env.example`, generate a key with `openssl rand -hex 32`, and set `N8N_ENCRYPTION_KEY`. Set `APP_DOMAIN=whosaidwhat.duckdns.org`, or replace it with the frontend hostname you created. Restrict `.env` to mode 600. On an existing deployment, retain its original encryption key: saved credentials depend on it. Never commit this file.

Before deploying the frontend, sign in to DuckDNS, create the `whosaidwhat` subdomain, and point it to the same EC2 public IP used by `whosaidwhat-n8n`. Allow inbound TCP 80 and 443. Keep SSH 22 limited to approved source IPs. If the EC2 public IP changes after a stop/start, update both DuckDNS records before restarting Caddy.

```sh
sudo docker compose config --quiet
sudo docker compose up -d --wait --wait-timeout 180
sudo docker compose ps
curl -f https://whosaidwhat-n8n.duckdns.org/healthz
curl -f https://whosaidwhat.duckdns.org/healthz
```

The ML adapter can be checked through Caddy:

```sh
curl -f https://whosaidwhat-n8n.duckdns.org/api/ml/health
```

Until Kynnedy's pipeline is connected, `/api/ml/analyze` intentionally returns
HTTP 503. It does not return mock sentiment or bias values that could be
mistaken for real analysis.

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

This can recreate changed services: coordinate with teammates using n8n. There is no automatic deployment pipeline. The frontend is containerized, but its search still needs Devin's n8n webhook contract. The ML adapter is containerized, but Kynnedy's real pipeline still needs to be integrated.

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
- Ben: replace frontend mock search with the agreed n8n API request and response.
- Kynnedy: provide the pipeline's Python entry point, input/output types, dependency versions and required model artifacts. The infrastructure contract currently accepts a non-empty list of articles containing `title`, `url`, `source` and `cleaned_text`.
- Xiaopei: integrate services, add off-host backups, deployment automation and measured resource/load tests.

## Verification history

On September 23, 2026, Compose configuration and Caddy validation passed. Both running services were healthy; public HTTPS returned 200 and `/healthz` returned `{"status":"ok"}`.

On November 3, 2026, the frontend lint and production build passed locally. The frontend and ML adapter images then built successfully on EC2, all four Compose services reported healthy, Caddy obtained HTTPS for `whosaidwhat.duckdns.org`, the frontend health endpoint returned `ok`, the n8n health endpoint returned `{"status":"ok"}`, and the ML health endpoint reported that the adapter was running with the real pipeline not yet connected.

Later on November 3, 2026, Kynnedy's callable pipeline was connected to `/api/ml/analyze` and deployed as a CPU-only container. A real request returned sentiment results for 20 articles and 7 clusters; after the final container rebuild, an 8-article request returned 8 sentiment results and 7 clusters in 31.3 seconds. All four services remained healthy. Hugging Face model files are retained in the `ml_model_cache` volume.
