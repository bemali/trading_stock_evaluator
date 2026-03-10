"""FastAPI application that wires ingestion, features, and model services."""

from fastapi import FastAPI

from src.api.schemas import HistoryResponse, PredictionRequest, PredictionResponse
from src.config import load_settings
from src.services.features import build_feature_vector
from src.services.ingestion import fetch_historical_prices, fetch_news_snapshot
from src.services.model import ModelWrapper


def create_app() -> FastAPI:
    settings = load_settings()
    model = ModelWrapper()

    app = FastAPI(
        title="Trading Stock Evaluator",
        description="Explainable regression forecasts powered by daily news + price signals.",
        version="0.1.0",
    )

    @app.get("/healthz", include_in_schema=False)
    def healthz() -> dict:
        return {"status": "ok", "env": settings.app_env}

    @app.post("/predict", response_model=PredictionResponse)
    def predict(payload: PredictionRequest) -> PredictionResponse:
        news = fetch_news_snapshot(payload.ticker, settings)
        prices = fetch_historical_prices(payload.ticker, settings, payload.lookback_days)
        features = build_feature_vector(prices, news, settings)
        prediction = model.predict(features)
        reasoning = model.explain(features)
        validation = [
            f"Last close: {prices[-1]['close'] if prices else 0.0:.2f}",
            f"Latest 3d MA: {features.get('ma_3', 0.0):.2f}",
        ]
        return PredictionResponse(
            ticker=payload.ticker,
            prediction=prediction,
            reasoning=reasoning,
            features=features,
            validation_notes=validation,
        )

    @app.get("/history/{ticker}", response_model=HistoryResponse)
    def history(ticker: str) -> HistoryResponse:
        lookback = 30
        news = fetch_news_snapshot(ticker, settings)
        prices = fetch_historical_prices(ticker, settings, lookback)
        features = build_feature_vector(prices, news, settings)
        serialized = [
            {"date": p["date"], "close": p["close"]}
            for p in prices
        ]
        return HistoryResponse(
            ticker=ticker,
            history=serialized,
            feature_context=features,
        )

    return app
