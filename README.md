# Pattern-Detection-V9
Professional Trading Pattern Detection - Build 8.2.1

A modular Streamlit application for detecting institutional-grade swing trading patterns with advanced consolidation analysis and multi-timeframe support.

## Quick Start

```bash
pip install streamlit pandas numpy plotly yfinance
streamlit run main.py
```

## What It Does

Detects 5 professional trading patterns across multiple timeframes:
- **Consolidation Breakout**: Advanced coiling spring detection with multi-criteria analysis
- **Inside Bar**: Consolidation breakouts with triple targets  
- **Bull Flag**: Trend continuation with flagpole projection
- **Flat Top Breakout**: Resistance breakouts with triangle targets
- **Inverse Head & Shoulders**: Classic reversal with measured moves
- **Cup Handle**: Base breakouts with cup depth projection

## New in V9: Advanced Consolidation Breakout Pattern

### Professional Consolidation Detection Engine
**Multi-Criteria Analysis** (any single criterion qualifies):

1. **ATR Volatility Analysis**: ATR% in bottom 15% of lookback window
2. **Bollinger Band Compression**: BB width in bottom 15% percentile  
3. **Narrow Range Clustering**: 2+ NR4/NR7 bars in 5-period window
4. **Price Box Tightness**: Range ≤ 6% over consolidation period
5. **Moving Average Pinch**: EMA 10/20/50 spread ≤ 2% convergence
6. **Volume Dry-up Pattern**: 60%+ bars below 70% of SMA50

### Triple Breakout Confirmation System
- **Price Breakout**: Close above consolidation box high + 0.2% buffer
- **True Range Expansion**: Current TR > 1.5x average TR(20) 
- **Volume Surge**: Volume ≥ 1.5x SMA(50) with tier scoring
- **Confirmation Levels**: Full/Partial/Price-Only status tracking

### Multi-Timeframe Architecture
- **Daily Timeframe**: 252-period lookback, 15-bar consolidation window
- **4-Hour Timeframe**: 1000-period lookback, 40-bar consolidation window  
- **Weekly Timeframe**: 104-period lookback, 8-bar consolidation window
- **Adaptive Parameters**: Timeframe-specific thresholds and aging limits

## Core Features

### Smart Pattern Detection
- **Volume Confirmation System**: 1.3x to 2.0x+ thresholds with tier scoring
- **Market Timing Intelligence**: Day-of-week adjustments and gap risk analysis
- **Measured Move Targets**: Pattern-specific projections, not fixed ratios
- **Age Validation**: Prevents stale pattern detection
- **Liquidity Filtering**: $20M+ average dollar volume requirement

### Professional Risk Management
- **Volatility-Based Stops**: ATR floor protection with multiple stop candidates
- **Target Hierarchy**: Measured moves with 2R/3R minimum enforcement
- **Position Sizing**: Standard 2% risk calculations
- **Risk/Reward Optimization**: Minimum 1.5:1 and 2.5:1 ratios enforced

### Market Timing Intelligence
- **Day-of-Week Analysis**: Confidence adjustments based on trading session
- **Gap Risk Assessment**: HIGH/MEDIUM/LOW classification system
- **Entry Timing Recommendations**: Optimal timing based on market conditions
- **Weekend/Friday Warnings**: Risk alerts for extended holding periods

### Enhanced Visualization
- **Multi-Panel Charts**: Price/MACD/Volume with synchronized annotations
- **Pattern Structure Markers**: Educational formation point indicators
- **Consolidation Box Display**: Visual boundaries with dimension statistics
- **Breakout Confirmation Indicators**: Real-time status markers
- **Volume Tier Visualization**: Color-coded volume analysis
- **Invalidation Warnings**: Prominent alerts for compromised patterns

## Modular Architecture

```
pattern-detector-v9/
├── main.py                 # Streamlit interface and orchestration
├── config.py              # Comprehensive configuration management  
├── data_handler.py        # Multi-timeframe data processing
├── pattern_detectors.py   # Core pattern algorithms
├── market_timing.py       # Context-aware timing analysis
├── risk_calculator.py     # Professional level calculations
└── chart_generator.py     # Advanced visualization engine
```

**Benefits of V9 Architecture:**
- Each module under 400 lines for maintainability
- Clean separation of concerns with minimal coupling
- Extensive configuration management
- Comprehensive error handling with graceful fallbacks
- Vectorized pandas operations for performance

