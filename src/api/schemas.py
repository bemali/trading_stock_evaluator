"""Pydantic schemas for API requests and responses."""

from typing import Dict, List

from pydantic import BaseModel, Field


class PredictionRequest(BaseModel):
    ticker: str = Field(..., min_length=1)
    lookback_days: int = Field(30, ge=7, le=90)


class FeatureSummary(BaseModel):
    feature: str
    value: float


class PredictionResponse(BaseModel):
    ticker: str
    prediction: float
    reasoning: str
    features: Dict[str, float]
    validation_notes: List[str]


class HistoryEntry(BaseModel):
    date: str
    close: float


class HistoryResponse(BaseModel):
    ticker: str
    history: List[HistoryEntry]
    feature_context: Dict[str, float]
