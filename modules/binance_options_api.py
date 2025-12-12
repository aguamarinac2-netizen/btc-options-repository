"""
Binance Options API Integration Module
Handles all interactions with Binance Options API
"""

import ccxt
import requests
import hmac
import hashlib
import time
from typing import Dict, List, Optional
import pandas as pd
import json


class BinanceOptionsAPI:
    """Wrapper for Binance Options API"""
    
    def __init__(self, api_key: str, api_secret: str, testnet: bool = False):
        self.api_key = api_key
        self.api_secret = api_secret
        self.testnet = testnet
        
        # Binance Options base URLs
        if testnet:
            self.base_url = "https://testnet.binanceops.com"
        else:
            self.base_url = "https://vapi.binance.com"
        
        # Initialize CCXT for spot prices
        self.exchange = ccxt.binance({
            'apiKey': api_key,
            'secret': api_secret,
            'enableRateLimit': True,
        })
        
    def _generate_signature(self, params: Dict) -> str:
        """Generate HMAC SHA256 signature for authenticated requests"""
        query_string = '&'.join([f"{k}={v}" for k, v in params.items()])
        signature = hmac.new(
            self.api_secret.encode('utf-8'),
            query_string.encode('utf-8'),
            hashlib.sha256
        ).hexdigest()
        return signature
    
    def _make_request(self, endpoint: str, method: str = 'GET', params: Dict = None, signed: bool = False) -> Dict:
        """Make HTTP request to Binance Options API"""
        if params is None:
            params = {}
            
        if signed:
            params['timestamp'] = int(time.time() * 1000)
            params['signature'] = self._generate_signature(params)
            
        headers = {
            'X-MBX-APIKEY': self.api_key
        }
        
        url = f"{self.base_url}{endpoint}"
        
        try:
            if method == 'GET':
                response = requests.get(url, params=params, headers=headers, timeout=10)
            elif method == 'POST':
                response = requests.post(url, params=params, headers=headers, timeout=10)
            elif method == 'DELETE':
                response = requests.delete(url, params=params, headers=headers, timeout=10)
            else:
                raise ValueError(f"Unsupported method: {method}")
                
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            print(f"API Request Error: {e}")
            return {}
    
    def get_btc_spot_price(self) -> float:
        """Get current BTC/USDT spot price"""
        try:
            ticker = self.exchange.fetch_ticker('BTC/USDT')
            return ticker['last']
        except Exception as e:
            print(f"Error fetching spot price: {e}")
            return 0.0
    
    def get_exchange_info(self) -> Dict:
        """Get exchange trading rules and symbol information"""
        return self._make_request('/vapi/v1/exchangeInfo')
    
    def get_index_price(self, underlying: str = 'BTCUSDT') -> Dict:
        """Get index price for the underlying asset"""
        return self._make_request('/vapi/v1/index', params={'underlying': underlying})
    
    def get_mark_price(self, symbol: Optional[str] = None) -> List[Dict]:
        """Get mark price for options contracts"""
        params = {}
        if symbol:
            params['symbol'] = symbol
        return self._make_request('/vapi/v1/mark', params=params)
    
    def get_available_options(self) -> pd.DataFrame:
        """Get all available BTCUSDT options contracts"""
        exchange_info = self.get_exchange_info()
        
        if not exchange_info or 'optionSymbols' not in exchange_info:
            return pd.DataFrame()
        
        options_list = []
        for option in exchange_info['optionSymbols']:
            if 'BTC' in option['symbol']:
                options_list.append({
                    'symbol': option['symbol'],
                    'underlying': option.get('underlying', 'BTCUSDT'),
                    'strike': float(option['strikePrice']),
                    'expiry_date': option['expiryDate'],
                    'option_type': 'CALL' if option['side'] == 'CALL' else 'PUT',
                    'contract_id': option.get('id', ''),
                })
        
        return pd.DataFrame(options_list)
    
    def get_option_depth(self, symbol: str, limit: int = 10) -> Dict:
        """Get order book depth for an option contract"""
        return self._make_request('/vapi/v1/depth', params={'symbol': symbol, 'limit': limit})
    
    def get_recent_trades(self, symbol: str, limit: int = 100) -> List[Dict]:
        """Get recent trades for an option contract"""
        return self._make_request('/vapi/v1/trades', params={'symbol': symbol, 'limit': limit})
    
    def get_klines(self, symbol: str, interval: str = '1h', limit: int = 100) -> List[List]:
        """Get kline/candlestick data for options"""
        params = {
            'symbol': symbol,
            'interval': interval,
            'limit': limit
        }
        return self._make_request('/vapi/v1/klines', params=params)
    
    def get_account_info(self) -> Dict:
        """Get account information (requires authentication)"""
        return self._make_request('/vapi/v1/account', signed=True)
    
    def get_positions(self) -> List[Dict]:
        """Get current open positions"""
        return self._make_request('/vapi/v1/position', signed=True)
    
    def place_order(self, symbol: str, side: str, order_type: str, 
                   quantity: float, price: Optional[float] = None) -> Dict:
        """
        Place an options order
        
        Args:
            symbol: Option symbol (e.g., 'BTC-250101-50000-C')
            side: 'BUY' or 'SELL'
            order_type: 'LIMIT' or 'MARKET'
            quantity: Order quantity
            price: Limit price (required for LIMIT orders)
        """
        params = {
            'symbol': symbol,
            'side': side,
            'type': order_type,
            'quantity': quantity,
        }
        
        if order_type == 'LIMIT' and price:
            params['price'] = price
            params['timeInForce'] = 'GTC'
        
        return self._make_request('/vapi/v1/order', method='POST', params=params, signed=True)
    
    def cancel_order(self, symbol: str, order_id: int) -> Dict:
        """Cancel an existing order"""
        params = {
            'symbol': symbol,
            'orderId': order_id,
        }
        return self._make_request('/vapi/v1/order', method='DELETE', params=params, signed=True)
    
    def get_open_orders(self, symbol: Optional[str] = None) -> List[Dict]:
        """Get all open orders"""
        params = {}
        if symbol:
            params['symbol'] = symbol
        return self._make_request('/vapi/v1/openOrders', params=params, signed=True)
    
    def get_historical_volatility(self, underlying: str = 'BTCUSDT', period: int = 30) -> float:
        """
        Calculate historical volatility from spot price data
        
        Args:
            underlying: Underlying asset
            period: Number of days for volatility calculation
        """
        try:
            # Fetch historical OHLCV data
            ohlcv = self.exchange.fetch_ohlcv('BTC/USDT', '1d', limit=period + 1)
            df = pd.DataFrame(ohlcv, columns=['timestamp', 'open', 'high', 'low', 'close', 'volume'])
            
            # Calculate daily returns
            df['returns'] = df['close'].pct_change()
            
            # Calculate annualized volatility
            volatility = df['returns'].std() * (365 ** 0.5)
            
            return volatility
        except Exception as e:
            print(f"Error calculating historical volatility: {e}")
            return 0.5  # Default to 50% volatility
    
    def get_implied_volatility_surface(self) -> pd.DataFrame:
        """
        Get implied volatility surface from available options
        Note: Binance doesn't provide IV directly, would need to calculate from prices
        """
        # This is a placeholder - actual IV calculation would require Black-Scholes inversion
        return pd.DataFrame()


if __name__ == "__main__":
    # Test the API connection
    with open('../config/credentials.json.example', 'r') as f:
        config = json.load(f)
    
    api = BinanceOptionsAPI(
        config['binance']['api_key'],
        config['binance']['api_secret'],
        config['binance']['testnet']
    )
    
    print("Testing Binance Options API...")
    print(f"Current BTC Price: ${api.get_btc_spot_price():.2f}")
    print(f"Historical Volatility (30d): {api.get_historical_volatility():.2%}")
