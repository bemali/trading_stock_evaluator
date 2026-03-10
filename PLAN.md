# Plan for the project
<<<<<<< HEAD
- this project is to provide an estimate for a certain stock with the help of a forecaster model, and market sentiments. 

#### input
- a ticker

#### resources
- news items recorded in a postgres database in cloud, with some research analysis points, indicators along with the ticker
- yahoo finance to extract past records for the ticker

#### output
- a prediction: initially qualitative for the stock based on the stock
- underlying reasoning
- validation based on previous instances (overlayed on the graph perhaps?)

#### deployment
- as an azure container app (backend)
- as an azure webapp (front end)
=======
- Provide explainable stock estimates by combining scikit-learn regression with news and price signals.

#### Input
- `ticker` identifier from external requests

#### Resources
- Daily snapshot of news + sentiment + catalyst schema stored in cloud Postgres (`event_id`, sentimen/catalyst details, market network effects, macro indicators, AI confidence).
- Yahoo Finance history (prices, volumes) normalized to daily cadence.
- Configurable `.env` for Postgres, Yahoo credentials, and feature weights.

#### Feature strategy
- Price-driven: last recorded point, moving averages for 3, 7, 30 days, and trend (slope over last window).
- News-driven: sentiment score/intensity, catalyst surprise factor, competitor impact, macro indicators, and AI confidence metrics; label blocks to explain contributions.

#### Output
- Qualitative prediction elevated by the scikit-learn regression result.
- Reasoning text referencing dominant features (moving averages, sentiment, catalysts).
- Validation overlay by comparing with recent actuals (no long-term forecast retention).

#### API surface
- `POST /predict`: ticker → prediction + reasoning + validation overlay data.
- `GET /history/{ticker}`: recent actuals + feature context to explain past performance.
- Health/readiness endpoints; security/rate limits set via `.env`.

#### Deployment
- Containerized backend (Azure Container App) reading `.env` secrets for Postgres/Yahoo.
- Logging/metrics for production observability.
- Front-end deployed as Azure Web App, consuming the backend APIs; backend keeps Web App agnostic to data sources.
>>>>>>> 2ea733c (Add initial project structure with FastAPI backend and essential components)
