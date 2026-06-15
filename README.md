# SMC Bot Advisor

A Python-based Smart Money Concepts (SMC) trading bot advisor with real-time chart analysis, pattern recognition, and advanced risk management.

## Features

- **SMC Pattern Detection**
  - Order Blocks identification
  - Liquidity Levels analysis
  - Supply and Demand Zones
  - Market Structure (highs/lows)
  - Fair Value Gaps (FVG)
  - Mitigation blocks

- **Real-time Analysis**
  - Live charting integration with Plotly
  - Real-time market data from multiple sources
  - Continuous pattern monitoring
  - Multi-timeframe analysis

- **Signal Generation**
  - Automated trading signal generation
  - Buy/Sell recommendations with confidence scores
  - Entry/Exit point identification
  - Signal filtering and validation

- **Risk Management**
  - Position sizing based on risk parameters
  - Stop-loss and take-profit calculation
  - Risk-reward ratio analysis
  - Portfolio exposure tracking
  - Drawdown management

- **Trading Execution**
  - Position management
  - Order placement (with paper trading support)
  - Trade logging and history
  - Performance tracking

## Quick Start

```python
from src.bot.advisor import SMCBotAdvisor

# Initialize the bot
bot = SMCBotAdvisor(config_file='config.yaml')

# Start analysis
bot.start()

# Monitor signals in real-time
while True:
    signals = bot.get_latest_signals()
    for signal in signals:
        print(f"Signal: {signal}")
```

## Installation

1. Clone the repository:
```bash
git clone https://github.com/meedahlavi-netizen/Smc-bot-advisor-.git
cd Smc-bot-advisor-
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

3. Configure settings:
Edit `config.yaml` with your API keys and preferences

## Project Structure

```
Smc-bot-advisor-/
├── src/
│   ├── __init__.py
│   ├── config/
│   │   ├── __init__.py
│   │   └── settings.py
│   ├── data/
│   │   ├── __init__.py
│   │   ├── fetcher.py
│   │   └── validators.py
│   ├── analysis/
│   │   ├── __init__.py
│   │   ├── smc_patterns.py
│   │   ├── order_blocks.py
│   │   ├── liquidity.py
│   │   ├── supply_demand.py
│   │   └── market_structure.py
│   ├── signals/
│   │   ├── __init__.py
│   │   ├── signal_generator.py
│   │   └── validators.py
│   ├── risk/
│   │   ├── __init__.py
│   │   ├── position_manager.py
│   │   ├── risk_calculator.py
│   │   └── portfolio.py
│   ├── execution/
│   │   ├── __init__.py
│   │   ├── broker_interface.py
│   │   └── trade_executor.py
│   ├── charting/
│   │   ├── __init__.py
│   │   └── live_plotter.py
│   └── bot/
│       ├── __init__.py
│       └── advisor.py
├── tests/
│   ├── __init__.py
│   ├── test_smc_patterns.py
│   ├── test_signal_generator.py
│   └── test_risk_manager.py
├── examples/
│   ├── basic_usage.py
│   └── advanced_trading.py
├── config.yaml
├── requirements.txt
└── .gitignore
```

## Dependencies

- pandas: Data manipulation
- numpy: Numerical computations
- plotly: Interactive charting
- websocket-client: Real-time data streaming
- ccxt: Crypto exchange API
- ta: Technical analysis indicators
- pydantic: Data validation

## Risk Disclaimer

This bot is for educational and research purposes. Trading cryptocurrencies and forex involves significant risk. Always use appropriate risk management and never risk more than you can afford to lose.

## License

MIT License - see LICENSE file for details