## Pattern Detection Algorithms

### Consolidation Breakout (NEW)
```python
# Consolidation Detection
- ATR percentile analysis (bottom 15%)
- Bollinger Band width compression
- NR4/NR7 cluster identification  
- Price box tightness validation
- Moving average convergence analysis
- Volume dry-up confirmation

# Breakout Validation
- Price above box high + buffer
- True Range expansion (1.5x+ average)
- Volume surge with tier bonuses
- Technical indicator alignment
```

### Inside Bar Enhancement
```python
# Enhanced Detection
- Color validation (Green mother + Red inside)
- Size ratio analysis with timeframe adaptation
- Triple target system (Mother bar, +13%, +21%)
- Multi-bar inside sequences (1-2 bars)
```

### Bull Flag Refinement  
```python
# Flagpole Analysis
- Minimum 8% gain requirement
- Volume pattern validation (flagpole vs flag)
- Pullback range validation (-15% to +5%)
- Age validation with invalidation checks
```

### Inverse Head & Shoulders
```python
# Professional Implementation
- 5/5 pivot validation system (daily)
- Symmetry scoring (time + price weighted)
- Neckline slope analysis
- Head depth measured move projection
```

## Usage Examples

### Basic Analysis
```python
# Configure in Streamlit sidebar:
# - Patterns: Consolidation Breakout, Inside Bar, Bull Flag
# - Tickers: AAPL,MSFT,NVDA,GOOGL
# - Timeframe: Daily (3mo) or 4-Hour  
# - Min confidence: 55%
# - Volume confirmation: Optional

# Results display:
# - Pattern confidence scores with timing adjustments
# - Volume status (Good/Strong/Exceptional) 
# - Entry/Stop/Target levels with R/R ratios
# - Market timing context and gap risk assessment
# - Visual charts with educational annotations
```

### Advanced Filtering
```python
# Consolidation Breakout Filters:
consolidation_filters = {
    'require_breakout_confirmation': True,    # Full confirmation only
    'min_consolidation_bars': 12,            # Minimum consolidation period
    'max_box_width': 4.5                     # Maximum 4.5% price range
}

# Volume Requirements:
volume_filters = {
    'require_volume': True,                   # Mandatory volume confirmation  
    'threshold': '1.5x (Strong)'            # Strong volume minimum
}
```

## Volume Analysis Framework

### Scoring System
- **Exceptional (2.0x+)**: 25 points + pattern bonus
- **Strong (1.5x)**: 20 points + pattern bonus  
- **Good (1.3x)**: 15 points + pattern bonus
- **Weak (<1.3x)**: 0 points, confidence capped at 70%

### Pattern-Specific Analysis
- **Consolidation Breakout**: Dry-up during consolidation + expansion on breakout
- **Bull Flag**: Flagpole volume vs flag volume comparison
- **Cup Handle**: Volume dry-up in handle formation
- **Inside Bar**: Prefer low volume during consolidation
- **Inverse H&S**: Classic diminishing volume pattern

## Market Timing Adjustments

### Day-of-Week Impact
- **Weekend Analysis**: -5% confidence (gap risk)
- **Friday Sessions**: -15% without exceptional volume  
- **Monday Sessions**: Gap validation required
- **Mid-week Optimal**: +2% confidence bonus

### Gap Risk Management
- **HIGH**: Weekend news cycle, extended closures
- **MEDIUM**: Friday close, Monday open volatility
- **LOW**: Standard mid-week conditions

## Installation & Setup

### Method 1: Direct Download
1. Download all 6 Python files from repository
2. Place in same directory  
3. Install dependencies: `pip install streamlit pandas numpy plotly yfinance`
4. Launch: `streamlit run main.py`

### Method 2: Git Clone
```bash
git clone https://github.com/[username]/pattern-detector-v9.git
cd pattern-detector-v9
pip install -r requirements.txt
streamlit run main.py
```

### Dependencies
```txt
streamlit>=1.28.0
pandas>=2.0.0
numpy>=1.24.0
plotly>=5.15.0
yfinance>=0.2.0
```

## Configuration Options

### Sidebar Controls
- **Pattern Selection**: Multi-select from 5 patterns
- **Ticker Input**: Comma-separated symbols
- **Timeframe**: 1mo to 1y, plus 4-Hour and Weekly
- **Confidence Threshold**: 45-85% range
- **Volume Filters**: Optional with tier selection
- **Timing Adjustments**: Show/hide timing analysis

