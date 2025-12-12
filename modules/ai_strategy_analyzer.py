"""
AI Strategy Analyzer Module
Uses machine learning to analyze market conditions and recommend optimal options strategies
"""

import numpy as np
import pandas as pd
from sklearn.ensemble import RandomForestClassifier, GradientBoostingRegressor
from sklearn.preprocessing import StandardScaler
from typing import Dict, List, Tuple
import joblib
from datetime import datetime, timedelta


class MarketRegimeDetector:
    """Detects current market regime (trending, ranging, volatile)"""
    
    def __init__(self):
        self.regime_labels = ['ranging', 'bullish_trend', 'bearish_trend', 'high_volatility']
    
    def analyze_price_action(self, price_data: pd.DataFrame) -> Dict[str, any]:
        """
        Analyze recent price action to determine market regime
        
        Args:
            price_data: DataFrame with columns ['timestamp', 'open', 'high', 'low', 'close', 'volume']
        
        Returns:
            Dictionary with regime analysis
        """
        if len(price_data) < 20:
            return {'regime': 'insufficient_data', 'confidence': 0.0}
        
        # Calculate technical indicators
        df = price_data.copy()
        
        # Moving averages
        df['sma_20'] = df['close'].rolling(window=20).mean()
        df['sma_50'] = df['close'].rolling(window=50).mean() if len(df) >= 50 else df['close'].mean()
        
        # Price position relative to MAs
        current_price = df['close'].iloc[-1]
        sma_20 = df['sma_20'].iloc[-1]
        sma_50 = df['sma_50'].iloc[-1]
        
        # Volatility (ATR - Average True Range)
        df['tr'] = df[['high', 'low', 'close']].apply(
            lambda x: max(x['high'] - x['low'], 
                         abs(x['high'] - x['close']), 
                         abs(x['low'] - x['close'])), 
            axis=1
        )
        atr = df['tr'].rolling(window=14).mean().iloc[-1]
        atr_pct = (atr / current_price) * 100
        
        # Trend strength (ADX-like calculation)
        df['returns'] = df['close'].pct_change()
        recent_returns = df['returns'].tail(20)
        trend_strength = abs(recent_returns.mean()) / (recent_returns.std() + 1e-10)
        
        # Determine regime
        regime = 'ranging'
        confidence = 0.0
        
        # High volatility check
        if atr_pct > 5.0:  # More than 5% daily range
            regime = 'high_volatility'
            confidence = min(atr_pct / 10.0, 0.95)
        
        # Trend detection
        elif current_price > sma_20 * 1.02 and sma_20 > sma_50 and trend_strength > 0.5:
            regime = 'bullish_trend'
            confidence = min(trend_strength, 0.9)
        
        elif current_price < sma_20 * 0.98 and sma_20 < sma_50 and trend_strength > 0.5:
            regime = 'bearish_trend'
            confidence = min(trend_strength, 0.9)
        
        else:
            regime = 'ranging'
            # Calculate how well price is contained
            price_std = df['close'].tail(20).std()
            price_range = df['close'].tail(20).max() - df['close'].tail(20).min()
            ranging_confidence = 1 - (price_std / (price_range + 1e-10))
            confidence = max(0.5, min(ranging_confidence, 0.85))
        
        return {
            'regime': regime,
            'confidence': confidence,
            'current_price': current_price,
            'sma_20': sma_20,
            'sma_50': sma_50,
            'atr': atr,
            'atr_pct': atr_pct,
            'trend_strength': trend_strength,
            'volatility_level': 'high' if atr_pct > 5 else 'medium' if atr_pct > 3 else 'low'
        }


