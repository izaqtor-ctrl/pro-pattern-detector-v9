# data_handler.py
# Pattern Detector V8.2 - Data Fetching and Processing with Consolidation Indicators

import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import warnings
from config import DEMO_DATA_CONFIG, ERROR_MESSAGES, WARNING_MESSAGES, INDICATOR_PERIODS, PATTERN_PARAMS

warnings.filterwarnings('ignore')

# Try to import yfinance with error handling
try:
    import yfinance as yf
    YFINANCE_AVAILABLE = True
except ImportError:
    YFINANCE_AVAILABLE = False

def create_demo_data(ticker, period):
    """Create realistic demo data when yfinance is not available"""
    if period == "1wk":
        days_map = {"1y": 52, "6mo": 26, "3mo": 13, "1mo": 4}
        freq = 'W'
    elif period == "4h":
        days_map = {"1y": 2190, "6mo": 1095, "3mo": 547, "1mo": 183}  # 4-hour periods
        freq = '4H'
    else:
        days_map = {"1y": 252, "6mo": 126, "3mo": 63, "1mo": 22}
        freq = 'D'
    
    days = days_map.get(period.replace("1wk", "1y").replace("4h", "1y"), 63)
    dates = pd.date_range(end=datetime.now(), periods=days, freq=freq)
    
    # Create reproducible but varied data per ticker
    np.random.seed(hash(ticker) % 2147483647)
    base_price = np.random.randint(
        DEMO_DATA_CONFIG["base_price_range"][0], 
        DEMO_DATA_CONFIG["base_price_range"][1]
    )
    
    # Generate realistic price movements with consolidation periods
    returns = np.random.normal(0.001, DEMO_DATA_CONFIG["volatility"], days)
    
    # Add consolidation periods (lower volatility sections)
    consolidation_periods = np.random.choice(range(days//4, days), size=2, replace=False)
    for start in consolidation_periods:
        end = min(start + np.random.randint(10, 30), days)
        returns[start:end] *= 0.3  # Reduce volatility in consolidation
    
    returns[0] = 0
    close_prices = base_price * np.cumprod(1 + returns)
    
    # Generate OHLC data with realistic relationships
    high_mult = 1 + np.abs(np.random.normal(0, 0.01, days))
    low_mult = 1 - np.abs(np.random.normal(0, 0.01, days))
    open_mult = 1 + np.random.normal(0, 0.005, days)
    
    data = pd.DataFrame({
        'Open': close_prices * open_mult,
        'High': close_prices * high_mult,
        'Low': close_prices * low_mult,
        'Close': close_prices,
        'Volume': np.random.randint(
            DEMO_DATA_CONFIG["volume_range"][0], 
            DEMO_DATA_CONFIG["volume_range"][1], 
            days
        )
    }, index=dates)
    
    # Ensure OHLC relationships are correct
    data['High'] = np.maximum.reduce([data['Open'], data['High'], data['Low'], data['Close']])
    data['Low'] = np.minimum.reduce([data['Open'], data['High'], data['Low'], data['Close']])
    
    return data

def get_stock_data(ticker, period):
    """Fetch stock data with fallback to demo data"""
    if not YFINANCE_AVAILABLE:
        return create_demo_data(ticker, period), "demo"
    
    try:
        stock = yf.Ticker(ticker)
        
        # Handle different timeframes
        if period == "1wk":
            data = stock.history(period="1y", interval="1wk")
        elif period == "4h":
            # For 4-hour data, we need to specify a longer period
            data = stock.history(period="1y", interval="1h")
            if len(data) > 0:
                # Resample to 4-hour intervals
                data = data.resample('4H').agg({
                    'Open': 'first',
                    'High': 'max', 
                    'Low': 'min',
                    'Close': 'last',
                    'Volume': 'sum'
                }).dropna()
        else:
            data = stock.history(period=period)
            
        if len(data) == 0:
            return create_demo_data(ticker, period), "demo"
        
        return data, "real"
        
    except Exception as e:
        return create_demo_data(ticker, period), "demo"

def calculate_true_range(data):
    """Calculate True Range"""
    high_low = data['High'] - data['Low']
    high_close_prev = np.abs(data['High'] - data['Close'].shift(1))
    low_close_prev = np.abs(data['Low'] - data['Close'].shift(1))
    
    tr = np.maximum(high_low, np.maximum(high_close_prev, low_close_prev))
    return tr

def calculate_atr(data, period=14):
    """Calculate Average True Range"""
    tr = calculate_true_range(data)
    atr = tr.rolling(window=period).mean()
    return atr

def calculate_atr_percent(data, period=14):
    """Calculate ATR as percentage of close price"""
    atr = calculate_atr(data, period)
    atr_percent = (atr / data['Close']) * 100
    return atr_percent

def calculate_bollinger_bands(data, period=20, std_dev=2):
    """Calculate Bollinger Bands"""
    sma = data['Close'].rolling(window=period).mean()
    std = data['Close'].rolling(window=period).std()
    
    bb_upper = sma + (std * std_dev)
    bb_lower = sma - (std * std_dev)
    bb_width = (bb_upper - bb_lower) / sma
    
    return bb_upper, bb_lower, bb_width

def calculate_ema(data, period):
    """Calculate Exponential Moving Average"""
    return data['Close'].ewm(span=period).mean()

def calculate_ma_pinch(data):
    """Calculate Moving Average Pinch (convergence)"""
    ema10 = calculate_ema(data, 10)
    ema20 = calculate_ema(data, 20)
    ema50 = calculate_ema(data, 50)
    
    ma_max = np.maximum(np.maximum(ema10, ema20), ema50)
    ma_min = np.minimum(np.minimum(ema10, ema20), ema50)
    
    ma_pinch = (ma_max - ma_min) / data['Close']
    return ma_pinch, ema10, ema20, ema50

def calculate_nr_bars(data, periods=[4, 7]):
    """Calculate Narrow Range bars (NR4, NR7)"""
    tr = calculate_true_range(data)
    results = {}
    
    for period in periods:
        # Find bars where TR is the lowest in the last 'period' bars
        rolling_min = tr.rolling(window=period).min()
        nr_flag = (tr == rolling_min) & (tr.notna())
        results[f'NR{period}'] = nr_flag
    
    return results

def calculate_percentile_ranks(series, window):
    """Calculate rolling percentile ranks"""
    def percentile_rank(x):
        if len(x) < 2:
            return np.nan
        return (x.iloc[-1] <= x).mean() * 100
    
    return series.rolling(window=window).apply(percentile_rank, raw=False)

def calculate_rsi(data, period=14):
    """Calculate RSI (Relative Strength Index)"""
    delta = data['Close'].diff()
    gain = (delta.where(delta > 0, 0)).rolling(window=period).mean()
    loss = (-delta.where(delta < 0, 0)).rolling(window=period).mean()
    rs = gain / loss
    rsi = 100 - (100 / (1 + rs))
    return rsi

def calculate_macd(data, fast=12, slow=26, signal=9):
    """Calculate MACD (Moving Average Convergence Divergence)"""
    ema_fast = data['Close'].ewm(span=fast).mean()
    ema_slow = data['Close'].ewm(span=slow).mean()
    macd_line = ema_fast - ema_slow
    signal_line = macd_line.ewm(span=signal).mean()
    histogram = macd_line - signal_line
    return macd_line, signal_line, histogram

def add_consolidation_indicators(data, timeframe="daily"):
    """Add all consolidation-specific indicators"""
    # Get parameters for the timeframe
    params = PATTERN_PARAMS["Consolidation Breakout"]
    
    # Determine percentile window based on timeframe
    if timeframe == "4h":
        perc_window = params["percentile_window_4h"]
    elif timeframe == "weekly":
        perc_window = params["percentile_window_weekly"]
    else:
        perc_window = params["percentile_window_daily"]
    
    # Ensure we don't exceed available data
    perc_window = min(perc_window, len(data))
    
    # Basic True Range and ATR
    data['TR'] = calculate_true_range(data)
    data['ATR14'] = calculate_atr(data, INDICATOR_PERIODS['atr'])
    data['ATRp'] = calculate_atr_percent(data, INDICATOR_PERIODS['atr'])
    data['TR20'] = data['TR'].rolling(window=INDICATOR_PERIODS['tr_sma']).mean()
    
    # Bollinger Bands and width
    bb_upper, bb_lower, bb_width = calculate_bollinger_bands(
        data, 
        INDICATOR_PERIODS['bb_period'], 
        INDICATOR_PERIODS['bb_std']
    )
    data['BB_Upper'] = bb_upper
    data['BB_Lower'] = bb_lower
    data['BBwidth20'] = bb_width
    
    # Moving averages and pinch
    ma_pinch, ema10, ema20, ema50 = calculate_ma_pinch(data)
    data['MA_pinch'] = ma_pinch
    data['EMA10'] = ema10
    data['EMA20'] = ema20
    data['EMA50'] = ema50
    
    # Volume indicators
    data['Vol50'] = data['Volume'].rolling(window=INDICATOR_PERIODS['volume_sma50']).mean()
    data['Vol_Ratio'] = data['Volume'] / data['Vol50']
    
    # NR (Narrow Range) bars
    nr_results = calculate_nr_bars(data)
    for key, values in nr_results.items():
        data[key] = values
    
    # Percentile ranks (only if we have enough data)
    if len(data) >= perc_window:
        data['ATRp_pct'] = calculate_percentile_ranks(data['ATRp'], perc_window)
        data['BBwidth20_pct'] = calculate_percentile_ranks(data['BBwidth20'], perc_window)
    else:
        # Fallback for insufficient data
        data['ATRp_pct'] = 50.0  # neutral percentile
        data['BBwidth20_pct'] = 50.0  # neutral percentile
    
    # Dollar volume for liquidity check
    data['Dollar_Volume'] = data['Volume'] * data['Close']
    data['Avg_Dollar_Volume'] = data['Dollar_Volume'].rolling(window=20).mean()
    
    return data

def add_technical_indicators(data, timeframe="daily"):
    """Add all technical indicators to the dataset"""
    # RSI
    data['RSI'] = calculate_rsi(data)
    
    # MACD
    macd_line, signal_line, histogram = calculate_macd(data)
    data['MACD'] = macd_line
    data['MACD_Signal'] = signal_line
    data['MACD_Histogram'] = histogram
    
    # Moving averages
    data['SMA20'] = data['Close'].rolling(window=INDICATOR_PERIODS['sma']).mean()
    
    # Volume indicators
    data['Volume_SMA20'] = data['Volume'].rolling(window=INDICATOR_PERIODS['volume_sma']).mean()
    data['Volume_Ratio'] = data['Volume'] / data['Volume_SMA20']
    
    # Add consolidation-specific indicators
    data = add_consolidation_indicators(data, timeframe)
    
    return data

def validate_data_quality(data, ticker):
    """Validate data quality and return status"""
    if data is None or len(data) == 0:
        return False, f"No data available for {ticker}"
    
    if len(data) < 10:
        return False, f"Insufficient data for {ticker} (only {len(data)} periods)"
    
    # Check for required columns
    required_columns = ['Open', 'High', 'Low', 'Close', 'Volume']
    missing_columns = [col for col in required_columns if col not in data.columns]
    if missing_columns:
        return False, f"Missing required columns for {ticker}: {missing_columns}"
    
    # Check for null values in recent data
    recent_data = data.tail(20)
    if recent_data[required_columns].isnull().any().any():
        return False, f"Missing values in recent data for {ticker}"
    
    # Check for unrealistic values
    if (recent_data['High'] < recent_data['Low']).any():
        return False, f"Data integrity error for {ticker}: High < Low"
    
    if (recent_data['Volume'] <= 0).any():
        return False, f"Invalid volume data for {ticker}"
    
    return True, "Data quality OK"

def get_data_summary(data, ticker, data_source, timeframe="daily"):
    """Generate data summary for display"""
    if data is None or len(data) == 0:
        return None
    
    summary = {
        'ticker': ticker,
        'source': data_source,
        'timeframe': timeframe,
        'periods': len(data),
        'date_range': f"{data.index[0].strftime('%Y-%m-%d')} to {data.index[-1].strftime('%Y-%m-%d')}",
        'current_price': data['Close'].iloc[-1],
        'price_change': data['Close'].iloc[-1] - data['Close'].iloc[-2] if len(data) > 1 else 0,
        'avg_volume': data['Volume'].tail(20).mean(),
        'current_volume': data['Volume'].iloc[-1],
        'atr_current': data.get('ATRp', pd.Series([0])).iloc[-1] if 'ATRp' in data.columns else 0,
        'bb_width_current': data.get('BBwidth20', pd.Series([0])).iloc[-1] if 'BBwidth20' in data.columns else 0
    }
    
    return summary

def fetch_and_process_data(ticker, period):
    """Main function to fetch and process data for a ticker"""
    # Determine timeframe from period
    if period == "1wk":
        timeframe = "weekly"
    elif period == "4h":
        timeframe = "4h"
    else:
        timeframe = "daily"
    
    # Fetch raw data
    data, source = get_stock_data(ticker, period)
    
    # Validate data quality
    is_valid, status_message = validate_data_quality(data, ticker)
    
    if not is_valid:
        return None, None, status_message, timeframe
    
    # Add technical indicators
    data = add_technical_indicators(data, timeframe)
    
    # Generate summary
    summary = get_data_summary(data, ticker, source, timeframe)
    
    return data, summary, status_message, timeframe

def get_timeframe_info(period):
    """Get timeframe information for display and processing"""
    if period == "1wk":
        return {
            'display_name': 'Weekly',
            'frequency': 'weekly',
            'lookback_multiplier': 1.5,
            'aging_threshold_multiplier': 1.3
        }
    elif period == "4h":
        return {
            'display_name': '4-Hour',
            'frequency': '4h',
            'lookback_multiplier': 2.0,
            'aging_threshold_multiplier': 1.5
        }
    else:
        return {
            'display_name': 'Daily',
            'frequency': 'daily', 
            'lookback_multiplier': 1.0,
            'aging_threshold_multiplier': 1.0
        }

def check_data_availability():
    """Check if yfinance is available and return status"""
    return {
        'yfinance_available': YFINANCE_AVAILABLE,
        'demo_mode': not YFINANCE_AVAILABLE,
        'message': WARNING_MESSAGES["demo_mode"] if not YFINANCE_AVAILABLE else "Real-time data available"
    }

def calculate_liquidity_filter(data, min_dollar_volume):
    """Check if stock meets minimum liquidity requirements"""
    if 'Avg_Dollar_Volume' not in data.columns:
        return True  # Skip filter if data not available
    
    recent_avg_dollar_volume = data['Avg_Dollar_Volume'].tail(20).mean()
    return recent_avg_dollar_volume >= min_dollar_volume

def get_consolidation_window_data(data, window_bars):
    """Extract consolidation window data safely"""
    if len(data) < window_bars + 5:  # Need some buffer
        return None
    
    # Use data excluding the current bar for consolidation analysis
    window_data = data.iloc[-(window_bars+1):-1]
    
    if len(window_data) < window_bars:
        return None
    
    return {
        'high': window_data['High'].max(),
        'low': window_data['Low'].min(),
        'data': window_data
    }
