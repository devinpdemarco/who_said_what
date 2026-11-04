# ML Integration Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Add a deployable ML API boundary to the existing EC2 Compose stack without implementing or guessing Kynnedy's model pipeline.

**Architecture:** A small FastAPI adapter exposes stable health and analysis endpoints in its own Docker container. Compose gives the service explicit resource limits and only exposes it to the internal network; Caddy routes `/api/ml/*` to it. Kynnedy's pipeline can later replace the adapter implementation without changing infrastructure consumers.

**Tech Stack:** Docker Compose, Python 3.12, FastAPI, pytest, Caddy

---

### Task 1: Define and test the ML API contract

**Files:**
- Create: `services/ml-api/app/main.py`
- Create: `services/ml-api/tests/test_api.py`
- Create: `services/ml-api/requirements.txt`

- [x] Write API tests for health, empty requests, and the temporary unavailable response.
- [x] Run pytest and confirm the tests initially fail.
- [x] Implement the minimal FastAPI adapter and request schemas.
- [x] Run pytest and confirm all API tests pass.

### Task 2: Containerize the adapter

**Files:**
- Create: `services/ml-api/Dockerfile`
- Create: `services/ml-api/.dockerignore`
- Modify: `compose.yaml`
- Modify: `.env.example`

- [x] Add a non-root Python container with a Docker health check.
- [x] Add the internal-only `ml-api` Compose service with configurable CPU and memory limits.
- [x] Validate the Compose YAML structure. Full `docker compose config` validation remains blocked because Docker is not installed locally.

### Task 3: Route and document the service

**Files:**
- Modify: `infra/caddy/Caddyfile`
- Modify: `docs/deployment.md`
- Modify: `README.md`

- [x] Route `/api/ml/*` to the ML container while preserving n8n routing.
- [x] Document local verification, the temporary API behavior, and the information required from Kynnedy.
- [x] Build the image and run the automated API tests.
- [x] Commit the completed integration foundation.

### Task 4: Connect and deploy the real pipeline

**Files:**
- Modify: `services/ml-api/app/main.py`
- Create: `services/ml-api/app/pipeline.py`
- Modify: `services/ml-api/tests/test_api.py`
- Modify: `services/ml-api/Dockerfile`
- Create: `services/ml-api/ml-requirements.txt`
- Modify: `compose.yaml`
- Modify: `ML/src/analyze_sentiment.py`
- Create: `ML/tests/test_analyze_sentiment.py`

- [x] Write failing API tests for a connected health response and returned ML results.
- [x] Connect `/analyze` to the callable ML entry point and pass the API tests.
- [x] Write a failing test showing that the sentiment model loads more than once.
- [x] Cache the classifier and pass all ML and API unit tests.
- [x] Package CPU-only ML dependencies and persistent model cache in Compose.
- [x] Build and restart only `ml-api` on EC2.
- [x] Verify public health and one real analysis request.