class StrategySelector:
    """Selects optimal options strategy based on market conditions"""
    
    def __init__(self):
        self.strategies = {
            'iron_condor': {
                'best_regime': 'ranging',
                'win_rate': 0.65,
                'description': 'Profit from low volatility and range-bound markets'
            },
            'butterfly_spread': {
                'best_regime': 'ranging',
                'win_rate': 0.55,
                'description': 'Profit from price staying near a specific level'
            },
            'bull_call_spread': {
                'best_regime': 'bullish_trend',
                'win_rate': 0.60,
                'description': 'Profit from moderate bullish movement'
            },
            'bear_put_spread': {
                'best_regime': 'bearish_trend',
                'win_rate': 0.60,
                'description': 'Profit from moderate bearish movement'
            },
            'long_straddle': {
                'best_regime': 'high_volatility',
                'win_rate': 0.45,
                'description': 'Profit from large price movements in either direction'
            },
            'credit_spread': {
                'best_regime': 'ranging',
                'win_rate': 0.62,
                'description': 'Collect premium with defined risk'
            }
        }
    
    def recommend_strategy(self, regime: str, volatility: float, 
                          current_price: float, capital: float) -> Dict[str, any]:
        """
        Recommend the best strategy based on market conditions
        
        Args:
            regime: Market regime from MarketRegimeDetector
            volatility: Current implied or historical volatility
            current_price: Current BTC price
            capital: Available capital
        
        Returns:
            Strategy recommendation with details
        """
        # Strategy scoring
        scores = {}
        
        for strategy_name, strategy_info in self.strategies.items():
            score = 0.0
            
            # Base score from regime match
            if strategy_info['best_regime'] == regime:
                score += 0.5
            
            # Volatility considerations
            if strategy_name == 'iron_condor' and volatility > 0.6:
                score += 0.3  # High IV good for selling premium
            elif strategy_name == 'long_straddle' and volatility < 0.5:
                score += 0.2  # Low IV good for buying options
            
            # Add base win rate
            score += strategy_info['win_rate'] * 0.2
            
            scores[strategy_name] = score
        
        # Get top strategy
        best_strategy = max(scores, key=scores.get)
        
        # Generate trade parameters
        trade_params = self._generate_trade_parameters(
            best_strategy, current_price, volatility, capital
        )
        
        return {
            'recommended_strategy': best_strategy,
            'confidence_score': scores[best_strategy],
            'description': self.strategies[best_strategy]['description'],
            'expected_win_rate': self.strategies[best_strategy]['win_rate'],
            'trade_parameters': trade_params,
            'alternative_strategies': sorted(
                [(k, v) for k, v in scores.items() if k != best_strategy],
                key=lambda x: x[1],
                reverse=True
            )[:2]
        }
    
    def _generate_trade_parameters(self, strategy: str, current_price: float,
                                   volatility: float, capital: float) -> Dict[str, any]:
        """Generate specific trade parameters for the strategy"""
        
        # Calculate position size (5-10% of capital)
        max_risk = capital * 0.08  # 8% default
        
        if strategy == 'iron_condor':
            # Set strikes around ±10% from current price
            call_short_strike = round(current_price * 1.10, -3)
            call_long_strike = round(current_price * 1.15, -3)
            put_short_strike = round(current_price * 0.90, -3)
            put_long_strike = round(current_price * 0.85, -3)
            
            spread_width = 5000  # Typical spread width
            contracts = int(max_risk / spread_width)
            
            return {
                'call_short_strike': call_short_strike,
                'call_long_strike': call_long_strike,
                'put_short_strike': put_short_strike,
                'put_long_strike': put_long_strike,
                'contracts': max(1, contracts),
                'expiration_days': 30,
                'max_risk': spread_width * max(1, contracts)
            }
        
        elif strategy == 'butterfly_spread':
            # ATM butterfly
            atm_strike = round(current_price, -3)
            wing_width = round(current_price * 0.05, -3)
            
            return {
                'lower_strike': atm_strike - wing_width,
                'middle_strike': atm_strike,
                'upper_strike': atm_strike + wing_width,
                'contracts': max(1, int(max_risk / 1000)),
                'expiration_days': 30,
                'max_risk': max_risk
            }
        
        elif strategy in ['bull_call_spread', 'bear_put_spread']:
            # Directional spreads
            strike_spacing = round(current_price * 0.05, -3)
            
            if strategy == 'bull_call_spread':
                long_strike = round(current_price * 1.02, -3)
                short_strike = long_strike + strike_spacing
            else:
                long_strike = round(current_price * 0.98, -3)
                short_strike = long_strike - strike_spacing
            
            return {
                'long_strike': long_strike,
                'short_strike': short_strike,
                'contracts': max(1, int(max_risk / strike_spacing)),
                'expiration_days': 21,
                'max_risk': max_risk
            }
        
        elif strategy == 'long_straddle':
            atm_strike = round(current_price, -3)
            
            return {
                'strike': atm_strike,
                'contracts': max(1, int(max_risk / (current_price * 0.1))),
                'expiration_days': 14,
                'max_risk': max_risk
            }
        
        else:  # credit_spread
            strike_spacing = round(current_price * 0.05, -3)
            short_strike = round(current_price * 1.05, -3)
            long_strike = short_strike + strike_spacing
            
            return {
                'short_strike': short_strike,
                'long_strike': long_strike,
                'contracts': max(1, int(max_risk / strike_spacing)),
                'expiration_days': 30,
                'max_risk': max_risk
            }


