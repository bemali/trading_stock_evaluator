"""Configuration helpers that read secrets from `.env`."""

from dataclasses import dataclass
from pathlib import Path
import os
from typing import Optional

from dotenv import load_dotenv

BASE_DIR = Path(__file__).resolve().parent
DOTENV_PATH = BASE_DIR.parent / ".env"


def _coerce_float(value: Optional[str], default: float) -> float:
    if value is None:
        return default
    try:
        return float(value)
    except ValueError:
        return default


def _coerce_int(value: Optional[str], default: int) -> int:
    if value is None:
        return default
    try:
        return int(value)
    except ValueError:
        return default


@dataclass
class Settings:
    postgres_host: str
    postgres_port: int
    postgres_db: str
    postgres_user: str
    postgres_password: str
    yahoo_api_key: str
    yahoo_api_secret: str
    app_env: str
    log_level: str
    request_rate_limit: int
    news_weight: float
    price_weight: float

    @property
    def postgres_url(self) -> str:
        return (
            f"postgresql://{self.postgres_user}:{self.postgres_password}"
            f"@{self.postgres_host}:{self.postgres_port}/{self.postgres_db}"
        )


def load_settings() -> Settings:
    if DOTENV_PATH.exists():
        load_dotenv(DOTENV_PATH)

    return Settings(
        postgres_host=os.getenv("POSTGRES_HOST", "localhost"),
        postgres_port=_coerce_int(os.getenv("POSTGRES_PORT"), 5432),
        postgres_db=os.getenv("POSTGRES_DB", "stock_evaluator"),
        postgres_user=os.getenv("POSTGRES_USER", "postgres"),
        postgres_password=os.getenv("POSTGRES_PASSWORD", "postgres"),
        yahoo_api_key=os.getenv("YAHOO_API_KEY", ""),
        yahoo_api_secret=os.getenv("YAHOO_API_SECRET", ""),
        app_env=os.getenv("APP_ENV", "development"),
        log_level=os.getenv("LOG_LEVEL", "info"),
        request_rate_limit=_coerce_int(os.getenv("REQUEST_RATE_LIMIT"), 50),
        news_weight=_coerce_float(os.getenv("NEWS_WEIGHT"), 1.0),
        price_weight=_coerce_float(os.getenv("PRICE_WEIGHT"), 1.0),
    )
