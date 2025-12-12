# 📋 Quick Reference Card

## 🚀 Launch Commands

```bash
# Quick Start (Recommended)
cd /root/Desktop/btc_options_trader
./start_trading.sh

# Manual Start
streamlit run main.py
```

Dashboard opens at: **http://localhost:8501**

---

## 📊 Dashboard Quick Actions

| Action | Button/Location | Description |
|--------|----------------|-------------|
| **Run Analysis** | Sidebar → "🤖 Run Analysis" | Analyze market and get recommendation |
| **Approve Trade** | Main Area → "✅ APPROVE TRADE" | Execute recommended strategy |
| **Reject Trade** | Main Area → "❌ REJECT TRADE" | Skip this recommendation |
| **Re-Analyze** | Main Area → "🔄 RE-ANALYZE" | Get fresh recommendation |
| **Refresh Data** | Sidebar → "🔄 Refresh Data" | Update market data |
| **Change Capital** | Sidebar → Input field | Adjust trading capital |

---

## 🎯 Trading Strategies at a Glance

| Strategy | Market Type | Win % | When to Use |
|----------|-------------|-------|-------------|
| **Iron Condor** | Ranging | 65% | Low volatility, sideways market |
| **Butterfly** | Neutral | 55% | Expect price to stay near level |
| **Bull Call Spread** | Bullish | 60% | Moderate upward move expected |
| **Bear Put Spread** | Bearish | 60% | Moderate downward move expected |
| **Credit Spread** | Ranging | 62% | High IV, want to collect premium |
| **Long Straddle** | Volatile | 45% | Expect large move either direction |

---

## ⏰ Optimal Trading Times (UTC)

✅ **Best:** 08:00-10:00, 14:00-16:00  
🟡 **Good:** 07:00, 11:00, 13:00, 17:00  
❌ **Avoid:** Weekends, Late night, News events

---

## 🛡️ Risk Management Rules

- **Max per trade:** 10% of capital
- **Recommended:** 5-8% of capital
- **Stop loss:** Exit at 50% of max risk
- **Max positions:** 3 concurrent trades
- **Reserve capital:** Keep 50% in reserve

---

## 📈 Key Metrics to Watch

| Metric | What It Means | Target |
|--------|---------------|--------|
| **Probability of Profit (POP)** | Chance trade will be profitable | > 55% |
| **Win Rate** | Historical success rate | > 50% |
| **Max Risk** | Maximum possible loss | < 10% capital |
| **Confidence** | AI certainty in regime | > 70% |
| **Volatility** | Price movement magnitude | Varies |

---

## 🔧 Configuration Quick Edit

Location: `config/credentials.json.example`

```json
{
  "trading_config": {
    "max_capital_per_trade_pct": 10,    ← Change this
    "min_probability_of_profit": 55,    ← Or this
    "max_positions": 3,                 ← Or this
    "default_capital": 5000             ← Or this
  }
}
```

---

## 🚨 Emergency Actions

| Issue | Solution |
|-------|----------|
| **Dashboard won't start** | Check Python version, reinstall deps |
| **API errors** | Verify API keys, check internet |
| **Wrong recommendations** | Market conditions changed, re-analyze |
| **Want to stop** | Press Ctrl+C in terminal |
| **Reset system** | Delete `logs/trades.json`, restart |

---

## 📁 Important Files

| File | Purpose |
|------|---------|
| `main.py` | Dashboard application |
| `config/credentials.json.example` | Your API keys |
| `logs/trades.json` | Trade history |
| `USER_GUIDE.md` | Full documentation |
| `README.md` | Project overview |

---

## 💡 Pro Tips

1. ✅ Always review trade details before approving
2. ✅ Trade during optimal hours for better fills
3. ✅ Start with small position sizes
4. ✅ Keep a trading journal
5. ✅ Review your trades weekly
6. ✅ Don't chase losses
7. ✅ Trust the system but verify
8. ✅ Take breaks to avoid overtrading

---

## 📞 Where to Get Help

1. **Read:** `USER_GUIDE.md` (comprehensive)
2. **Check:** FAQ section in user guide
3. **Review:** Code comments in `modules/`
4. **Test:** Use testnet mode first

---

## 🎓 Learning Path

**Week 1:** Understand basics, read guides, watch in simulation  
**Week 2:** Small trades ($100-500), learn from mistakes  
**Week 3:** Review performance, refine approach  
**Week 4+:** Scale up gradually with confidence

---

## ⚠️ Remember

- Options expire worthless if OTM
- Max loss can occur quickly
- Probability ≠ Guarantee
- Past performance ≠ Future results
- YOU make final decision, not AI
- Only risk what you can afford to lose

---

## 🎯 Success Metrics

Track these weekly:
- [ ] Win rate (target: > 55%)
- [ ] Average profit per trade
- [ ] Max drawdown
- [ ] Sharpe ratio
- [ ] Capital growth rate

---

**Keep this card handy while trading! 📋✅**
