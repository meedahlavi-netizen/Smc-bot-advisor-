"""Order Block Analysis"""

import pandas as pd
import numpy as np
from typing import List, Dict, Tuple
from dataclasses import dataclass
import logging

logger = logging.getLogger(__name__)


@dataclass
class OrderBlock:
    """Order Block Data Structure"""
    index: int
    high: float
    low: float
    close: float
    type: str  # "bullish" or "bearish"
    strength: float  # 0-1.0
    touched_count: int = 0
    last_touched: int = None


class OrderBlockAnalyzer:
    """Analyze and identify order blocks"""

    def __init__(self, min_candles: int = 5):
        self.min_candles = min_candles

    def detect_order_blocks(self, df: pd.DataFrame, sensitivity: float = 0.7) -> List[OrderBlock]:
        """
        Detect order blocks from price data
        
        Args:
            df: OHLCV dataframe
            sensitivity: Detection sensitivity (0-1.0)
            
        Returns:
            List of detected OrderBlocks
        """
        if len(df) < self.min_candles:
            logger.warning(f"Insufficient data: {len(df)} bars")
            return []

        order_blocks = []
        
        # Detect bearish order blocks (mitigated by downmove)
        for i in range(self.min_candles, len(df) - 1):
            if self._is_bearish_ob(df, i):
                strength = self._calculate_strength(df, i, sensitivity)
                ob = OrderBlock(
                    index=i,
                    high=df.iloc[i]['high'],
                    low=df.iloc[i]['low'],
                    close=df.iloc[i]['close'],
                    type="bearish",
                    strength=strength
                )
                order_blocks.append(ob)
        
        # Detect bullish order blocks
        for i in range(self.min_candles, len(df) - 1):
            if self._is_bullish_ob(df, i):
                strength = self._calculate_strength(df, i, sensitivity)
                ob = OrderBlock(
                    index=i,
                    high=df.iloc[i]['high'],
                    low=df.iloc[i]['low'],
                    close=df.iloc[i]['close'],
                    type="bullish",
                    strength=strength
                )
                order_blocks.append(ob)

        return order_blocks

    def _is_bearish_ob(self, df: pd.DataFrame, i: int) -> bool:
        """Check if bar is a bearish order block"""
        if i < 1 or i >= len(df) - 1:
            return False
        
        current = df.iloc[i]
        prev = df.iloc[i - 1]
        
        # Strong bearish candle with high rejection
        is_bearish = (
            prev['close'] < prev['open'] and
            current['close'] < current['open'] and
            current['low'] < prev['low']
        )
        
        return is_bearish

    def _is_bullish_ob(self, df: pd.DataFrame, i: int) -> bool:
        """Check if bar is a bullish order block"""
        if i < 1 or i >= len(df) - 1:
            return False
        
        current = df.iloc[i]
        prev = df.iloc[i - 1]
        
        # Strong bullish candle with high rejection
        is_bullish = (
            prev['close'] > prev['open'] and
            current['close'] > current['open'] and
            current['high'] > prev['high']
        )
        
        return is_bullish

    def _calculate_strength(self, df: pd.DataFrame, index: int, sensitivity: float) -> float:
        """Calculate order block strength"""
        if index < 1:
            return 0.0
        
        current = df.iloc[index]
        
        body_size = abs(current['close'] - current['open'])
        total_range = current['high'] - current['low']
        
        if total_range == 0:
            return 0.0
        
        strength = min(body_size / total_range * sensitivity, 1.0)
        return strength

    def get_active_order_blocks(self, df: pd.DataFrame, order_blocks: List[OrderBlock], lookback: int = 50) -> List[OrderBlock]:
        """Get order blocks that are still active (not yet mitigated)"""
        active = []
        current_price = df.iloc[-1]['close']
        
        for ob in order_blocks:
            if ob.index < len(df) - lookback:
                continue
            
            if self._price_in_zone(current_price, ob.low, ob.high):
                active.append(ob)
        
        return active

    @staticmethod
    def _price_in_zone(price: float, low: float, high: float) -> bool:
        """Check if price is within zone"""
        return low <= price <= high
