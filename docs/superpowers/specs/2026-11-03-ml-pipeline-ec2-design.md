# ML Pipeline EC2 Design

The existing FastAPI `ml-api` remains the only HTTP boundary for machine-learning work. Its `/analyze` endpoint validates the existing article request, converts it to dictionaries, calls `ML.src.main.analyze_articles`, and returns the pipeline result unchanged. The frontend and n8n contracts do not change.

The Docker image includes the ML source and runtime dependencies. PyTorch uses its CPU build because the EC2 instance has no GPU. Hugging Face model files live in a named Docker volume so service recreation does not download them again. The sentiment classifier is initialized once per process rather than once per article.

Health reports `pipeline_connected: true` after the callable is installed. Unit tests replace the expensive model call with a deterministic function; deployment verification checks Compose state, the public health endpoint, and one real analysis request. Only `ml-api` is rebuilt and restarted, leaving the frontend and n8n containers running.

Failures during analysis return an HTTP server error and appear in `ml-api` container logs. Empty article lists remain rejected by request validation. The existing EC2 resource limit remains in force to protect the rest of the stack.