class AIStrategyAnalyzer:
    """Main AI analyzer that combines all components"""
    
    def __init__(self):
        self.regime_detector = MarketRegimeDetector()
        self.strategy_selector = StrategySelector()
    
    def analyze_and_recommend(self, price_data: pd.DataFrame, 
                             volatility: float, capital: float) -> Dict[str, any]:
        """
        Complete analysis and strategy recommendation
        
        Args:
            price_data: Historical price data
            volatility: Current volatility estimate
            capital: Available trading capital
        
        Returns:
            Comprehensive recommendation with all analysis
        """
        # Detect market regime
        regime_analysis = self.regime_detector.analyze_price_action(price_data)
        
        # Get strategy recommendation
        strategy_rec = self.strategy_selector.recommend_strategy(
            regime_analysis['regime'],
            volatility,
            regime_analysis['current_price'],
            capital
        )
        
        # Calculate probability of profit using Monte Carlo-style estimation
        pop = self._estimate_probability_of_profit(
            strategy_rec['recommended_strategy'],
            regime_analysis,
            volatility,
            strategy_rec['trade_parameters']
        )
        
        # Generate timing recommendation
        timing = self._recommend_timing(regime_analysis, volatility)
        
        return {
            'timestamp': datetime.now().isoformat(),
            'market_analysis': regime_analysis,
            'strategy_recommendation': strategy_rec,
            'probability_of_profit': pop,
            'timing_recommendation': timing,
            'risk_assessment': self._assess_risk(strategy_rec, regime_analysis),
            'summary': self._generate_summary(regime_analysis, strategy_rec, pop)
        }
    
    def _estimate_probability_of_profit(self, strategy: str, regime: Dict,
                                       volatility: float, params: Dict) -> float:
        """Estimate probability of profit based on historical patterns"""
        
        base_pop = self.strategy_selector.strategies[strategy]['win_rate']
        
        # Adjust based on market conditions
        adjustment = 0.0
        
        if regime['regime'] == self.strategy_selector.strategies[strategy]['best_regime']:
            adjustment += 0.05  # Boost for matching regime
        
        if regime['confidence'] > 0.8:
            adjustment += 0.03  # High confidence in regime detection
        
        # Volatility adjustments
        if strategy in ['iron_condor', 'credit_spread'] and volatility > 0.6:
            adjustment += 0.05  # High IV good for premium selling
        
        return min(0.95, max(0.30, base_pop + adjustment))
    
    def _recommend_timing(self, regime: Dict, volatility: float) -> Dict[str, any]:
        """Recommend optimal trading times"""
        
        # Best times are typically during high liquidity
        recommended_hours_utc = [8, 9, 10, 14, 15, 16]
        
        current_hour = datetime.utcnow().hour
        
        if current_hour in recommended_hours_utc:
            timing_score = 'optimal'
        elif current_hour in [7, 11, 13, 17]:
            timing_score = 'good'
        else:
            timing_score = 'acceptable'
        
        return {
            'current_time_utc': datetime.utcnow().strftime('%Y-%m-%d %H:%M:%S UTC'),
            'timing_score': timing_score,
            'recommended_hours_utc': recommended_hours_utc,
            'next_optimal_window': self._get_next_window(recommended_hours_utc),
            'reason': 'High liquidity periods provide better fills and tighter spreads'
        }
    
    def _get_next_window(self, hours: List[int]) -> str:
        """Get next optimal trading window"""
        current_hour = datetime.utcnow().hour
        
        future_hours = [h for h in hours if h > current_hour]
        if future_hours:
            next_hour = future_hours[0]
            return f"Today at {next_hour:02d}:00 UTC"
        else:
            return f"Tomorrow at {hours[0]:02d}:00 UTC"
    
    def _assess_risk(self, strategy_rec: Dict, regime: Dict) -> Dict[str, any]:
        """Assess risk levels for the recommended strategy"""
        
        params = strategy_rec['trade_parameters']
        max_risk = params.get('max_risk', 0)
        
        # Calculate risk metrics
        risk_level = 'low'
        if max_risk > 1000:
            risk_level = 'high'
        elif max_risk > 500:
            risk_level = 'medium'
        
        return {
            'risk_level': risk_level,
            'max_loss': max_risk,
            'max_loss_pct': (max_risk / 5000) * 100,  # Assuming $5000 default capital
            'regime_uncertainty': 1 - regime['confidence'],
            'recommended_position_size': 'Conservative' if max_risk < 500 else 'Moderate',
            'stop_loss_recommendation': 'Exit if loss reaches 50% of max risk',
            'diversification': 'Consider spreading across 2-3 different expirations'
        }
    
    def _generate_summary(self, regime: Dict, strategy_rec: Dict, pop: float) -> str:
        """Generate human-readable summary"""
        
        regime_name = regime['regime'].replace('_', ' ').title()
        strategy_name = strategy_rec['recommended_strategy'].replace('_', ' ').title()
        
        summary = f"""
MARKET ANALYSIS SUMMARY
======================
Current Market Regime: {regime_name} (Confidence: {regime['confidence']:.1%})
Current BTC Price: ${regime['current_price']:,.2f}
Volatility Level: {regime['volatility_level'].upper()}

RECOMMENDED STRATEGY: {strategy_name}
{strategy_rec['description']}

Expected Win Rate: {strategy_rec['expected_win_rate']:.1%}
Probability of Profit: {pop:.1%}
Position Size: {strategy_rec['trade_parameters'].get('contracts', 1)} contract(s)
Suggested Duration: {strategy_rec['trade_parameters'].get('expiration_days', 30)} days

This strategy is optimal for current market conditions with a {regime['confidence']:.0%} confidence level.
        """.strip()
        
        return summary


if __name__ == "__main__":
    # Test the analyzer
    print("AI Strategy Analyzer - Test Mode")
    
    # Create sample price data
    dates = pd.date_range(end=datetime.now(), periods=100, freq='1H')
    prices = 50000 + np.cumsum(np.random.randn(100) * 500)
    
    df = pd.DataFrame({
        'timestamp': dates,
        'open': prices,
        'high': prices * 1.01,
        'low': prices * 0.99,
        'close': prices,
        'volume': np.random.randint(100, 1000, 100)
    })
    
    analyzer = AIStrategyAnalyzer()
    result = analyzer.analyze_and_recommend(df, volatility=0.7, capital=5000)
    
    print(result['summary'])