### Advanced Filters
- **Consolidation Breakout**: Confirmation level, bar count, box width
- **Volume Requirements**: Mandatory confirmation with threshold
- **Market Timing**: Gap risk consideration, timing optimization

### Default Configuration
```python
patterns = ["Flat Top Breakout", "Bull Flag", "Inside Bar", 
           "Inverse Head Shoulders", "Consolidation Breakout"]
period = "3mo"  # Daily timeframe
min_confidence = 55%
volume_confirmation = Optional
```

## Results Export & Analysis

### CSV Export Features
```python
# Export includes:
- Ticker and pattern identification
- Timeframe and confidence scores  
- Volume status and tier classification
- Entry/stop/target levels with R/R ratios
- Target calculation methodology
- Market timing context
- Consolidation-specific metrics (box width, breakout status)
```

### Summary Analytics
- **Pattern Distribution**: Count and percentage by type
- **Timeframe Analysis**: Daily vs 4-Hour vs Weekly breakdown
- **Volume Quality**: Percentage with strong/exceptional volume
- **Confidence Metrics**: Average scores and R/R ratios
- **Consolidation Stats**: Breakout confirmation rates

## Example Output

```
Ticker  Pattern              Timeframe  Confidence  Volume          Entry    Target1   R/R1    Breakout
AAPL    Consolidation BO     Daily      78%        Strong (1.6x)   $185.50  $195.20   2.1:1   ✅ Confirmed
MSFT    Inside Bar           Daily      85%        Good (1.4x)     $415.25  $425.00   2.8:1   N/A
NVDA    Inverse H&S          4-Hour     72%        Exceptional     $875.30  $920.15   1.9:1   N/A
GOOGL   Bull Flag            Daily      81%        Strong (1.7x)   $142.80  $151.20   2.3:1   N/A
```

## Performance & Limitations

### Strengths
- **Institutional-grade algorithms** with academic research backing
- **Multi-timeframe support** with adaptive parameters
- **Professional risk management** with measured move targets
- **Advanced volume analysis** with pattern-specific logic
- **Comprehensive visualization** with educational value

### Considerations
- **Demo mode fallback** when yfinance unavailable
- **4-hour data limitations** in some demo scenarios  
- **Intraday gap risks** for overnight positions
- **Pattern age validation** prevents stale signals
- **Educational tool** - not financial advice

## Development Roadmap

### Completed (V9)
- Advanced consolidation detection with multi-criteria analysis
- 4-hour timeframe support with proper data handling
- Enhanced volume analysis with pattern-specific bonuses
- Professional chart annotations with educational markers
- Comprehensive configuration management system

### Future Enhancements
- **Real-time alerts** with webhook integration
- **Backtesting engine** with historical performance analysis  
- **Portfolio management** with position sizing optimization
- **Advanced screeners** with sector/market cap filtering
- **Mobile optimization** with responsive design

## Disclaimer

**EDUCATIONAL PURPOSES ONLY - NOT FINANCIAL ADVICE**

This application is designed for educational use and pattern recognition learning. Trading involves substantial financial risk and may not be suitable for all investors. Past performance does not guarantee future results. Always consult with qualified financial professionals before making investment decisions.

The patterns detected by this software are based on technical analysis principles and should be combined with fundamental analysis, risk management, and professional guidance for actual trading decisions.

## License

[Specify your license here - MIT, GPL, Commercial, etc.]

## Support & Contributing

### Contributing Guidelines
This modular architecture makes contributions straightforward:
- **Add patterns**: Modify `pattern_detectors.py` with new detection logic
- **Enhance charts**: Edit `chart_generator.py` for visualization improvements  
- **Adjust settings**: Update `config.py` for new parameters
- **Improve timing**: Modify `market_timing.py` for enhanced context analysis

### Code Standards
- Each module focused and under 400 lines
- Comprehensive docstrings and type hints
- Vectorized pandas operations for performance
- Graceful error handling with user feedback
- Consistent naming conventions throughout

### Support Channels
- **Issues**: GitHub issue tracker for bug reports
- **Features**: Enhancement requests via pull requests
- **Documentation**: Wiki for detailed usage examples
- **Community**: Discord/Slack for user discussions

## Contact

[Your contact information and social links]

---

**Pattern Detection V9 - Professional Trading Pattern Recognition**
*Detecting institutional-grade patterns with advanced consolidation analysis*
