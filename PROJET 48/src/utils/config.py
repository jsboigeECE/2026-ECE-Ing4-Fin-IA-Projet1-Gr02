"""Configuration module for the XAI Investment project."""

import os
from pathlib import Path
from typing import List

from dotenv import load_dotenv  # python-dotenv package

# Load environment variables
load_dotenv()


class Config:
    """Configuration class for the project."""

    # Base paths
    BASE_DIR = Path(__file__).parent.parent.parent
    DATA_DIR = BASE_DIR / "data"
    RAW_DATA_DIR = DATA_DIR / "raw"
    PROCESSED_DATA_DIR = DATA_DIR / "processed"
    CACHE_DIR = DATA_DIR / "cache"
    MODELS_DIR = BASE_DIR / "models" / "saved"
    LOGS_DIR = BASE_DIR / "logs"

    # API Keys
    YAHOO_FINANCE_API_KEY = os.getenv("YAHOO_FINANCE_API_KEY", "")
    ALPHA_VANTAGE_API_KEY = os.getenv("ALPHA_VANTAGE_API_KEY", "")
    OPENAI_API_KEY = os.getenv("OPENAI_API_KEY", "")

    # Data Configuration
    DATA_CACHE_DIR = os.getenv("DATA_CACHE_DIR", str(CACHE_DIR))
    DATA_UPDATE_INTERVAL = os.getenv("DATA_UPDATE_INTERVAL", "1d")

    # Model Configuration
    MODEL_TYPE = os.getenv("MODEL_TYPE", "xgboost")
    MODEL_PATH = os.getenv("MODEL_PATH", str(MODELS_DIR))
    RANDOM_SEED = int(os.getenv("RANDOM_SEED", "42"))

    # XAI Configuration
    SHAP_BACKGROUND_SIZE = int(os.getenv("SHAP_BACKGROUND_SIZE", "100"))
    LIME_NUM_SAMPLES = int(os.getenv("LIME_NUM_SAMPLES", "5000"))
    COUNTERFACTUAL_NUM_SAMPLES = int(os.getenv("COUNTERFACTUAL_NUM_SAMPLES", "100"))

    # Streamlit Configuration
    STREAMLIT_PORT = int(os.getenv("STREAMLIT_PORT", "8501"))
    STREAMLIT_HOST = os.getenv("STREAMLIT_HOST", "localhost")

    # Logging
    LOG_LEVEL = os.getenv("LOG_LEVEL", "INFO")
    LOG_FILE = os.getenv("LOG_FILE", str(LOGS_DIR / "app.log"))

    # Financial features to compute
    FINANCIAL_FEATURES: List[str] = [
        # Price-based features
        "close",
        "open",
        "high",
        "low",
        "volume",
        # Technical indicators
        "rsi",
        "macd",
        "macd_signal",
        "macd_hist",
        "bb_upper",
        "bb_middle",
        "bb_lower",
        "sma_20",
        "sma_50",
        "sma_200",
        "ema_12",
        "ema_26",
        # Returns
        "daily_return",
        "weekly_return",
        "monthly_return",
        # Volatility
        "volatility_20",
        "volatility_50",
    ]

    # Investment decision classes
    DECISION_CLASSES = ["SELL", "HOLD", "BUY"]

    # Rule-based thresholds
    RULE_THRESHOLDS = {
        "pe_ratio": {"buy": 15, "sell": 30},
        "pb_ratio": {"buy": 1.5, "sell": 3.0},
        "roe": {"buy": 0.15, "sell": 0.05},
        "roa": {"buy": 0.10, "sell": 0.02},
        "debt_to_equity": {"buy": 1.0, "sell": 2.0},
        "current_ratio": {"buy": 2.0, "sell": 1.0},
        "rsi": {"oversold": 30, "overbought": 70},
    }

    @classmethod
    def create_directories(cls) -> None:
        """Create necessary directories if they don't exist."""
        directories = [
            cls.RAW_DATA_DIR,
            cls.PROCESSED_DATA_DIR,
            cls.CACHE_DIR,
            cls.MODELS_DIR,
            cls.LOGS_DIR,
        ]
        for directory in directories:
            directory.mkdir(parents=True, exist_ok=True)


# Create directories on import
Config.create_directories()
