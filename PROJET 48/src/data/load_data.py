"""Data loading module for financial data."""

import logging
from datetime import datetime, timedelta
from pathlib import Path
from typing import List, Optional, Union

import pandas as pd
import yfinance as yf

from ..utils.config import Config

# Configure logging
logging.basicConfig(
    level=getattr(logging, Config.LOG_LEVEL),
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
)
logger = logging.getLogger(__name__)


class DataLoader:
    """Load financial data from various sources."""

    def __init__(self, cache_dir: Optional[Path] = None):
        """Initialize the DataLoader.

        Args:
            cache_dir: Directory to cache downloaded data. Defaults to Config.CACHE_DIR.
        """
        self.cache_dir = Path(cache_dir) if cache_dir else Config.CACHE_DIR
        self.cache_dir.mkdir(parents=True, exist_ok=True)

    def load_yahoo_data(
        self,
        ticker: str,
        start_date: Optional[str] = None,
        end_date: Optional[str] = None,
        period: str = "5y",
        use_cache: bool = True,
    ) -> pd.DataFrame:
        """Load stock data from Yahoo Finance.

        Args:
            ticker: Stock ticker symbol (e.g., 'AAPL', 'MSFT').
            start_date: Start date in 'YYYY-MM-DD' format.
            end_date: End date in 'YYYY-MM-DD' format.
            period: Time period if start/end dates not specified (e.g., '1y', '5y', 'max').
            use_cache: Whether to use cached data if available.

        Returns:
            DataFrame with OHLCV data.
        """
        cache_file = self.cache_dir / f"{ticker}_{period}.parquet"

        # Check cache
        if use_cache and cache_file.exists():
            logger.info(f"Loading cached data for {ticker}")
            return pd.read_parquet(cache_file)

        # Download data
        logger.info(f"Downloading data for {ticker} from Yahoo Finance")
        try:
            if start_date and end_date:
                data = yf.download(ticker, start=start_date, end=end_date, progress=False)
            else:
                data = yf.download(ticker, period=period, progress=False)

            if data.empty:
                logger.warning(f"No data found for ticker {ticker}")
                return pd.DataFrame()

            # Flatten multi-index columns if present
            if isinstance(data.columns, pd.MultiIndex):
                data.columns = data.columns.get_level_values(0)

            # Cache the data
            data.to_parquet(cache_file)
            logger.info(f"Data cached to {cache_file}")

            return data

        except Exception as e:
            logger.error(f"Error loading data for {ticker}: {e}")
            return pd.DataFrame()

    def load_multiple_tickers(
        self,
        tickers: List[str],
        start_date: Optional[str] = None,
        end_date: Optional[str] = None,
        period: str = "5y",
    ) -> dict[str, pd.DataFrame]:
        """Load data for multiple tickers.

        Args:
            tickers: List of ticker symbols.
            start_date: Start date in 'YYYY-MM-DD' format.
            end_date: End date in 'YYYY-MM-DD' format.
            period: Time period if start/end dates not specified.

        Returns:
            Dictionary mapping tickers to their DataFrames.
        """
        data_dict = {}
        for ticker in tickers:
            data = self.load_yahoo_data(ticker, start_date, end_date, period)
            if not data.empty:
                data_dict[ticker] = data
        return data_dict

    def load_from_csv(
        self, file_path: Union[str, Path], parse_dates: bool = True
    ) -> pd.DataFrame:
        """Load data from a CSV file.

        Args:
            file_path: Path to the CSV file.
            parse_dates: Whether to parse date columns.

        Returns:
            DataFrame with the loaded data.
        """
        file_path = Path(file_path)
        if not file_path.exists():
            logger.error(f"File not found: {file_path}")
            return pd.DataFrame()

        logger.info(f"Loading data from {file_path}")
        try:
            if parse_dates:
                df = pd.read_csv(file_path, parse_dates=["Date"], index_col="Date")
            else:
                df = pd.read_csv(file_path)
            return df
        except Exception as e:
            logger.error(f"Error loading CSV file: {e}")
            return pd.DataFrame()

    def get_stock_info(self, ticker: str) -> dict:
        """Get basic stock information.

        Args:
            ticker: Stock ticker symbol.

        Returns:
            Dictionary with stock information.
        """
        try:
            stock = yf.Ticker(ticker)
            info = stock.info
            return {
                "ticker": ticker,
                "name": info.get("longName", ""),
                "sector": info.get("sector", ""),
                "industry": info.get("industry", ""),
                "market_cap": info.get("marketCap", 0),
                "pe_ratio": info.get("trailingPE", None),
                "pb_ratio": info.get("priceToBook", None),
                "roe": info.get("returnOnEquity", None),
                "roa": info.get("returnOnAssets", None),
                "debt_to_equity": info.get("debtToEquity", None),
                "current_ratio": info.get("currentRatio", None),
                "dividend_yield": info.get("dividendYield", None),
                "beta": info.get("beta", None),
            }
        except Exception as e:
            logger.error(f"Error getting stock info for {ticker}: {e}")
            return {}

    def get_snp500_tickers(self) -> List[str]:
        """Get a list of S&P 500 tickers.

        Returns:
            List of ticker symbols.
        """
        # Common S&P 500 tickers (subset for demonstration)
        tickers = [
            "AAPL",
            "MSFT",
            "GOOGL",
            "AMZN",
            "NVDA",
            "META",
            "TSLA",
            "BRK.B",
            "JPM",
            "V",
            "JNJ",
            "WMT",
            "PG",
            "MA",
            "HD",
            "UNH",
            "BAC",
            "XOM",
            "PFE",
            "CSCO",
        ]
        return tickers

    def clear_cache(self, ticker: Optional[str] = None) -> None:
        """Clear cached data.

        Args:
            ticker: Specific ticker to clear. If None, clears all cache.
        """
        if ticker:
            cache_files = list(self.cache_dir.glob(f"{ticker}_*.parquet"))
        else:
            cache_files = list(self.cache_dir.glob("*.parquet"))

        for file in cache_files:
            file.unlink()
            logger.info(f"Deleted cache file: {file}")
