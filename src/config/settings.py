"""Settings and configuration management"""

import os
from pathlib import Path
from typing import Optional, Dict, Any
import yaml
from pydantic import BaseModel, Field


class APISettings(BaseModel):
    """API Configuration"""
    exchange: str = "binance"
    api_key: str = Field(default="")
    api_secret: str = Field(default="")
    sandbox_mode: bool = True


class TradingSettings(BaseModel):
    """Trading Configuration"""
    pairs: list = ["BTC/USDT", "ETH/USDT"]
    timeframes: list = ["1h", "4h", "1d"]


class SMCPatternsSettings(BaseModel):
    """SMC Pattern Detection Settings"""
    detect_order_blocks: bool = True
    detect_liquidity_levels: bool = True
    detect_supply_demand: bool = True
    detect_market_structure: bool = True
    detect_fair_value_gaps: bool = True
    sensitivity: float = 0.7
    min_candles: int = 5


class RiskManagementSettings(BaseModel):
    """Risk Management Settings"""
    account_risk_percent: float = 2.0
    max_daily_loss_percent: float = 5.0
    position_size_type: str = "fixed"
    default_position_size: float = 0.1
    default_risk_reward_ratio: float = 1.5
    max_leverage: float = 1.0
    max_open_positions: int = 5
    max_exposure_percent: float = 30.0


class SignalSettings(BaseModel):
    """Signal Generation Settings"""
    min_confidence_threshold: float = 0.65
    require_confluence: bool = True
    confluence_count: int = 2
    validate_higher_timeframe: bool = True
    validate_market_structure: bool = True


class ChartingSettings(BaseModel):
    """Charting Configuration"""
    enabled: bool = True
    update_interval: int = 300
    save_charts: bool = True
    chart_output_dir: str = "./charts"
    show_order_blocks: bool = True
    show_liquidity_levels: bool = True
    show_supply_demand: bool = True
    show_signals: bool = True
    show_risk_zones: bool = True


class LoggingSettings(BaseModel):
    """Logging Configuration"""
    level: str = "INFO"
    log_file: str = "./logs/smc_bot.log"


class DatabaseSettings(BaseModel):
    """Database Settings"""
    type: str = "sqlite"
    path: str = "./trades.db"


class Settings(BaseModel):
    """Main Settings Class"""
    api: APISettings = APISettings()
    trading: TradingSettings = TradingSettings()
    smc_patterns: SMCPatternsSettings = SMCPatternsSettings()
    risk_management: RiskManagementSettings = RiskManagementSettings()
    signals: SignalSettings = SignalSettings()
    charting: ChartingSettings = ChartingSettings()
    logging: LoggingSettings = LoggingSettings()
    database: DatabaseSettings = DatabaseSettings()

    @classmethod
    def from_yaml(cls, config_path: str) -> "Settings":
        """Load settings from YAML file"""
        with open(config_path, 'r') as f:
            config_dict = yaml.safe_load(f)
        return cls(**config_dict)

    @classmethod
    def from_env(cls) -> "Settings":
        """Load settings from environment variables"""
        return cls()
