"""Feature engineering utilities for the regression model."""

from statistics import mean
from typing import Dict, List, Sequence

from src.config import Settings


def compute_moving_average(prices: Sequence[Dict], window: int) -> float:
    if len(prices) < window:
        return mean(price["close"] for price in prices) if prices else 0.0
    return mean(price["close"] for price in prices[-window:])


def compute_trend(prices: Sequence[Dict], lookback: int = 7) -> float:
    if len(prices) < 2:
        return 0.0
    lookback = min(len(prices), lookback)
    window = prices[-lookback:]
    start = window[0]["close"]
    end = window[-1]["close"]
    if start == 0:
        return 0.0
    return (end - start) / start


def build_feature_vector(prices: List[Dict], news: List[Dict], settings: Settings) -> Dict[str, float]:
    close_prices = [p["close"] for p in prices]
    if not close_prices:
        close_prices = [0.0]

    feature_vector = {
        "trend": compute_trend(prices),
        "last_close": close_prices[-1],
        "volume": prices[-1].get("volume", 0) if prices else 0,
        "ma_3": compute_moving_average(prices, 3),
        "ma_7": compute_moving_average(prices, 7),
        "ma_30": compute_moving_average(prices, 30),
    }

    if news:
        latest_event = news[-1]
        sentiment = latest_event.get("primary_entity", {}).get("sentiment", {})
        catalyst = latest_event.get("primary_entity", {}).get("catalyst", {})
        feature_vector.update(
            {
                "sentiment_score": sentiment.get("score", 0.0) * settings.news_weight,
                "sentiment_intensity": len(str(sentiment.get("intensity", ""))),
                "catalyst_surprise": catalyst.get("surprise_factor", 0.0) * settings.news_weight,
                "ai_confidence": latest_event.get("ai_confidence_metrics", {}).get("source_reliability", 0.0),
            }
        )
    else:
        feature_vector.update(
            {
                "sentiment_score": 0.0,
                "sentiment_intensity": 0.0,
                "catalyst_surprise": 0.0,
                "ai_confidence": 0.0,
            }
        )

    return feature_vector
