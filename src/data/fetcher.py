"""Market data fetcher using CCXT"""

import ccxt
import pandas as pd
from typing import Optional, List
from datetime import datetime, timedelta
import logging

logger = logging.getLogger(__name__)


class DataFetcher:
    """Fetch market data from exchanges"""

    def __init__(self, exchange_name: str, api_key: str = "", api_secret: str = "", sandbox: bool = True):
        """Initialize data fetcher"""
        self.exchange_name = exchange_name.lower()
        self.sandbox = sandbox
        
        try:
            exchange_class = getattr(ccxt, self.exchange_name)
            self.exchange = exchange_class({
                'apiKey': api_key,
                'secret': api_secret,
                'enableRateLimit': True,
                'sandbox': sandbox
            })
        except AttributeError:
            raise ValueError(f"Exchange {exchange_name} not supported by CCXT")

    def fetch_ohlcv(self, symbol: str, timeframe: str, limit: int = 100) -> pd.DataFrame:
        """Fetch OHLCV data"""
        try:
            ohlcv = self.exchange.fetch_ohlcv(symbol, timeframe, limit=limit)
            df = pd.DataFrame(
                ohlcv,
                columns=['timestamp', 'open', 'high', 'low', 'close', 'volume']
            )
            df['timestamp'] = pd.to_datetime(df['timestamp'], unit='ms')
            return df
        except Exception as e:
            logger.error(f"Error fetching OHLCV data for {symbol}: {e}")
            return pd.DataFrame()

    def fetch_multiple_timeframes(self, symbol: str, timeframes: List[str]) -> dict:
        """Fetch data for multiple timeframes"""
        data = {}
        for tf in timeframes:
            data[tf] = self.fetch_ohlcv(symbol, tf)
        return data

    def get_supported_timeframes(self) -> List[str]:
        """Get supported timeframes for exchange"""
        return self.exchange.timeframes if hasattr(self.exchange, 'timeframes') else []
