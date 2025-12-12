"""
Options Pricing and Greeks Calculation Module
Implements Black-Scholes model and Monte Carlo simulations
"""

import numpy as np
from scipy.stats import norm
from typing import Dict, Tuple
import math


class OptionsPricing:
    """Options pricing and Greeks calculator using Black-Scholes model"""
    
    def __init__(self, risk_free_rate: float = 0.05):
        """
        Initialize options pricing calculator
        
        Args:
            risk_free_rate: Annual risk-free interest rate (default 5%)
        """
        self.risk_free_rate = risk_free_rate
    
    def black_scholes(self, S: float, K: float, T: float, r: float, 
                     sigma: float, option_type: str = 'call') -> float:
        """
        Calculate option price using Black-Scholes formula
        
        Args:
            S: Current spot price
            K: Strike price
            T: Time to expiration (in years)
            r: Risk-free rate
            sigma: Volatility (annualized)
            option_type: 'call' or 'put'
        
        Returns:
            Option price
        """
        if T <= 0:
            # Option has expired
            if option_type.lower() == 'call':
                return max(S - K, 0)
            else:
                return max(K - S, 0)
        
        d1 = (math.log(S / K) + (r + 0.5 * sigma ** 2) * T) / (sigma * math.sqrt(T))
        d2 = d1 - sigma * math.sqrt(T)
        
        if option_type.lower() == 'call':
            price = S * norm.cdf(d1) - K * math.exp(-r * T) * norm.cdf(d2)
        else:  # put
            price = K * math.exp(-r * T) * norm.cdf(-d2) - S * norm.cdf(-d1)
        
        return price
    
    def calculate_greeks(self, S: float, K: float, T: float, r: float, 
                        sigma: float, option_type: str = 'call') -> Dict[str, float]:
        """
        Calculate option Greeks
        
        Returns:
            Dictionary containing Delta, Gamma, Theta, Vega, Rho
        """
        if T <= 0:
            return {
                'delta': 0.0,
                'gamma': 0.0,
                'theta': 0.0,
                'vega': 0.0,
                'rho': 0.0
            }
        
        d1 = (math.log(S / K) + (r + 0.5 * sigma ** 2) * T) / (sigma * math.sqrt(T))
        d2 = d1 - sigma * math.sqrt(T)
        
        # Delta
        if option_type.lower() == 'call':
            delta = norm.cdf(d1)
        else:
            delta = -norm.cdf(-d1)
        
        # Gamma (same for calls and puts)
        gamma = norm.pdf(d1) / (S * sigma * math.sqrt(T))
        
        # Theta
        term1 = -(S * norm.pdf(d1) * sigma) / (2 * math.sqrt(T))
        if option_type.lower() == 'call':
            term2 = r * K * math.exp(-r * T) * norm.cdf(d2)
            theta = (term1 - term2) / 365  # Daily theta
        else:
            term2 = r * K * math.exp(-r * T) * norm.cdf(-d2)
            theta = (term1 + term2) / 365  # Daily theta
        
        # Vega (same for calls and puts)
        vega = S * norm.pdf(d1) * math.sqrt(T) / 100  # Per 1% change in volatility
        
        # Rho
        if option_type.lower() == 'call':
            rho = K * T * math.exp(-r * T) * norm.cdf(d2) / 100
        else:
            rho = -K * T * math.exp(-r * T) * norm.cdf(-d2) / 100
        
        return {
            'delta': delta,
            'gamma': gamma,
            'theta': theta,
            'vega': vega,
            'rho': rho
        }
    
    def calculate_implied_volatility(self, S: float, K: float, T: float, r: float,
                                    market_price: float, option_type: str = 'call',
                                    max_iterations: int = 100, tolerance: float = 1e-5) -> float:
        """
        Calculate implied volatility using Newton-Raphson method
        
        Args:
            market_price: Current market price of the option
            
        Returns:
            Implied volatility
        """
        # Initial guess
        sigma = 0.5
        
        for i in range(max_iterations):
            price = self.black_scholes(S, K, T, r, sigma, option_type)
            diff = market_price - price
            
            if abs(diff) < tolerance:
                return sigma
            
            # Calculate vega for Newton-Raphson
            vega = S * norm.pdf((math.log(S/K) + (r + 0.5*sigma**2)*T) / (sigma*math.sqrt(T))) * math.sqrt(T)
            
            if vega < 1e-10:  # Avoid division by very small numbers
                break
            
            sigma = sigma + diff / vega
            
            # Keep sigma within reasonable bounds
            sigma = max(0.01, min(sigma, 5.0))
        
        return sigma
    
    def monte_carlo_simulation(self, S: float, K: float, T: float, r: float,
                              sigma: float, option_type: str = 'call',
                              num_simulations: int = 10000) -> Dict[str, float]:
        """
        Run Monte Carlo simulation for option pricing
        
        Returns:
            Dictionary with price, confidence intervals, and probability of profit
        """
        dt = T / 365  # Daily time step
        num_steps = int(T * 365)
        
        # Generate random price paths
        Z = np.random.standard_normal((num_simulations, num_steps))
        
        # Initialize price paths
        S_t = np.zeros((num_simulations, num_steps + 1))
        S_t[:, 0] = S
        
        # Generate price paths using geometric Brownian motion
        for t in range(1, num_steps + 1):
            S_t[:, t] = S_t[:, t-1] * np.exp((r - 0.5 * sigma**2) * dt + 
                                              sigma * np.sqrt(dt) * Z[:, t-1])
        
        # Calculate payoffs at expiration
        final_prices = S_t[:, -1]
        
        if option_type.lower() == 'call':
            payoffs = np.maximum(final_prices - K, 0)
        else:
            payoffs = np.maximum(K - final_prices, 0)
        
        # Discount payoffs to present value
        option_price = np.exp(-r * T) * np.mean(payoffs)
        
        # Calculate confidence intervals
        std_error = np.std(payoffs) / np.sqrt(num_simulations)
        confidence_95 = 1.96 * std_error * np.exp(-r * T)
        
        # Calculate probability of profit
        profitable_paths = np.sum(payoffs > 0)
        probability_of_profit = profitable_paths / num_simulations
        
        return {
            'price': option_price,
            'confidence_interval_lower': option_price - confidence_95,
            'confidence_interval_upper': option_price + confidence_95,
            'probability_of_profit': probability_of_profit,
            'expected_payoff': np.mean(payoffs),
            'max_payoff': np.max(payoffs),
            'min_payoff': np.min(payoffs),
        }
    
    def calculate_probability_itm(self, S: float, K: float, T: float, 
                                 sigma: float, option_type: str = 'call') -> float:
        """
        Calculate probability that option will be in-the-money at expiration
        
        Returns:
            Probability (0 to 1)
        """
        if T <= 0:
            if option_type.lower() == 'call':
                return 1.0 if S > K else 0.0
            else:
                return 1.0 if S < K else 0.0
        
        # Log-normal distribution
        d2 = (math.log(S / K) + (self.risk_free_rate - 0.5 * sigma ** 2) * T) / (sigma * math.sqrt(T))
        
        if option_type.lower() == 'call':
            prob_itm = norm.cdf(d2)
        else:
            prob_itm = norm.cdf(-d2)
        
        return prob_itm
    
    def calculate_break_even(self, S: float, K: float, premium: float,
                            option_type: str = 'call') -> float:
        """
        Calculate break-even price at expiration
        
        Args:
            premium: Option premium paid
            
        Returns:
            Break-even spot price
        """
        if option_type.lower() == 'call':
            return K + premium
        else:
            return K - premium


