"""Liquidity Level Analysis"""

import pandas as pd
import numpy as np
from typing import List, Dict
from dataclasses import dataclass
import logging

logger = logging.getLogger(__name__)


@dataclass
class LiquidityLevel:
    """Liquidity Level Data Structure"""
    price: float
    type: str  # "high" or "low"
    strength: int  # Number of times tested
    first_touch: int  # Index when first touched
    last_touch: int  # Index when last touched
    broken: bool = False
    break_index: int = None


class LiquidityAnalyzer:
    """Analyze liquidity levels (swing highs and lows)"""

    def __init__(self, lookback: int = 20, min_touches: int = 2):
        self.lookback = lookback
        self.min_touches = min_touches

    def detect_liquidity_levels(self, df: pd.DataFrame) -> List[LiquidityLevel]:
        """
        Detect liquidity levels (swing highs and lows)
        
        Args:
            df: OHLCV dataframe
            
        Returns:
            List of detected liquidity levels
        """
        if len(df) < 5:
            logger.warning("Insufficient data for liquidity detection")
            return []

        levels = []
        
        # Detect swing highs
        swing_highs = self._find_swing_highs(df)
        for high, index in swing_highs:
            level = LiquidityLevel(
                price=high,
                type="high",
                strength=1,
                first_touch=index,
                last_touch=index
            )
            levels.append(level)
        
        # Detect swing lows
        swing_lows = self._find_swing_lows(df)
        for low, index in swing_lows:
            level = LiquidityLevel(
                price=low,
                type="low",
                strength=1,
                first_touch=index,
                last_touch=index
            )
            levels.append(level)
        
        # Update strength based on touches
        levels = self._update_touch_strength(df, levels)
        
        return levels

    def _find_swing_highs(self, df: pd.DataFrame) -> List[tuple]:
        """Find swing highs"""
        swing_highs = []
        period = 2
        
        for i in range(period, len(df) - period):
            high = df.iloc[i]['high']
            
            is_swing_high = all(
                high > df.iloc[j]['high'] 
                for j in range(i - period, i + period + 1) if j != i
            )
            
            if is_swing_high:
                swing_highs.append((high, i))
        
        return swing_highs

    def _find_swing_lows(self, df: pd.DataFrame) -> List[tuple]:
        """Find swing lows"""
        swing_lows = []
        period = 2
        
        for i in range(period, len(df) - period):
            low = df.iloc[i]['low']
            
            is_swing_low = all(
                low < df.iloc[j]['low'] 
                for j in range(i - period, i + period + 1) if j != i
            )
            
            if is_swing_low:
                swing_lows.append((low, i))
        
        return swing_lows

    def _update_touch_strength(self, df: pd.DataFrame, levels: List[LiquidityLevel]) -> List[LiquidityLevel]:
        """Update liquidity level strength based on number of touches"""
        tolerance = 0.001
        
        for level in levels:
            touches = 0
            for i in range(len(df)):
                high = df.iloc[i]['high']
                low = df.iloc[i]['low']
                
                if self._price_touches_level(level.price, high, low, tolerance):
                    touches += 1
                    level.last_touch = i
            
            level.strength = touches
        
        return levels

    @staticmethod
    def _price_touches_level(level: float, high: float, low: float, tolerance: float) -> bool:
        """Check if price touched the liquidity level"""
        tolerance_value = level * tolerance
        return low <= level <= high or (level - tolerance_value <= high and level + tolerance_value >= low)

    def get_nearby_liquidity(self, df: pd.DataFrame, levels: List[LiquidityLevel], distance_percent: float = 0.02) -> List[LiquidityLevel]:
        """Get liquidity levels near current price"""
        current_price = df.iloc[-1]['close']
        distance = current_price * distance_percent
        
        nearby = [
            level for level in levels
            if abs(level.price - current_price) <= distance
        ]
        
        return sorted(nearby, key=lambda x: x.strength, reverse=True)
