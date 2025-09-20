# config.py
# Pattern Detector V8.2 - Configuration Settings with Consolidation Breakout

# Application Settings
APP_TITLE = "Pro Pattern Detector v8.2"
APP_SUBTITLE = "Enhanced with Consolidation Breakout - Professional Pattern Recognition"
VERSION = "8.2"

# Pattern Detection Settings
PATTERNS = ["Flat Top Breakout", "Bull Flag", "Cup Handle", "Inside Bar", "Inverse Head Shoulders", "Consolidation Breakout"]
DEFAULT_PATTERNS = ["Flat Top Breakout", "Bull Flag", "Inside Bar", "Inverse Head Shoulders", "Consolidation Breakout"]

# Timeframe Settings
PERIOD_OPTIONS = ["1mo", "3mo", "6mo", "1y", "1wk (Weekly)", "4h (4-Hour)"]
DEFAULT_PERIOD = "3mo"

# Confidence Settings
MIN_CONFIDENCE_RANGE = (45, 85)
DEFAULT_MIN_CONFIDENCE = 55

# Volume Analysis Settings
VOLUME_THRESHOLDS = {
    "good": 1.3,
    "strong": 1.5,
    "exceptional": 2.0
}

VOLUME_SCORE_POINTS = {
    "exceptional": 25,  # 2.0x+ average
    "strong": 20,       # 1.5-2.0x average
    "good": 15,         # 1.3-1.5x average
    "weak": 0           # <1.3x average
}

# Pattern-specific volume bonuses
PATTERN_VOLUME_BONUS = {
    "Bull Flag": 20,      # Flagpole vs flag volume
    "Cup Handle": 20,     # Volume dryup in handle
    "Flat Top Breakout": 20,  # Breakout volume surge
    "Inside Bar": 15,     # Consolidation volume
    "Inverse Head Shoulders": 20,  # Classic volume diminishing pattern
    "Consolidation Breakout": 25   # Volume expansion on breakout
}

# NEW: Consolidation Breakout Parameters
PATTERN_PARAMS = {
    "Consolidation Breakout": {
        "percentile_window_daily": 252,    # 1 year of daily data
        "percentile_window_4h": 1000,      # ~6 months of 4h data
        "percentile_window_weekly": 104,   # 2 years of weekly data
        "atrp_percentile_cut": 15,         # bottom 15% for low volatility
        "bbw_percentile_cut": 15,          # bottom 15% for tight BB
        "box_bars_daily": 15,              # consolidation window
        "box_bars_4h": 40,                 # longer for 4h
        "box_bars_weekly": 8,              # shorter for weekly
        "box_width_max": 0.06,             # 6% max consolidation range
        "ma_pinch_max": 0.02,              # 2% max MA spread
        "nr_cluster_lookback": 5,          # lookback for NR bars
        "nr_cluster_min_hits": 2,          # minimum NR occurrences
        "vol_dryup_k": 10,                 # volume dry-up window
        "vol_dryup_mult": 0.7,             # below 70% of SMA50
        "vol_dryup_threshold": 0.6,        # 60% of bars must be low volume
        "breakout_tr_mult": 1.5,           # True Range expansion
        "breakout_vol_mult": 1.5,          # Volume expansion
        "entry_buffer": 0.002,             # 0.2% above box high
        "stop_buffer": 0.005,              # 0.5% below box low
        "stop_atr_floor_mult": 0.75,       # 0.75x ATR minimum stop
        "min_liquidity_usd": 2e7,          # $20M average dollar volume
        "min_confidence_base": 40,         # base confidence for detection
        "consolidation_bonus": 20,         # bonus for tight consolidation
        "breakout_bonus": 25,              # bonus for confirmed breakout
        "volume_dryup_bonus": 15,          # bonus for volume dry-up
        "ma_pinch_bonus": 10,              # bonus for MA convergence
        "nr_cluster_bonus": 15             # bonus for NR cluster
    }
}

