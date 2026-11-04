# Frontend Deployment Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Merge the current frontend into the deployment stack and serve its production build from a separate DuckDNS hostname.

**Architecture:** Build the Vite application in a Node build stage and serve the generated static files from an unprivileged nginx container. Caddy keeps the existing n8n hostname unchanged and routes the new application hostname to the frontend container.

**Tech Stack:** React, Vite, Docker Compose, nginx, Caddy, DuckDNS

---

### Task 1: Merge and verify the frontend

- [x] Merge `origin/feature/frontend-ui` into `ml-integration`.
- [x] Install locked dependencies, run lint, and build the production bundle.

### Task 2: Containerize the production frontend

- [x] Add a multi-stage frontend Dockerfile and nginx SPA configuration.
- [x] Add the internal-only frontend service to `compose.yaml` with health checks and resource limits.
- [x] Validate the frontend configuration and production build.

### Task 3: Route the application hostname

- [x] Add `whosaidwhat.duckdns.org` to Caddy without changing the n8n hostname.
- [x] Update deployment documentation and the environment example.
- [x] Commit and push the integration branch.
- [ ] Fast-forward `dev` to the verified integration commit and push it.