class SpreadPricing:
    """Pricing for option spreads and complex strategies"""
    
    def __init__(self, pricer: OptionsPricing):
        self.pricer = pricer
    
    def iron_condor(self, S: float, K_call_short: float, K_call_long: float,
                   K_put_short: float, K_put_long: float, T: float, r: float,
                   sigma: float) -> Dict[str, float]:
        """
        Price an Iron Condor strategy
        
        Args:
            K_call_short: Short call strike
            K_call_long: Long call strike (higher)
            K_put_short: Short put strike
            K_put_long: Long put strike (lower)
        
        Returns:
            Strategy metrics
        """
        # Calculate individual option prices
        short_call_price = self.pricer.black_scholes(S, K_call_short, T, r, sigma, 'call')
        long_call_price = self.pricer.black_scholes(S, K_call_long, T, r, sigma, 'call')
        short_put_price = self.pricer.black_scholes(S, K_put_short, T, r, sigma, 'put')
        long_put_price = self.pricer.black_scholes(S, K_put_long, T, r, sigma, 'put')
        
        # Net credit received (premium collected)
        net_credit = (short_call_price + short_put_price) - (long_call_price + long_put_price)
        
        # Max profit is the net credit
        max_profit = net_credit
        
        # Max loss
        call_spread_width = K_call_long - K_call_short
        put_spread_width = K_put_short - K_put_long
        max_loss = max(call_spread_width, put_spread_width) - net_credit
        
        # Break-even points
        upper_breakeven = K_call_short + net_credit
        lower_breakeven = K_put_short - net_credit
        
        # Probability of profit (price stays between short strikes)
        prob_below_call = self.pricer.calculate_probability_itm(S, K_call_short, T, sigma, 'put')
        prob_above_put = self.pricer.calculate_probability_itm(S, K_put_short, T, sigma, 'call')
        probability_of_profit = prob_below_call - (1 - prob_above_put)
        
        return {
            'strategy_type': 'Iron Condor',
            'net_credit': net_credit,
            'max_profit': max_profit,
            'max_loss': max_loss,
            'max_profit_pct': (max_profit / max_loss) * 100 if max_loss > 0 else 0,
            'upper_breakeven': upper_breakeven,
            'lower_breakeven': lower_breakeven,
            'probability_of_profit': probability_of_profit,
            'risk_reward_ratio': max_loss / max_profit if max_profit > 0 else float('inf'),
        }
    
    def butterfly_spread(self, S: float, K_lower: float, K_middle: float,
                        K_upper: float, T: float, r: float, sigma: float,
                        option_type: str = 'call') -> Dict[str, float]:
        """
        Price a Butterfly Spread
        
        Returns:
            Strategy metrics
        """
        # Buy 1 lower strike, sell 2 middle strike, buy 1 upper strike
        lower_price = self.pricer.black_scholes(S, K_lower, T, r, sigma, option_type)
        middle_price = self.pricer.black_scholes(S, K_middle, T, r, sigma, option_type)
        upper_price = self.pricer.black_scholes(S, K_upper, T, r, sigma, option_type)
        
        net_debit = lower_price + upper_price - (2 * middle_price)
        
        # Max profit occurs when price is at middle strike at expiration
        max_profit = (K_middle - K_lower) - net_debit
        max_loss = net_debit
        
        # Break-even points
        lower_breakeven = K_lower + net_debit
        upper_breakeven = K_upper - net_debit
        
        return {
            'strategy_type': 'Butterfly Spread',
            'net_debit': net_debit,
            'max_profit': max_profit,
            'max_loss': max_loss,
            'max_profit_pct': (max_profit / max_loss) * 100 if max_loss > 0 else 0,
            'lower_breakeven': lower_breakeven,
            'upper_breakeven': upper_breakeven,
            'probability_of_profit': 0.5,  # Simplified
            'risk_reward_ratio': max_loss / max_profit if max_profit > 0 else float('inf'),
        }


if __name__ == "__main__":
    # Test pricing calculations
    pricer = OptionsPricing()
    
    # Example: BTC at $50,000
    S = 50000
    K = 52000
    T = 30 / 365  # 30 days
    r = 0.05
    sigma = 0.8  # 80% volatility
    
    call_price = pricer.black_scholes(S, K, T, r, sigma, 'call')
    greeks = pricer.calculate_greeks(S, K, T, r, sigma, 'call')
    
    print(f"Call Option Price: ${call_price:.2f}")
    print(f"Delta: {greeks['delta']:.4f}")
    print(f"Gamma: {greeks['gamma']:.6f}")
    print(f"Theta: ${greeks['theta']:.2f} per day")
    print(f"Vega: ${greeks['vega']:.2f} per 1% vol change")
