"""Ingestion layer for news and price snapshots."""

from datetime import datetime, timedelta
from typing import Dict, List, Sequence

from httpx import Client

from src.config import Settings


def fetch_news_snapshot(ticker: str, settings: Settings) -> List[Dict]:
    """
    Placeholder for the logic that pulls the daily news snapshot for a ticker.
    Later this will query Postgres, but for now it returns an empty list so the
    pipeline can be wired end-to-end.
    """
    # TODO: replace with actual Postgres query using `settings.postgres_url`
    return []


def fetch_historical_prices(ticker: str, settings: Settings, lookback_days: int = 30) -> List[Dict]:
    """
    Placeholder for Yahoo Finance ingestion.
    Returns a list of dicts with `date`, `close`, `volume`.
    """
    end_date = datetime.utcnow().date()
    start_date = end_date - timedelta(days=lookback_days)
    return [
        {
            "date": (start_date + timedelta(days=i)).isoformat(),
            "close": 1.0,
            "volume": 1_000,
        }
        for i in range(lookback_days + 1)
    ]