# Confidence Capping
MAX_CONFIDENCE_WITHOUT_VOLUME = 70

# Market Timing Settings
MARKET_TIMING_ADJUSTMENTS = {
    "weekend_penalty": 0.95,      # -5%
    "friday_penalty": 0.85,       # -15% without exceptional volume
    "midweek_bonus": 1.02,        # +2%
    "monday_gap_check": True
}

# Pattern Age Limits (days/periods)
PATTERN_AGE_LIMITS = {
    "daily": {
        "Flat Top Breakout": 8,
        "Bull Flag": 10,
        "Cup Handle": 30,
        "Inside Bar": 6,
        "Inverse Head Shoulders": 30,
        "Consolidation Breakout": 12
    },
    "4h": {
        "Flat Top Breakout": 32,  # 4h periods
        "Bull Flag": 40,
        "Cup Handle": 120,
        "Inside Bar": 24,
        "Inverse Head Shoulders": 120,
        "Consolidation Breakout": 48
    },
    "weekly": {
        "Flat Top Breakout": 8,  # weeks
        "Bull Flag": 10,         # weeks
        "Cup Handle": 30,        # weeks
        "Inside Bar": 8,         # weeks
        "Inverse Head Shoulders": 20,  # weeks
        "Consolidation Breakout": 12   # weeks
    }
}

# Risk Management Settings
RISK_MULTIPLIERS = {
    "volatility_stop": 1.5,  # 1.5x average daily range
    "min_stop_distance": {
        "Flat Top Breakout": 0.03,  # 3%
        "Bull Flag": 0.04,          # 4%
        "Cup Handle": 0.05,         # 5%
        "Inside Bar": 0.05,         # 5%
        "Inverse Head Shoulders": 0.04,  # 4%
        "Consolidation Breakout": 0.035  # 3.5%
    }
}

# Target Calculation Settings
MIN_RISK_REWARD_RATIOS = {
    "target1": 1.5,
    "target2": 2.5
}

# Inside Bar specific settings
INSIDE_BAR_CONFIG = {
    "entry_buffer": 1.05,    # 5% above inside bar high
    "stop_buffer": 0.95,     # 5% below inside bar low
    "target2_multiplier": 1.13,  # 13% above mother bar high
    "target3_multiplier": 1.21,  # 21% above mother bar high
    "max_inside_bars": 2,
    "preferred_inside_bars": 1
}

# Technical Indicator Settings
INDICATOR_PERIODS = {
    "rsi": 14,
    "macd_fast": 12,
    "macd_slow": 26,
    "macd_signal": 9,
    "sma": 20,
    "volume_sma": 20,
    "atr": 14,
    "bb_period": 20,
    "bb_std": 2,
    "ema10": 10,
    "ema20": 20,
    "ema50": 50,
    "volume_sma50": 50,
    "tr_sma": 20
}

