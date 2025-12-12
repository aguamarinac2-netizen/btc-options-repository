# 📈 BTCUSDT Options Trading System

**AI-Powered Semi-Automated Options Trading with Manual Approval**

A sophisticated trading system that analyzes Bitcoin options markets on Binance and recommends optimal strategies using artificial intelligence. The system detects market regimes, calculates probabilities of profit, and suggests strategies like Iron Condors, Butterfly Spreads, and Credit Spreads - all while requiring your manual approval for every trade.

---

## ✨ Key Features

- 🤖 **AI Market Analysis** - Automated regime detection (Trending, Ranging, High Volatility)
- 📊 **Real-Time Data** - Live BTC prices, volatility metrics, and options data from Binance
- 🎯 **Strategy Recommendations** - 6 different options strategies with probability calculations
- ✅ **Semi-Automated Trading** - AI recommends, YOU approve each trade
- 📈 **Black-Scholes Pricing** - Accurate options pricing with Greeks (Delta, Gamma, Theta, Vega)
- 🛡️ **Risk Management** - Position sizing limited to 5-10% of capital per trade
- 📱 **Interactive Dashboard** - Beautiful Streamlit web interface
- 📜 **Trade Logging** - Complete history of all recommendations and executions
- ⏰ **Optimal Timing** - Recommendations for best trading windows

---

## 🎯 Supported Strategies

| Strategy | Best Market Condition | Win Rate | Risk/Reward |
|----------|----------------------|----------|-------------|
| **Iron Condor** | Range-bound, Low Vol | ~65% | Defined Risk |
| **Butterfly Spread** | Neutral, Pinned Price | ~55% | Defined Risk |
| **Bull Call Spread** | Bullish Trend | ~60% | Defined Risk |
| **Bear Put Spread** | Bearish Trend | ~60% | Defined Risk |
| **Credit Spread** | High IV, Ranging | ~62% | Defined Risk |
| **Long Straddle** | High Volatility | ~45% | High Risk/Reward |

---

## 🚀 Quick Start

### Prerequisites
- Python 3.10+
- Binance account with Options trading enabled
- API keys with options permissions (read + trade)
- Recommended capital: $1,000 - $10,000 USDT

### Installation

```bash
# Navigate to the project directory
cd /root/Desktop/btc_options_trader

# Install dependencies
pip install -r requirements.txt

# Make start script executable
chmod +x start_trading.sh

# Launch the system
./start_trading.sh
```

**Or manually:**
```bash
streamlit run main.py
```

The dashboard will open at `http://localhost:8501`

---

## ⚙️ Configuration

Your API credentials are already configured in `config/credentials.json.example`:

```json
{
  "binance": {
    "api_key": "pxrBznR6cD64GZUhy9vuGOWPDrXb4W89hXMDRq1XAWvlK1VTJaSsiczU5t5ko7XN",
    "api_secret": "zSI1j2A52GywHALZgG7bdqbyafrKxk2cAVJEX7a7ljroJwEuUYrcYqQmlSCmnf6U",
    "testnet": false
  },
  "trading_config": {
    "max_capital_per_trade_pct": 10,
    "min_probability_of_profit": 55,
    "max_positions": 3,
    "default_capital": 5000
  }
}
```

### Configuration Options:
- `max_capital_per_trade_pct`: Max % of capital per trade (default: 10%)
- `min_probability_of_profit`: Minimum POP to show recommendations (default: 55%)
- `max_positions`: Maximum concurrent positions (default: 3)
- `default_capital`: Your trading capital in USDT (default: 5000)

---

## 📖 How It Works

### 1. Market Analysis
The AI analyzes:
- 100 periods of historical price data
- Moving averages (20-period, 50-period)
- Average True Range (ATR) for volatility
- Trend strength indicators
- Current market regime classification

### 2. Strategy Selection
Based on market conditions, the AI:
- Scores each strategy's suitability
- Calculates probability of profit using Monte Carlo simulations
- Generates optimal strike prices and position sizes
- Considers your capital and risk parameters

### 3. Manual Approval
You review:
- Recommended strategy with full details
- Max profit, max loss, and probability metrics
- Trade parameters (strikes, expiration, contracts)
- Risk assessment and timing recommendation

### 4. Execution (Simulated by Default)
- Approved trades are logged to `logs/trades.json`
- Connect to live trading by implementing order execution
- Monitor positions and performance

---

## 🕐 When to Trade

The system recommends trading during high liquidity windows:

**Optimal Hours (UTC):**
- 08:00 - 10:00 (Asian/European overlap)
- 14:00 - 16:00 (European/US overlap)

**Avoid:**
- Weekends (lower liquidity)
- Late night hours (wider spreads)
- Major news events (unpredictable volatility)

---

## 📊 Dashboard Guide

### Main Interface

1. **Market Overview** - Current BTC price, volatility, time, and trading window status
2. **Price Chart** - Interactive candlestick chart with volume
3. **AI Analysis** - Market regime, recommended strategy, probability of profit
4. **Trade Approval** - Approve/Reject/Re-analyze buttons
5. **Trade History** - Log of all past recommendations and actions

### Workflow

```
1. Launch Dashboard → 2. Click "Run Analysis" → 3. Review Recommendation
                                ↓
4. Approve or Reject ← 5. Monitor Results ← 6. Track History
```

---

## ⚠️ Risk Management

### Position Sizing Rules
- **Conservative**: 5% of capital per trade
- **Moderate**: 8% of capital per trade (default)
- **Aggressive**: 10% of capital per trade
- **Never exceed**: 15% per trade

