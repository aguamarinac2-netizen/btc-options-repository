# BTCUSDT Options Trading System - User Guide

## 📋 Table of Contents
1. [Introduction](#introduction)
2. [System Overview](#system-overview)
3. [Installation](#installation)
4. [Configuration](#configuration)
5. [Running the System](#running-the-system)
6. [Understanding the Dashboard](#understanding-the-dashboard)
7. [Trading Strategies Explained](#trading-strategies-explained)
8. [Risk Management](#risk-management)
9. [Trading Schedule](#trading-schedule)
10. [FAQ](#faq)

---

## 🎯 Introduction

This AI-powered trading system analyzes BTCUSDT options markets on Binance and recommends optimal trading strategies. It uses machine learning to detect market regimes, calculate probabilities, and suggest strategies like Iron Condors, Butterflies, and Credit Spreads.

**Key Features:**
- ✅ Real-time market analysis
- ✅ AI-driven strategy recommendations
- ✅ Probability of profit calculations
- ✅ Semi-automated trading with manual approval
- ✅ Risk management built-in (max 5-10% capital per trade)
- ✅ Comprehensive reporting

---

## 🔧 System Overview

### Architecture
```
btc_options_trader/
├── main.py                          # Dashboard application
├── modules/
│   ├── binance_options_api.py       # Binance API integration
│   ├── options_pricing.py           # Black-Scholes pricing & Greeks
│   └── ai_strategy_analyzer.py      # AI market analysis
├── config/
│   └── credentials.json.example     # Your API credentials
└── logs/
    └── trades.json                  # Trade history log
```

### AI Components

1. **Market Regime Detector**
   - Analyzes price action, moving averages, volatility
   - Classifies market as: Ranging, Bullish Trend, Bearish Trend, or High Volatility
   - Provides confidence level (0-100%)

2. **Strategy Selector**
   - Matches optimal strategy to current market regime
   - Calculates win rates and probability of profit
   - Generates trade parameters automatically

3. **Risk Manager**
   - Limits position size to 5-10% of capital
   - Calculates max loss scenarios
   - Provides stop-loss recommendations

---

## 💻 Installation

### Prerequisites
- Python 3.10 or higher
- Active Binance account with Options trading enabled
- API keys with options trading permissions

### Step-by-Step Installation

1. **Install Python dependencies:**
```bash
cd /root/Desktop/btc_options_trader
pip install -r requirements.txt
```

2. **Verify your API keys are configured:**
   - Your API keys are already in `config/credentials.json.example`
   - API Key: `pxrBznR6cD64GZUhy9vuGOWPDrXb4W89hXMDRq1XAWvlK1VTJaSsiczU5t5ko7XN`
   - Secret: (configured)

3. **Test the connection:**
```bash
python -c "from modules.binance_options_api import BinanceOptionsAPI; import json; config = json.load(open('config/credentials.json.example')); api = BinanceOptionsAPI(config['binance']['api_key'], config['binance']['api_secret'], False); print(f'BTC Price: ${api.get_btc_spot_price():.2f}')"
```

---

## ⚙️ Configuration

The system is configured via `config/credentials.json.example`:

```json
{
  "binance": {
    "api_key": "YOUR_API_KEY",
    "api_secret": "YOUR_SECRET",
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
- **max_capital_per_trade_pct**: Maximum % of capital to risk per trade (default: 10%)
- **min_probability_of_profit**: Minimum POP to recommend a trade (default: 55%)
- **max_positions**: Maximum concurrent positions (default: 3)
- **default_capital**: Default trading capital in USDT (default: 5000)

---

## 🚀 Running the System

### Launch the Dashboard

```bash
cd /root/Desktop/btc_options_trader
streamlit run main.py
```

The dashboard will open in your browser at `http://localhost:8501`

### Dashboard Workflow

1. **View Market Data** - Real-time BTC price, volatility, and price chart
2. **Run Analysis** - Click "🤖 Run Analysis" in sidebar
3. **Review Recommendations** - AI shows recommended strategy with metrics
4. **Approve/Reject** - Manually approve or reject the trade
5. **Monitor** - Track trade history and performance

---

## 📊 Understanding the Dashboard

### Market Overview Section
- **BTC/USDT Price**: Current spot price
- **30-Day Volatility**: Historical volatility (annualized)
- **Current Time (UTC)**: System time
- **Trading Window**: Optimal (🟢), Good (🟡), or Fair (🟠)

### AI Analysis Section
- **Market Regime**: Current market classification
- **Confidence**: How confident the AI is (higher is better)
- **Recommended Strategy**: Best strategy for current conditions
- **Probability of Profit**: Expected success rate
- **Max Risk**: Maximum potential loss

### Trade Approval
- **✅ APPROVE TRADE**: Execute the recommended trade
- **❌ REJECT TRADE**: Skip this recommendation
- **🔄 RE-ANALYZE**: Run fresh analysis with updated data

---

## 📈 Trading Strategies Explained

### 1. Iron Condor
**Best For:** Range-bound, low volatility markets  
**Win Rate:** ~65%  
**Description:** Sell OTM call & put spreads, collect premium  
**Max Profit:** Net credit received  
**Max Loss:** Spread width minus credit  

**Example:**
- Current BTC: $50,000
- Sell Call: $55,000
- Buy Call: $60,000
- Sell Put: $45,000
- Buy Put: $40,000
- Collect $500 premium, max loss $4,500

### 2. Butterfly Spread
**Best For:** Neutral markets, expect price to stay near specific level  
**Win Rate:** ~55%  
**Description:** Buy 1 low strike, sell 2 middle, buy 1 high  
**Max Profit:** At middle strike at expiration  
**Max Loss:** Net debit paid  

### 3. Bull Call Spread
**Best For:** Bullish trending markets  
**Win Rate:** ~60%  
**Description:** Buy ATM call, sell OTM call  
**Max Profit:** Difference in strikes minus debit  
**Max Loss:** Net debit paid  

### 4. Bear Put Spread
**Best For:** Bearish trending markets  
**Win Rate:** ~60%  
**Description:** Buy ATM put, sell OTM put  
**Max Profit:** Difference in strikes minus debit  
**Max Loss:** Net debit paid  

### 5. Long Straddle
**Best For:** High volatility, expecting big move  
**Win Rate:** ~45% (but higher profit when wins)  
**Description:** Buy ATM call AND ATM put  
**Max Profit:** Unlimited (theoretically)  
**Max Loss:** Total premium paid  

### 6. Credit Spread
**Best For:** Ranging markets with high IV  
**Win Rate:** ~62%  
**Description:** Sell option, buy further OTM option for protection  
**Max Profit:** Net credit received  
**Max Loss:** Spread width minus credit  

---

## ⚠️ Risk Management

### Position Sizing
- **Default:** 8% of total capital per trade
- **Conservative:** 5% per trade
- **Moderate:** 10% per trade
- **Never exceed:** 15% per trade

### Stop Loss Rules
1. Exit if loss reaches 50% of max risk
2. Close position if market regime changes significantly
3. Consider rolling position if approaching expiration

### Diversification
- Spread trades across 2-3 different expiration dates
- Don't put all capital in same strategy type
- Monitor total portfolio Greeks (delta, theta, vega)

### Capital Preservation
- Start with $1,000-$5,000 for testing
- Never risk money you can't afford to lose
- Keep 50% of capital in reserve
- Options can expire worthless - understand the risks!

---

## 🕐 Trading Schedule

### Optimal Trading Hours (UTC)
The AI recommends trading during high liquidity periods:

**Primary Windows:**
- 08:00-10:00 UTC (Asian/European overlap)
- 14:00-16:00 UTC (European/US overlap)

**Why these times?**
- Highest trading volume
- Tighter bid-ask spreads
- Better order fills
- More accurate pricing

**Avoid:**
- Weekends (lower liquidity)
- Late night hours (wider spreads)
- Major economic news releases (unpredictable volatility)

### Daily Workflow Recommendation

**Morning (08:00-10:00 UTC):**
1. Check overnight price action
2. Run AI analysis
3. Review recommended trades
4. Place approved orders

**Afternoon (14:00-16:00 UTC):**
1. Monitor existing positions
2. Check for adjustment opportunities
3. Run fresh analysis if needed
4. Consider new positions

**Evening:**
1. Review daily performance
2. Update trade journal
3. Plan next day's trades

---

## ❓ FAQ

### Q: Is the system fully automated?
**A:** No, it's semi-automated. The AI recommends trades, but YOU must approve each one manually. This keeps you in control and helps you learn.

### Q: What is Probability of Profit (POP)?
**A:** The estimated chance the trade will be profitable at expiration. POP of 65% means 65% chance of profit, 35% chance of loss.

### Q: How much capital do I need?
**A:** Minimum $1,000, recommended $5,000-$10,000. Start small to learn the system.

### Q: Can I lose more than my initial investment?
**A:** With defined-risk spreads (our focus), your max loss is limited to the spread width. Always use defined-risk strategies.

### Q: How often should I trade?
**A:** Quality over quantity. 2-3 high-probability trades per week is better than daily trading.

### Q: What if I disagree with the AI recommendation?
**A:** Always use your judgment! The AI is a tool, not a replacement for your decision-making. Reject trades you're not comfortable with.

### Q: How do I track my performance?
**A:** Check the "Trade History" section at the bottom of the dashboard. All trades are logged to `logs/trades.json`.

### Q: Can I use this on testnet first?
**A:** Yes! Set `"testnet": true` in the config file to test without real money.

### Q: What's the expected monthly return?
**A:** This varies greatly. With good risk management, experienced traders target 5-10% monthly, but there are no guarantees. Always prioritize capital preservation.

### Q: Does this work for other cryptocurrencies?
**A:** Currently optimized for BTCUSDT. Could be adapted for ETH or other assets with liquid options markets.

---

## 🛡️ Important Disclaimers

### Risk Warning
**OPTIONS TRADING IS HIGHLY RISKY AND NOT SUITABLE FOR EVERYONE**

- You can lose 100% of your investment
- Past performance doesn't guarantee future results
- AI predictions can be wrong
- Market conditions can change rapidly
- Always do your own research
- Never invest more than you can afford to lose

### No Financial Advice
This system is for educational and informational purposes only. It does NOT constitute financial advice. Consult a licensed financial advisor before trading.

### System Limitations
- AI models can fail during unprecedented market conditions
- Binance API can have outages
- Network issues can delay order execution
- Slippage can affect actual fills vs. theoretical prices

---

## 📞 Support & Resources

### Learning Resources
- **Options Basics**: https://www.investopedia.com/options-basics-tutorial-4583012
- **Greeks Explained**: https://www.optionseducation.org/referencelibrary/white-papers/page-assets/listed-options-greeks.aspx
- **Binance Options Guide**: https://www.binance.com/en/support/faq/options

### System Files
- Main application: `main.py`
- API integration: `modules/binance_options_api.py`
- AI analyzer: `modules/ai_strategy_analyzer.py`
- Pricing engine: `modules/options_pricing.py`
- Trade logs: `logs/trades.json`

---

## 🎓 Quick Start Checklist

- [ ] Install Python dependencies
- [ ] Configure API keys
- [ ] Test API connection
- [ ] Launch dashboard (`streamlit run main.py`)
- [ ] Review market overview
- [ ] Run first analysis
- [ ] Review recommended strategy
- [ ] Understand max risk
- [ ] Check trading window timing
- [ ] Approve or reject trade
- [ ] Monitor trade history
- [ ] Keep trade journal

---

**Good luck and trade responsibly! 🚀📈**
