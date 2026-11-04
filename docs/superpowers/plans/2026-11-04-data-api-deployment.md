# Data API Deployment Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Deploy Nidya's data processing and Supabase insertion code as an internal EC2 service callable from n8n.

**Architecture:** A FastAPI `data-api` accepts raw articles, calls the existing processing pipeline, saves valid rows through the existing Supabase client, and returns inserted rows. Docker Compose keeps the service internal and injects credentials from the server environment.

**Tech Stack:** Python 3.12, FastAPI, Supabase Python client, Docker Compose, pytest

---

### Task 1: Import and verify Nidya's pipeline

- [x] Import only data-pipeline files without replacing deployed frontend code.
- [x] Run existing processing tests and confirm 12 pass.
- [x] Refactor Supabase client creation to occur only when saving.
- [x] Add and pass an injected-client unit test.

### Task 2: Add the internal data API

- [x] Write failing tests for health, processing/saving, and empty input.
- [x] Implement `/health` and `/process`.
- [x] Add a non-root Docker image and Compose service.
- [x] Run all local data-api and pipeline tests.

### Task 3: Deploy and verify

- [x] Add `SUPABASE_URL` and `SUPABASE_KEY` to the EC2 `.env` file.
- [x] Build and start only `data-api` without restarting existing services.
- [x] Send a real article through the service and confirm the returned Supabase row.
- [x] Confirm all Compose services remain healthy.
