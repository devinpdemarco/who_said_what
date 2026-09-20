# EC2 deployment foundation

Owner: Xiaopei. This is a development environment, not the completed news application.

## Architecture

An existing Ubuntu 24.04 EC2 instance runs Docker Compose. Nginx serves a public placeholder on port 80. n8n listens on host loopback port 5678 only; no public proxy route leads to its editor or webhooks. Supabase will be hosted externally and connected in a later sprint. ML and the actual frontend will be integrated after agreeing on their interfaces.

The target has 4 GiB RAM, 30 GiB gp3 storage and 4 GiB swap. Container limits reduce resource contention; a single EC2 host is still a shared failure point. Swap is not a substitute for RAM. No performance target is claimed at this stage.

## First deployment

Create `.env` from `.env.example`, generate a key with `openssl rand -hex 32`, and place it in `N8N_ENCRYPTION_KEY`. Restrict `.env` permissions to 600. Keep this key stable and back it up securely together with n8n data.

```sh
sudo docker compose config --quiet
sudo docker compose up -d --wait --wait-timeout 180
curl -f http://localhost/healthz
curl -f http://localhost:5678/healthz
sudo docker compose ps
```

Image references are pinned by digest. Upgrade intentionally, after backing up data and verifying compatibility.

## Access n8n from your Mac

Replace `PUBLIC_DNS` with the instance's current public DNS:

```sh
ssh -i ~/Downloads/who-said-what-xiaopei.pem -N -L 127.0.0.1:5678:127.0.0.1:5678 ubuntu@PUBLIC_DNS
```

Leave that terminal open and visit http://localhost:5678 in Chrome. Complete the n8n owner account setup yourself. No workflows or external credentials are preconfigured. Browser cookies retain n8n's secure default; use localhost in Chrome for this development tunnel. Public HTTPS and external webhooks require a separate configuration phase.

## Operations

Run commands from `/home/ubuntu/who_said_what` on EC2.

```sh
sudo docker compose ps
sudo docker compose logs --tail=100
sudo docker stats --no-stream
sudo docker compose restart
sudo docker compose stop
sudo docker compose up -d --wait
```

Docker starts at boot; services restart unless explicitly stopped. `docker compose down` removes containers but retains named volumes. Do not use `down -v`: it deletes n8n's database and saved workflows.

Back up before changing images: stop n8n, copy its named volume with a trusted container or host administrator tools, save the backup outside this EC2 disk, retain the matching encryption key securely, and restart n8n. A volume alone is persistence, not a backup. Automated off-host backups are not configured yet.

## AWS and cost

Required school tag: `Group=Who_Said_What`, including instances and volumes. Only manage this team's resources. SSH port 22 is limited to the operator's IP; update it if your network changes. Port 80 serves the development page. Do not open 5678 publicly.

The school TA tracks spending. Plan within $100; this is not an automatic spending cap. Stop this team's instance when unused; EBS still costs money. An allocated Elastic IP also costs money while stopped. This setup uses the automatically assigned public IP, which can change after stop/start. Confirm the new address before SSH or sharing links. CPU Standard mode can throttle sustained jobs; record the setting during future stress tests. Do not change it silently for benchmarks.

## Next integrations

1. User creates the n8n owner account through the tunnel.
2. Devin supplies workflow exports and Nidya supplies the Supabase schema/connection requirements.
3. Agree with Ben on the actual frontend framework before writing its Dockerfile.
4. Kynnedy supplies the ML runtime and input/output interface; set limits after measuring memory use.
5. Add HTTPS, deployment CI, off-host backups and meaningful end-to-end/load tests before production.

## Verified deployment — 2026-09-20

- EC2 name in the console: `Who_Said_What`; instance ID `i-0b8b92301be98a6dc`, Ohio.
- Public address at deployment: http://18.223.111.54 (auto-assigned; may change).
- Server checkout: `/home/ubuntu/who_said_what`, branch `codex/ec2-bootstrap`.
- Both Compose services passed health checks. Public `/healthz` returned `ok`.
- Restarted n8n, waited for health checks, and verified its SQLite database remained present in the mounted volume. No user workflows exist yet.
- Verified the browser reaches the public landing page and n8n owner setup through an SSH tunnel.
- Added inbound TCP 80 from IPv4 internet to this instance's security group after user confirmation. Existing SSH source restriction and HTTPS rule retained; HTTPS service is not configured.
- CPU credit mode remains **Unlimited**. Changing it to Standard was denied because the school IAM policy lacks `ec2:ModifyInstanceCreditSpecification`. Ask the TA to switch this instance to Standard or grant that action if appropriate. No heavy load test was run.
- n8n owner account setup is left to Xiaopei. No Supabase credentials, production integrations or off-host backup were configured.