### Stop Loss Guidelines
- Exit if loss reaches 50% of max risk
- Close position if market regime changes
- Consider rolling before expiration

### Capital Preservation
- Start small ($1,000-$5,000)
- Keep 50% of capital in reserve
- Diversify across different expirations
- Never risk money you can't afford to lose

---

## 📂 Project Structure

```
btc_options_trader/
├── main.py                          # Main dashboard application
├── requirements.txt                 # Python dependencies
├── start_trading.sh                 # Quick start script
├── README.md                        # This file
├── USER_GUIDE.md                    # Comprehensive user guide
│
├── config/
│   └── credentials.json.example     # API credentials
│
├── modules/
│   ├── __init__.py                  # Module initialization
│   ├── binance_options_api.py       # Binance API integration
│   ├── options_pricing.py           # Black-Scholes pricing & Greeks
│   └── ai_strategy_analyzer.py      # AI market analysis engine
│
├── logs/
│   └── trades.json                  # Trade history log
│
├── data/                            # Market data cache (auto-generated)
└── models/                          # AI models (future expansion)
```

---

## 🛠️ Technical Details

### AI Components

**Market Regime Detector**
- Analyzes price patterns and volatility
- Uses technical indicators (SMA, ATR, trend strength)
- Classifies markets with confidence scores

**Strategy Selector**
- Matches strategies to market regimes
- Calculates position parameters automatically
- Optimizes risk/reward ratios

**Options Pricing Engine**
- Black-Scholes model for fair value
- Greeks calculation (Delta, Gamma, Theta, Vega, Rho)
- Monte Carlo simulations for probability
- Implied volatility calculations

### Technologies Used
- Python 3.10+
- Streamlit (Web Dashboard)
- CCXT (Exchange API)
- NumPy/Pandas (Data Processing)
- Scikit-learn (Machine Learning)
- Plotly (Interactive Charts)
- SciPy (Statistical Functions)

---

## 📚 Resources

### Documentation
- **User Guide**: See `USER_GUIDE.md` for detailed instructions
- **API Docs**: `modules/` directory contains inline documentation
- **Binance Options**: https://www.binance.com/en/support/faq/options

### Learning Materials
- Options Basics: https://www.investopedia.com/options-basics-tutorial-4583012
- Greeks Explained: https://www.optionseducation.org
- Trading Strategies: https://www.optionsplaybook.com

---

## ⚡ Example Usage

```bash
# Start the system
cd /root/Desktop/btc_options_trader
./start_trading.sh

# Or use Python directly
streamlit run main.py
```

**In the Dashboard:**
1. View current BTC price and market conditions
2. Click "🤖 Run Analysis" in the sidebar
3. Review the AI's recommended strategy
4. Check probability of profit and max risk
5. Click "✅ APPROVE TRADE" if you agree
6. Monitor your trade history at the bottom

---

## 🛡️ Safety & Disclaimers

### ⚠️ RISK WARNING
**OPTIONS TRADING IS HIGHLY RISKY AND NOT SUITABLE FOR EVERYONE**

- You can lose 100% of your investment
- Past performance doesn't guarantee future results
- AI predictions can be wrong
- Market conditions can change rapidly
- Always do your own research
- Never invest more than you can afford to lose

### Legal Disclaimer
This system is for **educational purposes only** and does NOT constitute financial advice. Trading options involves substantial risk and is not suitable for every investor. Consult a licensed financial advisor before trading.

### System Limitations
- AI models may fail during unprecedented market conditions
- Binance API outages can occur
- Network latency can affect execution
- Slippage may impact actual fills vs. theoretical prices

---

## 🤝 Support

For questions or issues:
1. Review the `USER_GUIDE.md` for detailed instructions
2. Check the FAQ section in the user guide
3. Verify your API credentials are correct
4. Ensure you have sufficient capital and permissions

---

## 📈 Performance Tracking

All trades are logged to `logs/trades.json` with:
- Timestamp
- Strategy type
- Trade parameters
- Probability of profit
- Execution status
- Notes and metadata

---

## 🎓 Best Practices

1. **Start Small** - Test with minimum capital first
2. **Understand the Strategy** - Don't trade what you don't understand
3. **Manage Risk** - Never exceed 10% capital per trade
4. **Trade During Optimal Hours** - Better liquidity = better fills
5. **Keep Learning** - Review every trade and learn from results
6. **Stay Disciplined** - Follow your trading plan
7. **Use Stop Losses** - Exit losing trades at 50% of max risk

---

## 🚦 Current Status

✅ **Ready to Use** - System is fully functional with your API keys configured

**What's Working:**
- ✅ Real-time market data fetching
- ✅ AI market analysis
- ✅ Strategy recommendations
- ✅ Probability calculations
- ✅ Interactive dashboard
- ✅ Trade logging

**Current Mode:**
- 🟡 **SIMULATION MODE** - Trades are logged but not executed
- To enable live trading, implement order execution in `execute_trade()` method

---

## 📝 Quick Start Checklist

- [x] Python 3.10+ installed
- [x] Dependencies in `requirements.txt`
- [x] API credentials configured
- [ ] Review USER_GUIDE.md
- [ ] Understand risk warnings
- [ ] Launch dashboard
- [ ] Run first analysis
- [ ] Approve first trade
- [ ] Monitor results

---

**Trade Smart. Trade Safe. Good Luck! 🚀📈**