# Pattern Detection Thresholds
PATTERN_THRESHOLDS = {
    "Flat Top Breakout": {
        "min_initial_gain": 0.10,  # 10%
        "min_pullback": 0.08,      # 8%
        "resistance_tolerance": 0.98  # 98% of resistance level
    },
    "Bull Flag": {
        "min_flagpole_gain": 0.08,  # 8%
        "pullback_range": (-0.15, 0.05),  # -15% to +5%
        "flag_tolerance": 0.95
    },
    "Cup Handle": {
        "min_cup_depth": 0.08,     # 8%
        "max_cup_depth": 0.60,     # 60%
        "max_handle_depth": 0.25   # 25%
    },
    "Inside Bar": {
        "tight_consolidation": 0.30,    # 30% of mother bar (daily)
        "tight_consolidation_weekly": 0.35,  # 35% for weekly
        "tight_consolidation_4h": 0.25,      # 25% for 4h
        "good_consolidation": 0.50,
        "good_consolidation_weekly": 0.55,
        "good_consolidation_4h": 0.45,
        "moderate_consolidation": 0.70,
        "moderate_consolidation_weekly": 0.75,
        "moderate_consolidation_4h": 0.65
    },
    "Inverse Head Shoulders": {
        "min_head_depth": 0.05,     # 5% minimum depth
        "max_head_depth": 0.60,     # 60% maximum depth
        "min_symmetry": 0.5,        # 50% symmetry minimum
        "min_pattern_width_daily": 20,   # 20 days minimum
        "max_pattern_width_daily": 60,   # 60 days maximum
        "min_pattern_width_weekly": 15,  # 15 weeks minimum
        "max_pattern_width_weekly": 40,  # 40 weeks maximum
        "min_pattern_width_4h": 80,      # 80 4h periods minimum
        "max_pattern_width_4h": 240,     # 240 4h periods maximum
        "impulsive_move_threshold": 0.6,  # 60% impulsive bars required
        "ideal_head_depth": 0.15,        # 15% ideal depth
        "pivot_strength_daily": 5,       # 5/5 pivot validation
        "pivot_strength_weekly": 4,      # 4/4 pivot validation for weekly
        "pivot_strength_4h": 3           # 3/3 pivot validation for 4h
    },
    "Consolidation Breakout": {
        "min_consolidation_bars": 8,     # minimum bars in consolidation
        "max_consolidation_bars": 100,   # maximum bars in consolidation
        "min_box_height": 0.02,          # 2% minimum range
        "max_box_height": 0.15,          # 15% maximum range
        "breakout_confirmation_bars": 1   # bars to confirm breakout
    }
}

# Chart Settings
CHART_CONFIG = {
    "height": 800,
    "volume_opacity": 0.7,
    "volume_colors": {
        "exceptional": "darkgreen",
        "strong": "green", 
        "good": "lightgreen",
        "weak": "red",
        "default": "blue"
    },
    "line_colors": {
        "entry": "green",
        "stop": "red",
        "target1": "lime",
        "target2": "darkgreen",
        "target3": "purple",
        "sma": "orange",
        "neckline": "blue",
        "left_shoulder": "cyan",
        "head": "magenta",
        "right_shoulder": "cyan",
        "consolidation_box": "purple",
        "breakout_marker": "gold"
    },
    "consolidation_box": {
        "line_width": 2,
        "line_dash": "dash",
        "fill_opacity": 0.1,
        "fill_color": "purple"
    }
}

# Demo Data Settings (when yfinance unavailable)
DEMO_DATA_CONFIG = {
    "base_price_range": (50, 250),
    "volatility": 0.02,
    "volume_range": (1000000, 5000000)
}

# Export Settings
EXPORT_FILENAME_FORMAT = "patterns_v82_{timestamp}.csv"

# Error Messages
ERROR_MESSAGES = {
    "insufficient_data": "Insufficient data for analysis",
    "no_patterns": "No patterns detected. Try lowering confidence threshold.",
    "yfinance_unavailable": "Using demo data (yfinance not available)",
    "data_fetch_error": "Error fetching data, using demo data",
    "consolidation_data_insufficient": "Insufficient data for consolidation analysis"
}

# Warning Messages
WARNING_MESSAGES = {
    "demo_mode": "Demo Mode: Using simulated data",
    "weekend_analysis": "Weekend Analysis: Patterns based on Friday's close",
    "friday_risk": "Friday entries require exceptional volume for weekend holds",
    "monday_gap": "Monday gap risk - validate patterns post-open",
    "4h_data_limited": "4-hour data may be limited in demo mode"
}

# Success Messages
SUCCESS_MESSAGES = {
    "pattern_detected": "Pattern detected with high confidence",
    "volume_confirmed": "Volume confirmation present",
    "optimal_timing": "Optimal timing for entry",
    "consolidation_confirmed": "Tight consolidation confirmed",
    "breakout_confirmed": "Breakout confirmed with volume"
}

# Disclaimer
DISCLAIMER_TEXT = """
DISCLAIMER: Educational purposes only. Not financial advice. 
Trading involves substantial risk. Consult professionals before trading.
"""
