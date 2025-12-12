"""
Main Application - BTCUSDT Options Trading System
Semi-Automated Trading Dashboard with AI Recommendations
"""

import streamlit as st
import pandas as pd
import json
import os
from datetime import datetime, timedelta
import plotly.graph_objects as go
from plotly.subplots import make_subplots

# Import custom modules
import sys
sys.path.append(os.path.dirname(__file__))

from modules.binance_options_api import BinanceOptionsAPI
from modules.options_pricing import OptionsPricing, SpreadPricing
from modules.ai_strategy_analyzer import AIStrategyAnalyzer


# Page configuration
st.set_page_config(
    page_title="BTC Options Trading System",
    page_icon="📈",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS
st.markdown("""
    <style>
    .big-font {
        font-size:30px !important;
        font-weight: bold;
    }
    .metric-card {
        background-color: #f0f2f6;
        padding: 20px;
        border-radius: 10px;
        margin: 10px 0;
    }
    .success-box {
        background-color: #d4edda;
        border: 1px solid #c3e6cb;
        border-radius: 5px;
        padding: 15px;
        margin: 10px 0;
    }
    .warning-box {
        background-color: #fff3cd;
        border: 1px solid #ffeaa7;
        border-radius: 5px;
        padding: 15px;
        margin: 10px 0;
    }
    .danger-box {
        background-color: #f8d7da;
        border: 1px solid #f5c6cb;
        border-radius: 5px;
        padding: 15px;
        margin: 10px 0;
    }
    </style>
    """, unsafe_allow_html=True)


class TradingDashboard:
    """Main trading dashboard application"""
    
    def __init__(self):
        self.config_path = 'config/credentials.json.example'
        self.load_config()
        self.initialize_components()
    
    def load_config(self):
        """Load configuration from JSON file"""
        try:
            with open(self.config_path, 'r') as f:
                self.config = json.load(f)
        except Exception as e:
            st.error(f"Error loading configuration: {e}")
            self.config = {}
    
    def initialize_components(self):
        """Initialize API and analysis components"""
        try:
            self.api = BinanceOptionsAPI(
                self.config['binance']['api_key'],
                self.config['binance']['api_secret'],
                self.config['binance']['testnet']
            )
            self.pricer = OptionsPricing()
            self.spread_pricer = SpreadPricing(self.pricer)
            self.analyzer = AIStrategyAnalyzer()
            
            # Initialize session state
            if 'trades' not in st.session_state:
                st.session_state.trades = []
            if 'last_analysis' not in st.session_state:
                st.session_state.last_analysis = None
                
        except Exception as e:
            st.error(f"Error initializing components: {e}")
    
    def fetch_market_data(self):
        """Fetch current market data"""
        try:
            # Get spot price
            btc_price = self.api.get_btc_spot_price()
            
            # Get historical data
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
            st.error(f"Error fetching market data: {e}")
            return None, None, None
    
    def run_analysis(self, price_data, volatility, capital):
        """Run AI analysis and get recommendations"""
        try:
            analysis = self.analyzer.analyze_and_recommend(
                price_data, 
                volatility, 
                capital
            )
            st.session_state.last_analysis = analysis
            return analysis
        except Exception as e:
            st.error(f"Error running analysis: {e}")
            return None
    
    def display_market_overview(self, btc_price, volatility):
        """Display market overview section"""
        st.header("📊 Market Overview")
        
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            st.metric(
                label="BTC/USDT Price",
                value=f"${btc_price:,.2f}" if btc_price else "N/A",
                delta=None
            )
        
        with col2:
            st.metric(
                label="30-Day Volatility",
                value=f"{volatility:.2%}" if volatility else "N/A",
                delta=None
            )
        
        with col3:
            current_time = datetime.utcnow()
            st.metric(
                label="Current Time (UTC)",
                value=current_time.strftime("%H:%M:%S"),
                delta=None
            )
        
        with col4:
            # Market status
            hour = current_time.hour
            if hour in [8, 9, 10, 14, 15, 16]:
                status = "🟢 Optimal"
            elif hour in [7, 11, 13, 17]:
                status = "🟡 Good"
            else:
                status = "🟠 Fair"
            st.metric(
                label="Trading Window",
                value=status,
                delta=None
            )
    
    def display_price_chart(self, price_data):
        """Display price chart"""
        if price_data is None or len(price_data) == 0:
            st.warning("No price data available")
            return
        
        fig = make_subplots(
            rows=2, cols=1,
            shared_xaxes=True,
            vertical_spacing=0.03,
            row_heights=[0.7, 0.3]
        )
        
        # Candlestick chart
        fig.add_trace(
            go.Candlestick(
                x=price_data['timestamp'],
                open=price_data['open'],
                high=price_data['high'],
                low=price_data['low'],
                close=price_data['close'],
                name='BTC/USDT'
            ),
            row=1, col=1
        )
        
        # Volume
        fig.add_trace(
            go.Bar(x=price_data['timestamp'], y=price_data['volume'], name='Volume'),
            row=2, col=1
        )
        
        fig.update_layout(
            title='BTC/USDT Price Chart (1H)',
            xaxis_title='Time',
            yaxis_title='Price (USDT)',
            height=600,
            showlegend=False
        )
        
        st.plotly_chart(fig, use_container_width=True)
    
    def display_analysis_results(self, analysis):
        """Display AI analysis results"""
        if not analysis:
            st.warning("Run analysis first to see recommendations")
            return
        
        st.header("🤖 AI Analysis & Recommendations")
        
        # Market regime
        regime = analysis['market_analysis']['regime']
        confidence = analysis['market_analysis']['confidence']
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.subheader("Market Regime")
            regime_color = {
                'ranging': '🟦',
                'bullish_trend': '🟢',
                'bearish_trend': '🔴',
                'high_volatility': '🟡'
            }
            st.markdown(f"### {regime_color.get(regime, '⚪')} {regime.replace('_', ' ').title()}")
            st.progress(confidence)
            st.caption(f"Confidence: {confidence:.1%}")
        
        with col2:
            st.subheader("Recommended Strategy")
            strategy = analysis['strategy_recommendation']['recommended_strategy']
            st.markdown(f"### 📈 {strategy.replace('_', ' ').title()}")
            st.write(analysis['strategy_recommendation']['description'])
        
        # Key metrics
        st.subheader("Strategy Metrics")
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            pop = analysis['probability_of_profit']
            st.metric("Probability of Profit", f"{pop:.1%}")
        
        with col2:
            win_rate = analysis['strategy_recommendation']['expected_win_rate']
            st.metric("Expected Win Rate", f"{win_rate:.1%}")
        
        with col3:
            max_risk = analysis['strategy_recommendation']['trade_parameters'].get('max_risk', 0)
            st.metric("Max Risk", f"${max_risk:.2f}")
        
        with col4:
            contracts = analysis['strategy_recommendation']['trade_parameters'].get('contracts', 1)
            st.metric("Contracts", contracts)
        
        # Summary
        st.markdown("---")
        st.subheader("📝 Analysis Summary")
        st.text(analysis['summary'])
        
        # Trade parameters
        with st.expander("🔧 Detailed Trade Parameters"):
            st.json(analysis['strategy_recommendation']['trade_parameters'])
        
        # Risk assessment
        with st.expander("⚠️ Risk Assessment"):
            risk = analysis['risk_assessment']
            risk_color = {'low': 'success', 'medium': 'warning', 'high': 'danger'}
            st.markdown(f"**Risk Level:** :{risk_color[risk['risk_level']]}-box[{risk['risk_level'].upper()}]")
            st.write(f"**Max Loss:** ${risk['max_loss']:.2f} ({risk['max_loss_pct']:.1f}% of capital)")
            st.write(f"**Position Size:** {risk['recommended_position_size']}")
            st.write(f"**Stop Loss:** {risk['stop_loss_recommendation']}")
            st.write(f"**Diversification:** {risk['diversification']}")
        
        # Timing
        with st.expander("⏰ Timing Recommendation"):
            timing = analysis['timing_recommendation']
            st.write(f"**Current Time:** {timing['current_time_utc']}")
            st.write(f"**Timing Score:** {timing['timing_score'].upper()}")
            st.write(f"**Next Optimal Window:** {timing['next_optimal_window']}")
            st.write(f"**Recommended Hours (UTC):** {', '.join([f'{h:02d}:00' for h in timing['recommended_hours_utc']])}")
            st.info(timing['reason'])
    
    def display_trade_approval(self, analysis):
        """Display trade approval interface"""
        if not analysis:
            return
        
        st.header("✅ Trade Approval")
        
        st.markdown('<div class="warning-box">', unsafe_allow_html=True)
        st.warning("⚠️ **IMPORTANT:** Review all details carefully before approving the trade.")
        st.markdown('</div>', unsafe_allow_html=True)
        
        col1, col2, col3 = st.columns(3)
        
        with col1:
            if st.button("✅ APPROVE TRADE", type="primary", use_container_width=True):
                self.execute_trade(analysis)
        
        with col2:
            if st.button("❌ REJECT TRADE", use_container_width=True):
                st.info("Trade rejected. No action taken.")
        
        with col3:
            if st.button("🔄 RE-ANALYZE", use_container_width=True):
                st.session_state.last_analysis = None
                st.rerun()
    
    def execute_trade(self, analysis):
        """Execute the approved trade"""
        try:
            st.markdown('<div class="success-box">', unsafe_allow_html=True)
            st.success("🎯 Trade execution initiated...")
            
            # In production, this would place actual orders via Binance API
            # For now, we'll simulate and log the trade
            
            trade_record = {
                'timestamp': datetime.now().isoformat(),
                'strategy': analysis['strategy_recommendation']['recommended_strategy'],
                'parameters': analysis['strategy_recommendation']['trade_parameters'],
                'probability_of_profit': analysis['probability_of_profit'],
                'status': 'SIMULATED',  # Change to 'EXECUTED' in production
                'note': 'This is a simulation. Connect to live trading to execute real orders.'
            }
            
            st.session_state.trades.append(trade_record)
            
            st.success("✅ Trade recorded successfully!")
            st.json(trade_record)
            
            st.markdown('</div>', unsafe_allow_html=True)
            
            # Save trade log
            self.save_trade_log(trade_record)
            
        except Exception as e:
            st.error(f"Error executing trade: {e}")
    
    def save_trade_log(self, trade):
        """Save trade to log file"""
        try:
            log_file = 'logs/trades.json'
            os.makedirs('logs', exist_ok=True)
            
            # Load existing trades
            if os.path.exists(log_file):
                with open(log_file, 'r') as f:
                    trades = json.load(f)
            else:
                trades = []
            
            trades.append(trade)
            
            # Save updated trades
            with open(log_file, 'w') as f:
                json.dump(trades, f, indent=2)
                
        except Exception as e:
            st.error(f"Error saving trade log: {e}")
    
    def display_trade_history(self):
        """Display trade history"""
        st.header("📜 Trade History")
        
        if not st.session_state.trades:
            st.info("No trades recorded yet.")
            return
        
        df = pd.DataFrame(st.session_state.trades)
        st.dataframe(df, use_container_width=True)
    
    def run(self):
        """Main application loop"""
        st.title("📈 BTCUSDT Options Trading System")
        st.markdown("**AI-Powered Semi-Automated Options Trading with Manual Approval**")
        st.markdown("---")
        
        # Sidebar
        with st.sidebar:
            st.header("⚙️ Settings")
            
            capital = st.number_input(
                "Trading Capital (USDT)",
                min_value=100,
                max_value=100000,
                value=self.config.get('trading_config', {}).get('default_capital', 5000),
                step=100
            )
            
            st.markdown("---")
            
            if st.button("🔄 Refresh Data", use_container_width=True):
                st.rerun()
            
            if st.button("🤖 Run Analysis", type="primary", use_container_width=True):
                st.session_state.run_analysis = True
            
            st.markdown("---")
            st.caption("⚠️ **Risk Warning:** Options trading involves significant risk. Never invest more than you can afford to lose.")
        
        # Fetch market data
        btc_price, price_data, volatility = self.fetch_market_data()
        
        # Display market overview
        if btc_price:
            self.display_market_overview(btc_price, volatility)
            st.markdown("---")
        
        # Display price chart
        if price_data is not None:
            self.display_price_chart(price_data)
            st.markdown("---")
        
        # Run analysis if requested
        if st.session_state.get('run_analysis', False) or st.session_state.last_analysis:
            if price_data is not None and volatility:
                if not st.session_state.last_analysis:
                    with st.spinner("🤖 Running AI analysis..."):
                        analysis = self.run_analysis(price_data, volatility, capital)
                else:
                    analysis = st.session_state.last_analysis
                
                if analysis:
                    self.display_analysis_results(analysis)
                    st.markdown("---")
                    self.display_trade_approval(analysis)
            
            st.session_state.run_analysis = False
        
        # Trade history
        st.markdown("---")
        self.display_trade_history()


def main():
    """Main entry point"""
    try:
        dashboard = TradingDashboard()
        dashboard.run()
    except Exception as e:
        st.error(f"Application Error: {e}")
        st.info("Please check your configuration and try again.")


if __name__ == "__main__":
    main()
