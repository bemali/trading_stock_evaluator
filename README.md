# Trading Stock Evaluator

Backend skeleton for the scikit-learn regression service described in `PLAN.md`.

## Structure

- `main.py` launches the FastAPI/uvicorn server via `src/api/app.py`.
- `src/config.py` reads `.env` for database, Yahoo, and feature controls.
- `src/services` hosts the ingestion, feature engineering, and model stubs.
- `src/api` defines request/response schemas and the HTTP surface for predictions/history.
- `.env` stores placeholders for Postgres/Yahoo credentials and app tuning flags.

## Getting started

1. Copy `.env` and fill in the Postgres/Yahoo credentials.
2. Install dependencies: `pip install .`

## Running

- Launch the server locally: `python main.py` (starts uvicorn on `localhost:8000`).
- `POST /predict` accepts a `ticker` + optional lookback days and returns a prediction skeleton.
- `GET /history/{ticker}` surfaces the normalized price history plus feature context.

## Next steps

- Wire ingestion to the nightly Postgres snapshot and Yahoo Finance API.
- Replace the dummy model with a trained scikit-learn regressor and record feature importance.
- Implement validation overlays and historical comparisons before deploying to Azure Container Apps.
