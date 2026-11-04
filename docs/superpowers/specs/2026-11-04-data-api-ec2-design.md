# Data API EC2 Design

Nidya's existing `process_articles()` and `save_articles()` functions run behind a small internal FastAPI service named `data-api`. n8n sends raw article dictionaries to `POST http://data-api:8001/process`; the service cleans, normalizes, deduplicates, validates, and inserts valid articles into Supabase. It returns the inserted rows, including database-generated IDs, so n8n can pass them directly to the ML API.

The service is available only on the Docker Compose network. Supabase credentials are injected from the EC2 `.env` file and are never sent to the browser or committed to Git. A health endpoint supports Docker monitoring. Unit tests replace the database operation, while the existing Supabase integration test runs only when credentials are explicitly present.
