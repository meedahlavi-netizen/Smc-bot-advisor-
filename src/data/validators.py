"""Data validation utilities"""

import pandas as pd
import numpy as np
from typing import Optional
import logging

logger = logging.getLogger(__name__)


class DataValidator:
    """Validate market data integrity"""

    @staticmethod
    def validate_ohlcv(df: pd.DataFrame) -> bool:
        """Validate OHLCV data integrity"""
        if df.empty:
            logger.warning("Empty dataframe")
            return False

        required_columns = ['open', 'high', 'low', 'close', 'volume']
        if not all(col in df.columns for col in required_columns):
            logger.error("Missing required OHLCV columns")
            return False

        # Check for missing values
        if df.isnull().any().any():
            logger.warning("Found null values in data")
            return False

        # Validate price relationships
        if (df['high'] < df['low']).any():
            logger.error("High < Low found in data")
            return False

        if (df['high'] < df['close']).any() or (df['low'] > df['close']).any():
            logger.error("Close price outside high-low range")
            return False

        return True

    @staticmethod
    def validate_minimum_bars(df: pd.DataFrame, min_bars: int) -> bool:
        """Validate minimum number of bars"""
        if len(df) < min_bars:
            logger.warning(f"Insufficient bars: {len(df)} < {min_bars}")
            return False
        return True

    @staticmethod
    def remove_duplicates(df: pd.DataFrame) -> pd.DataFrame:
        """Remove duplicate timestamps"""
        return df.drop_duplicates(subset=['timestamp'], keep='last')

    @staticmethod
    def handle_missing_data(df: pd.DataFrame, method: str = 'forward_fill') -> pd.DataFrame:
        """Handle missing data"""
        if method == 'forward_fill':
            return df.fillna(method='ffill')
        elif method == 'interpolate':
            return df.interpolate()
        return df
