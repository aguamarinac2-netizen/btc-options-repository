#!/usr/bin/env python3
"""
BTCUSDT Options Trading System - CLI Version
Works directly in terminal without web browser
"""

import json
import os
from datetime import datetime
from modules.binance_options_api import BinanceOptionsAPI
from modules.options_pricing import OptionsPricing, SpreadPricing
from modules.ai_strategy_analyzer import AIStrategyAnalyzer


class TradingCLI:
    """Command-line interface for options trading system"""
    
    def __init__(self):
        self.load_config()
        self.initialize_components()
        
    def load_config(self):
        """Load configuration"""
        config_path = 'config/credentials.json.example'
        with open(config_path, 'r') as f:
            self.config = json.load(f)
            
    def initialize_components(self):
        """Initialize trading components"""
        print("\n🔄 Initializing trading system...")
        
        self.api = BinanceOptionsAPI(
            self.config['binance']['api_key'],
            self.config['binance']['api_secret'],
            self.config['binance']['testnet']
        )
        self.pricer = OptionsPricing()
        self.spread_pricer = SpreadPricing(self.pricer)
        self.analyzer = AIStrategyAnalyzer()
        
        print("✅ System initialized successfully!")
        
    def print_header(self):
        """Print fancy header"""
        print("\n" + "="*70)
        print("   📈 BTCUSDT OPTIONS TRADING SYSTEM - AI POWERED")
        print("="*70)
        
    def fetch_market_data(self):
        """Fetch current market data"""
        print("\n🔍 Fetching market data...")
        
        try:
            # Get spot price
            btc_price = self.api.get_btc_spot_price()
            
            # Get historical data
            import pandas as pd
            ohlcv = self.api.exchange.fetch_ohlcv('BTC/USDT', '1h', limit=100)
            price_data = pd.DataFrame(
                ohlcv, 
                columns=['timestamp', 'open', 'high', 'low', 'close', 'volume']
            )
            price_data['timestamp'] = pd.to_datetime(price_data['timestamp'], unit='ms')
            
            # Calculate volatility
            volatility = self.api.get_historical_volatility()
            
            return btc_price, price_data, volatility
            
        except Exception as e:
            print(f"⚠️  Warning: {e}")
            print("📌 Using simulated data for demonstration...")
            
            # Create simulated data for demo
            import pandas as pd
            import numpy as np
            
            dates = pd.date_range(end=datetime.now(), periods=100, freq='1H')
            prices = 95000 + np.cumsum(np.random.randn(100) * 500)
            
            price_data = pd.DataFrame({
                'timestamp': dates,
                'open': prices,
                'high': prices * 1.01,
                'low': prices * 0.99,
                'close': prices,
                'volume': np.random.randint(100, 1000, 100)
            })
            
            return 95000.0, price_data, 0.65
            
    def display_market_overview(self, btc_price, volatility):
        """Display market overview"""
        print("\n" + "─"*70)
        print("📊 MARKET OVERVIEW")
        print("─"*70)
        
        current_time = datetime.utcnow()
        hour = current_time.hour
        
        if hour in [8, 9, 10, 14, 15, 16]:
            timing_status = "🟢 OPTIMAL"
        elif hour in [7, 11, 13, 17]:
            timing_status = "🟡 GOOD"
        else:
            timing_status = "🟠 FAIR"
            
        print(f"  💰 BTC/USDT Price:     ${btc_price:,.2f}")
        print(f"  📈 30-Day Volatility:  {volatility:.2%}")
        print(f"  🕐 Current Time (UTC): {current_time.strftime('%Y-%m-%d %H:%M:%S')}")
        print(f"  ⏰ Trading Window:     {timing_status}")
        print("─"*70)
        
    def run_analysis(self, price_data, volatility, capital):
        """Run AI analysis"""
        print("\n🤖 Running AI Market Analysis...")
        print("   ⏳ This may take a few seconds...")
        
        try:
            analysis = self.analyzer.analyze_and_recommend(
                price_data, 
                volatility, 
                capital
            )
            return analysis
        except Exception as e:
            print(f"❌ Error during analysis: {e}")
            return None
            
    def display_analysis(self, analysis):
        """Display analysis results"""
        if not analysis:
            print("\n❌ Analysis failed. Please try again.")
            return
            
        print("\n" + "="*70)
        print("🤖 AI ANALYSIS RESULTS")
        print("="*70)
        
        # Market regime
        regime = analysis['market_analysis']['regime']
        confidence = analysis['market_analysis']['confidence']
        
        regime_emoji = {
            'ranging': '🟦',
            'bullish_trend': '🟢',
            'bearish_trend': '🔴',
            'high_volatility': '🟡'
        }
        
        print(f"\n📍 MARKET REGIME: {regime_emoji.get(regime, '⚪')} {regime.replace('_', ' ').upper()}")
        print(f"   Confidence: {confidence:.1%} {'▓' * int(confidence * 20)}{'░' * (20 - int(confidence * 20))}")
        
        # Recommended strategy
        strategy = analysis['strategy_recommendation']['recommended_strategy']
        description = analysis['strategy_recommendation']['description']
        
        print(f"\n💡 RECOMMENDED STRATEGY: {strategy.replace('_', ' ').upper()}")
        print(f"   {description}")
        
        # Key metrics
        print(f"\n📊 KEY METRICS:")
        print(f"   ✓ Probability of Profit:  {analysis['probability_of_profit']:.1%}")
        print(f"   ✓ Expected Win Rate:      {analysis['strategy_recommendation']['expected_win_rate']:.1%}")
        
        max_risk = analysis['strategy_recommendation']['trade_parameters'].get('max_risk', 0)
        contracts = analysis['strategy_recommendation']['trade_parameters'].get('contracts', 1)
        
        print(f"   ✓ Max Risk:               ${max_risk:.2f}")
        print(f"   ✓ Contracts:              {contracts}")
        
        # Trade parameters
        print(f"\n🔧 TRADE PARAMETERS:")
        params = analysis['strategy_recommendation']['trade_parameters']
        
        if strategy == 'iron_condor':
            print(f"   Call Short Strike:  ${params.get('call_short_strike', 0):,.0f}")
            print(f"   Call Long Strike:   ${params.get('call_long_strike', 0):,.0f}")
            print(f"   Put Short Strike:   ${params.get('put_short_strike', 0):,.0f}")
            print(f"   Put Long Strike:    ${params.get('put_long_strike', 0):,.0f}")
        elif strategy == 'butterfly_spread':
            print(f"   Lower Strike:       ${params.get('lower_strike', 0):,.0f}")
            print(f"   Middle Strike:      ${params.get('middle_strike', 0):,.0f}")
            print(f"   Upper Strike:       ${params.get('upper_strike', 0):,.0f}")
        else:
            for key, value in params.items():
                if 'strike' in key.lower():
                    print(f"   {key.replace('_', ' ').title()}: ${value:,.0f}")
                    
        print(f"   Expiration:         {params.get('expiration_days', 0)} days")
        
        # Risk assessment
        risk = analysis['risk_assessment']
        print(f"\n⚠️  RISK ASSESSMENT:")
        
        risk_color = {'low': '🟢', 'medium': '🟡', 'high': '🔴'}
        print(f"   Risk Level:         {risk_color.get(risk['risk_level'], '⚪')} {risk['risk_level'].upper()}")
        print(f"   Max Loss:           ${risk['max_loss']:.2f} ({risk['max_loss_pct']:.1f}% of capital)")
        print(f"   Position Size:      {risk['recommended_position_size']}")
        print(f"   Stop Loss:          {risk['stop_loss_recommendation']}")
        
        # Timing
        timing = analysis['timing_recommendation']
        print(f"\n⏰ TIMING RECOMMENDATION:")
        print(f"   Current Status:     {timing['timing_score'].upper()}")
        print(f"   Next Optimal:       {timing['next_optimal_window']}")
        print(f"   Reason:             {timing['reason']}")
        
        print("\n" + "="*70)
        
    def get_user_decision(self):
        """Get user's trading decision"""
        print("\n" + "─"*70)
        print("TRADE APPROVAL")
        print("─"*70)
        print("\nOptions:")
        print("  [1] ✅ APPROVE TRADE (Execute the recommendation)")
        print("  [2] ❌ REJECT TRADE (Skip this opportunity)")
        print("  [3] 🔄 RE-ANALYZE (Run fresh analysis)")
        print("  [4] 🚪 EXIT (Close the system)")
        
        while True:
            try:
                choice = input("\nYour choice [1-4]: ").strip()
                
                if choice in ['1', '2', '3', '4']:
                    return choice
                else:
                    print("❌ Invalid choice. Please enter 1, 2, 3, or 4.")
            except KeyboardInterrupt:
                print("\n\n👋 Exiting...")
                return '4'
                
    def execute_trade(self, analysis):
        """Log the approved trade"""
        print("\n" + "="*70)
        print("🎯 TRADE EXECUTION")
        print("="*70)
        
        print("\n⚠️  SIMULATION MODE ACTIVE")
        print("    (No real trades will be executed)")
        
        trade_record = {
            'timestamp': datetime.now().isoformat(),
            'strategy': analysis['strategy_recommendation']['recommended_strategy'],
            'parameters': analysis['strategy_recommendation']['trade_parameters'],
            'probability_of_profit': analysis['probability_of_profit'],
            'status': 'SIMULATED',
            'note': 'Trade logged in simulation mode'
        }
        
        # Save to log
        self.save_trade_log(trade_record)
        
        print("\n✅ Trade recorded successfully!")
        print(f"\n📝 Trade Details:")
        print(f"   Strategy:     {trade_record['strategy'].replace('_', ' ').title()}")
        print(f"   Status:       {trade_record['status']}")
        print(f"   Timestamp:    {trade_record['timestamp']}")
        print(f"   Win Chance:   {trade_record['probability_of_profit']:.1%}")
        
        print("\n💾 Trade saved to: logs/trades.json")
        print("="*70)
        
    def save_trade_log(self, trade):
        """Save trade to log file"""
        try:
            log_file = 'logs/trades.json'
            os.makedirs('logs', exist_ok=True)
            
            if os.path.exists(log_file):
                with open(log_file, 'r') as f:
                    trades = json.load(f)
            else:
                trades = []
            
            trades.append(trade)
            
            with open(log_file, 'w') as f:
                json.dump(trades, f, indent=2)
                
        except Exception as e:
            print(f"⚠️  Warning: Could not save trade log: {e}")
            
    def run(self):
        """Main CLI loop"""
        self.print_header()
        
        print("\n⚠️  RISK WARNING:")
        print("    Options trading involves significant risk.")
        print("    Never invest more than you can afford to lose.")
        print("    This system requires YOUR manual approval for all trades.\n")
        
        # Get capital
        while True:
            try:
                capital_input = input("💰 Enter your trading capital in USDT [default: 5000]: ").strip()
                capital = float(capital_input) if capital_input else 5000.0
                
                if capital < 100:
                    print("❌ Minimum capital is $100 USDT")
                    continue
                    
                break
            except ValueError:
                print("❌ Please enter a valid number")
                
        # Main loop
        while True:
            try:
                # Fetch market data
                btc_price, price_data, volatility = self.fetch_market_data()
                
                # Display overview
                self.display_market_overview(btc_price, volatility)
                
                # Run analysis
                analysis = self.run_analysis(price_data, volatility, capital)
                
                if analysis:
                    # Display results
                    self.display_analysis(analysis)
                    
                    # Get user decision
                    choice = self.get_user_decision()
                    
                    if choice == '1':
                        # Approve trade
                        self.execute_trade(analysis)
                        print("\n✓ Press Enter to continue...")
                        input()
                        
                    elif choice == '2':
                        # Reject trade
                        print("\n❌ Trade rejected. No action taken.")
                        print("\n✓ Press Enter to continue...")
                        input()
                        
                    elif choice == '3':
                        # Re-analyze
                        print("\n🔄 Running fresh analysis...")
                        continue
                        
                    elif choice == '4':
                        # Exit
                        print("\n" + "="*70)
                        print("👋 Thank you for using BTCUSDT Options Trading System!")
                        print("   Trade safely and responsibly.")
                        print("="*70 + "\n")
                        break
                else:
                    print("\n❌ Analysis failed. Please try again.")
                    print("\n✓ Press Enter to retry...")
                    input()
                    
            except KeyboardInterrupt:
                print("\n\n" + "="*70)
                print("👋 System interrupted. Exiting safely...")
                print("="*70 + "\n")
                break
            except Exception as e:
                print(f"\n❌ Unexpected error: {e}")
                print("\n✓ Press Enter to continue...")
                input()


def main():
    """Entry point"""
    try:
        cli = TradingCLI()
        cli.run()
    except Exception as e:
        print(f"\n❌ Fatal error: {e}")
        print("Please check your configuration and try again.\n")


if __name__ == "__main__":
    main()
