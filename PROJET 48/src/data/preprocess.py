"""Data preprocessing module for financial data."""

import logging
from typing import List, Optional, Tuple

import numpy as np
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler

from ..utils.config import Config

# Configure logging
logging.basicConfig(
    level=getattr(logging, Config.LOG_LEVEL),
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
)
logger = logging.getLogger(__name__)


class DataPreprocessor:
    """Preprocess financial data for machine learning."""

    def __init__(self, random_seed: int = Config.RANDOM_SEED):
        """Initialize the DataPreprocessor.

        Args:
            random_seed: Random seed for reproducibility.
        """
        self.random_seed = random_seed
        self.scaler = StandardScaler()
        self.feature_columns: List[str] = []

    def clean_data(self, df: pd.DataFrame) -> pd.DataFrame:
        """Clean the data by handling missing values and duplicates.

        Args:
            df: DataFrame to clean.

        Returns:
            Cleaned DataFrame.
        """
        df = df.copy()

        # Remove duplicate indices
        df = df[~df.index.duplicated(keep="first")]

        # Forward fill missing values
        df = df.fillna(method="ffill")

        # Backward fill remaining missing values
        df = df.fillna(method="bfill")

        # Drop any remaining rows with NaN
        df = df.dropna()

        logger.info(f"Data cleaned. Shape: {df.shape}")
        return df

    def compute_technical_indicators(self, df: pd.DataFrame) -> pd.DataFrame:
        """Compute technical indicators from OHLCV data.

        Args:
            df: DataFrame with OHLCV data.

        Returns:
            DataFrame with added technical indicators.
        """
        df = df.copy()

        # Ensure required columns exist
        required_cols = ["Close", "Open", "High", "Low", "Volume"]
        for col in required_cols:
            if col not in df.columns:
                logger.warning(f"Column {col} not found in DataFrame")
                return df

        # Simple Moving Averages
        df["sma_20"] = df["Close"].rolling(window=20).mean()
        df["sma_50"] = df["Close"].rolling(window=50).mean()
        df["sma_200"] = df["Close"].rolling(window=200).mean()

        # Exponential Moving Averages
        df["ema_12"] = df["Close"].ewm(span=12, adjust=False).mean()
        df["ema_26"] = df["Close"].ewm(span=26, adjust=False).mean()

        # RSI (Relative Strength Index)
        df["rsi"] = self._compute_rsi(df["Close"], window=14)

        # MACD
        macd, macd_signal, macd_hist = self._compute_macd(df["Close"])
        df["macd"] = macd
        df["macd_signal"] = macd_signal
        df["macd_hist"] = macd_hist

        # Bollinger Bands
        bb_upper, bb_middle, bb_lower = self._compute_bollinger_bands(df["Close"])
        df["bb_upper"] = bb_upper
        df["bb_middle"] = bb_middle
        df["bb_lower"] = bb_lower

        # Returns
        df["daily_return"] = df["Close"].pct_change()
        df["weekly_return"] = df["Close"].pct_change(5)
        df["monthly_return"] = df["Close"].pct_change(20)

        # Volatility
        df["volatility_20"] = df["daily_return"].rolling(window=20).std()
        df["volatility_50"] = df["daily_return"].rolling(window=50).std()

        # Price momentum
        df["momentum_5"] = df["Close"] / df["Close"].shift(5) - 1
        df["momentum_10"] = df["Close"] / df["Close"].shift(10) - 1

        logger.info(f"Technical indicators computed. Shape: {df.shape}")
        return df

    def _compute_rsi(self, prices: pd.Series, window: int = 14) -> pd.Series:
        """Compute RSI indicator.

        Args:
            prices: Price series.
            window: RSI window period.

        Returns:
            RSI series.
        """
        delta = prices.diff()
        gain = (delta.where(delta > 0, 0)).rolling(window=window).mean()
        loss = (-delta.where(delta < 0, 0)).rolling(window=window).mean()
        rs = gain / loss
        rsi = 100 - (100 / (1 + rs))
        return rsi

    def _compute_macd(
        self, prices: pd.Series, fast: int = 12, slow: int = 26, signal: int = 9
    ) -> Tuple[pd.Series, pd.Series, pd.Series]:
        """Compute MACD indicator.

        Args:
            prices: Price series.
            fast: Fast EMA period.
            slow: Slow EMA period.
            signal: Signal line period.

        Returns:
            Tuple of (MACD, signal, histogram).
        """
        ema_fast = prices.ewm(span=fast, adjust=False).mean()
        ema_slow = prices.ewm(span=slow, adjust=False).mean()
        macd = ema_fast - ema_slow
        macd_signal = macd.ewm(span=signal, adjust=False).mean()
        macd_hist = macd - macd_signal
        return macd, macd_signal, macd_hist

    def _compute_bollinger_bands(
        self, prices: pd.Series, window: int = 20, num_std: float = 2.0
    ) -> Tuple[pd.Series, pd.Series, pd.Series]:
        """Compute Bollinger Bands.

        Args:
            prices: Price series.
            window: Moving average window.
            num_std: Number of standard deviations.

        Returns:
            Tuple of (upper, middle, lower) bands.
        """
        sma = prices.rolling(window=window).mean()
        std = prices.rolling(window=window).std()
        upper = sma + (std * num_std)
        lower = sma - (std * num_std)
        return upper, sma, lower

    def create_target_variable(
        self, df: pd.DataFrame, forward_days: int = 5, threshold: float = 0.02
    ) -> pd.DataFrame:
        """Create target variable for investment decisions.

        Args:
            df: DataFrame with price data.
            forward_days: Number of days to look forward.
            threshold: Return threshold for classification.

        Returns:
            DataFrame with target variable.
        """
        df = df.copy()

        # Compute forward returns
        df["forward_return"] = df["Close"].pct_change(forward_days).shift(-forward_days)

        # Create target: 0=SELL, 1=HOLD, 2=BUY
        df["target"] = 1  # Default to HOLD
        df.loc[df["forward_return"] > threshold, "target"] = 2  # BUY
        df.loc[df["forward_return"] < -threshold, "target"] = 0  # SELL

        # Drop rows with NaN target (last forward_days rows)
        df = df.dropna(subset=["target"])

        logger.info(f"Target distribution:\n{df['target'].value_counts()}")
        return df

    def prepare_features(
        self, df: pd.DataFrame, feature_list: Optional[list] = None
    ) -> pd.DataFrame:
        """Prepare feature matrix.

        Args:
            df: DataFrame with computed indicators.
            feature_list: List of features to use. If None, uses all numeric features.

        Returns:
            DataFrame with selected features.
        """
        df = df.copy()

        if feature_list is None:
            # Use all numeric features except target
            feature_list = [
                col
                for col in df.select_dtypes(include=[np.number]).columns
                if col not in ["target", "forward_return"]
            ]

        # Select features and drop NaN
        features_df = df[feature_list].dropna()

        self.feature_columns = feature_list
        logger.info(f"Features prepared. Columns: {len(feature_list)}")
        return features_df

    def split_data(
        self,
        df: pd.DataFrame,
        test_size: float = 0.2,
        val_size: float = 0.2,
        time_series_split: bool = True,
    ) -> Tuple[pd.DataFrame, pd.DataFrame, pd.DataFrame]:
        """Split data into train, validation, and test sets.

        Args:
            df: DataFrame with features and target.
            test_size: Proportion of data for test set.
            val_size: Proportion of data for validation set.
            time_series_split: Whether to use time-series split (chronological).

        Returns:
            Tuple of (train, val, test) DataFrames.
        """
        if time_series_split:
            # Chronological split
            n = len(df)
            test_start = int(n * (1 - test_size))
            val_start = int(n * (1 - test_size - val_size))

            train = df.iloc[:val_start]
            val = df.iloc[val_start:test_start]
            test = df.iloc[test_start:]
        else:
            # Random split
            train_val, test = train_test_split(
                df, test_size=test_size, random_state=self.random_seed
            )
            train, val = train_test_split(
                train_val, test_size=val_size / (1 - test_size), random_state=self.random_seed
            )

        logger.info(
            f"Data split - Train: {len(train)}, Val: {len(val)}, Test: {len(test)}"
        )
        return train, val, test

    def scale_features(
        self, train: pd.DataFrame, val: pd.DataFrame, test: pd.DataFrame
    ) -> Tuple[pd.DataFrame, pd.DataFrame, pd.DataFrame]:
        """Scale features using StandardScaler.

        Args:
            train: Training DataFrame.
            val: Validation DataFrame.
            test: Test DataFrame.

        Returns:
            Tuple of scaled (train, val, test) DataFrames.
        """
        feature_cols = [col for col in train.columns if col != "target"]

        # Fit scaler on training data
        train_scaled = train.copy()
        train_scaled[feature_cols] = self.scaler.fit_transform(train[feature_cols])

        # Transform validation and test
        val_scaled = val.copy()
        val_scaled[feature_cols] = self.scaler.transform(val[feature_cols])

        test_scaled = test.copy()
        test_scaled[feature_cols] = self.scaler.transform(test[feature_cols])

        logger.info("Features scaled using StandardScaler")
        return train_scaled, val_scaled, test_scaled

    def get_feature_importance_data(
        self, df: pd.DataFrame
    ) -> Tuple[np.ndarray, np.ndarray]:
        """Get features and target arrays for model training.

        Args:
            df: DataFrame with features and target.

        Returns:
            Tuple of (X, y) arrays.
        """
        feature_cols = [col for col in df.columns if col != "target"]
        X = df[feature_cols].values
        y = df["target"].values
        return X, y
