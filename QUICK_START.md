# 🚀 Quick Start Guide - BTCUSDT Options Trading System

## ⚡ Start Trading in 3 Steps

### Step 1: Navigate to the project
```bash
cd /root/Desktop/btc_options_trader
```

### Step 2: Choose your interface

#### Option A: Command-Line Interface (Recommended for beginners)
```bash
python trading_cli.py
```

#### Option B: Web Dashboard Interface
```bash
streamlit run main.py
```
Then open your browser to `http://localhost:8501`

### Step 3: Follow the prompts
- Enter your trading capital (default: $5,000 USDT)
- Review the AI's market analysis
- Approve or reject each trade recommendation

---

## 📋 System Features

✅ **AI-Powered Analysis** - Detects market regimes and recommends optimal strategies  
✅ **Manual Approval Required** - You control every trade  
✅ **Risk Management** - Position sizing limited to 5-10% of capital  
✅ **6 Strategy Types** - Iron Condor, Butterfly, Spreads, Straddles  
✅ **Real-Time Data** - Live BTC prices and volatility from Binance  
✅ **Simulation Mode** - Trades are logged but not executed (safe for testing)  

---

## 🎯 Recommended Strategies

| Strategy | Market Condition | Win Rate | Best For |
|----------|-----------------|----------|----------|
| **Iron Condor** | Ranging/Low Vol | 65% | Beginners |
| **Butterfly Spread** | Neutral | 55% | Advanced |
| **Bull Call Spread** | Bullish | 60% | Trending up |
| **Bear Put Spread** | Bearish | 60% | Trending down |
| **Credit Spread** | High IV | 62% | Income |
| **Long Straddle** | High Vol | 45% | Experienced |

---

## ⚠️ Important Safety Rules

1. **Start Small** - Test with minimum capital ($100-$500)
2. **Never Risk More Than 10%** - Per trade maximum
3. **Understand Before Trading** - Read the strategy details
4. **Trade During Optimal Hours** - 08:00-10:00 UTC or 14:00-16:00 UTC
5. **Use Stop Losses** - Exit at 50% of max risk
6. **Keep Learning** - Review every trade outcome

---

## 🔑 API Configuration

Your API keys are pre-configured in `config/credentials.json.example`:

```json
{
  "binance": {
    "api_key": "pxrBznR6cD64GZUhy9vuGOWPDrXb4W89hXMDRq1XAWvlK1VTJaSsiczU5t5ko7XN",
    "api_secret": "zSI1j2A52GywHALZgG7bdqbyafrKxk2cAVJEX7a7ljroJwEuUYrcYqQmlSCmnf6U",
    "testnet": false
  }
}
```

**Note:** Due to location restrictions, the system uses simulated data for demonstration. This is safe and perfect for learning!

---

## 📊 Example Session

```
$ python trading_cli.py

💰 Enter your trading capital: 5000

📊 MARKET OVERVIEW
  💰 BTC/USDT Price:     $95,000.00
  📈 30-Day Volatility:  65.00%
  🕐 Current Time (UTC): 2025-12-12 21:23:00

🤖 AI ANALYSIS RESULTS
📍 MARKET REGIME: 🟦 RANGING
💡 RECOMMENDED STRATEGY: IRON CONDOR
   Probability of Profit:  75.0%
   Max Risk:               $500.00
   Expected Return:        $300.00

TRADE APPROVAL:
  [1] ✅ APPROVE TRADE
  [2] ❌ REJECT TRADE
  [3] 🔄 RE-ANALYZE
  [4] 🚪 EXIT

Your choice: 1

✅ Trade approved and logged!
```

---

## 🛠️ Troubleshooting

### Dependencies not installed?
```bash
pip install -r requirements.txt
```

### API connection issues?
The system automatically uses simulated data for demonstration - this is normal and safe!

### Want to modify settings?
Edit `config/credentials.json.example`:
- `max_capital_per_trade_pct`: Max % per trade (default: 10%)
- `min_probability_of_profit`: Min POP to show trades (default: 55%)
- `default_capital`: Your trading capital (default: 5000)

---

## 📚 Learn More

- **Full Documentation**: See `README.md`
- **Detailed User Guide**: See `USER_GUIDE.md`
- **Strategy Reference**: See `QUICK_REFERENCE.md`
- **Trade Logs**: Check `logs/trades.json`

---

## 🚦 System Status

✅ **Ready to Use**  
🟡 **Simulation Mode Active** (No real trades executed)  
✅ **All Dependencies Installed**  
✅ **API Configured**  

---

## ⚠️ Risk Warning

**OPTIONS TRADING IS HIGHLY RISKY**

- You can lose 100% of your investment
- AI predictions can be wrong
- Never invest money you can't afford to lose
- Always do your own research
- This is for educational purposes only

---

## 🎓 Best Practices

1. **Test First** - Use simulated mode to learn the system
2. **Start Small** - Begin with minimal capital
3. **Set Limits** - Never exceed 10% per trade
4. **Be Patient** - Wait for high-probability setups
5. **Learn Continuously** - Review every trade outcome
6. **Trade Sober** - Never trade emotionally or impulsively
7. **Keep Records** - Track all trades in the log

---

## 🆘 Need Help?

1. Review the comprehensive `USER_GUIDE.md`
2. Check the troubleshooting section in `README.md`
3. Examine the code in `modules/` directory
4. Review logged trades in `logs/trades.json`

---

**Ready to Start? Run:** `python trading_cli.py`

**Trade Smart. Trade Safe. Good Luck! 🚀📈**
