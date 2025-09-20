# main.py
# Pattern Detector V8.2 - Main Streamlit Application with Consolidation Breakout

import streamlit as st
import pandas as pd
from datetime import datetime

# Import our modules
from config import *
from data_handler import fetch_and_process_data, check_data_availability, get_timeframe_info
from pattern_detectors import detect_pattern
from market_timing import get_market_context, display_market_context, adjust_confidence_for_timing
from risk_calculator import calculate_levels
from chart_generator import create_chart

# Configure Streamlit
st.set_page_config(
    page_title=APP_TITLE,
    layout="wide"
)

def main():
    st.title(APP_TITLE)
    st.markdown(f"**{APP_SUBTITLE}** - {VERSION}")
    
    # Check data availability
    data_status = check_data_availability()
    if data_status['demo_mode']:
        st.warning(data_status['message'])
    
    # Disclaimer
    st.error(DISCLAIMER_TEXT)
    
    # Market Timing Context Display
    market_context = display_market_context()
    
    # Info about new Consolidation Breakout pattern
    with st.expander("What's New in v8.2 - Consolidation Breakout Pattern"):
        st.markdown("""
        ### New Pattern: Consolidation Breakout
        
        **Professional-Grade Consolidation Detection**:
        - Multi-timeframe support (Daily/4-Hour/Weekly)
        - Advanced volatility analysis (ATR percentiles, Bollinger Band width)
        - NR4/NR7 cluster detection for tight ranges
        - Moving Average convergence analysis (MA pinch)
        - Volume dry-up confirmation during consolidation
        
        **Breakout Confirmation System**:
        - **Price breakout** above consolidation box high
        - **True Range expansion** (1.5x+ average TR)
        - **Volume surge** (1.5x+ average volume with tier bonuses)
        - **Measured move targets** based on box height
        - **Risk-based stops** with volatility floor protection
        
        **Key Features**:
        - **Visual consolidation box** with width/duration stats
        - **Breakout confirmation markers** (Full/Partial/Price-only)
        - **Liquidity filtering** ($20M+ average dollar volume)
        - **Box height projection** targets + 2R/3R minimums
        - **Educational annotations** showing criteria met
        
        **Consolidation Criteria** (any qualifies):
        - ATR% in bottom 15% of lookback window
        - Bollinger Band width in bottom 15%
        - NR4/NR7 cluster (2+ occurrences in 5 bars)
        - Box tightness ≤ 6% of price range
        - MA pinch ≤ 2% spread (EMA 10/20/50)
        - Volume dry-up (60%+ bars below 70% of SMA50)
        
        **All V8.1 Features Maintained**:
        - Inverse Head & Shoulders pattern
        - Inside Bar with triple targets
        - Enhanced volume confirmation system
        - Market timing adjustments
        - Professional risk/reward calculations
        
        This pattern detects the "coiling spring" effect - tight consolidations followed by explosive breakouts.
        """)
    
    # Sidebar Configuration
    st.sidebar.header("Configuration")
    
    # Pattern Selection
    selected_patterns = st.sidebar.multiselect(
        "Select Patterns:", 
        PATTERNS, 
        default=DEFAULT_PATTERNS
    )
    
    # Ticker Input
    tickers = st.sidebar.text_input("Tickers:", "AAPL,MSFT,NVDA")
    
    # Period Selection
    period_display = st.sidebar.selectbox(
        "Period:", 
        PERIOD_OPTIONS, 
        index=PERIOD_OPTIONS.index(DEFAULT_PERIOD)
    )
    
    # Handle different timeframe formats
    if period_display == "1wk (Weekly)":
        period = "1wk"
    elif period_display == "4h (4-Hour)":
        period = "4h"
    else:
        period = period_display
    
    # Confidence Threshold
    min_confidence = st.sidebar.slider(
        "Min Confidence:", 
        MIN_CONFIDENCE_RANGE[0], 
        MIN_CONFIDENCE_RANGE[1], 
        DEFAULT_MIN_CONFIDENCE
    )
    
    # Volume Filters
    st.sidebar.subheader("Volume Filters")
    require_volume = st.sidebar.checkbox("Require Volume Confirmation", value=False)
    volume_threshold = st.sidebar.selectbox(
        "Volume Threshold:", 
        ["1.3x (Good)", "1.5x (Strong)", "2.0x (Exceptional)"], 
        index=0
    )
    
    # Timing Filters
    st.sidebar.subheader("Timing Filters")
    show_timing_adjustments = st.sidebar.checkbox("Show Timing Adjustments", value=True)
    
    # Consolidation Breakout specific filters
    if "Consolidation Breakout" in selected_patterns:
        st.sidebar.subheader("Consolidation Filters")
        require_breakout_confirmation = st.sidebar.checkbox("Require Full Breakout Confirmation", value=False)
        min_consolidation_bars = st.sidebar.slider("Min Consolidation Bars:", 8, 50, 15)
        max_box_width = st.sidebar.slider("Max Box Width %:", 2, 15, 6)
    
    # Analysis Button
    if st.sidebar.button("Analyze", type="primary"):
        if tickers and selected_patterns:
            consolidation_filters = {}
            if "Consolidation Breakout" in selected_patterns:
                consolidation_filters = {
                    'require_breakout_confirmation': require_breakout_confirmation,
                    'min_consolidation_bars': min_consolidation_bars,
                    'max_box_width': max_box_width / 100  # Convert to decimal
                }
            
            run_analysis(
                tickers, selected_patterns, period, period_display, min_confidence,
                require_volume, volume_threshold, show_timing_adjustments, market_context,
                consolidation_filters
            )
        else:
            st.error("Please enter tickers and select at least one pattern.")

def run_analysis(tickers, selected_patterns, period, period_display, min_confidence,
                require_volume, volume_threshold, show_timing_adjustments, market_context,
                consolidation_filters=None):
    """Run the pattern analysis"""
    
    ticker_list = [t.strip().upper() for t in tickers.split(',')]
    timeframe_info = get_timeframe_info(period)
    
    st.header("Pattern Analysis Results")
    results = []
    
    for ticker in ticker_list:
        st.subheader(f"{ticker}")
        
        # Fetch and process data
        data, summary, status_message, timeframe = fetch_and_process_data(ticker, period)
        
        if data is None:
            st.error(f"⚠️ {status_message}")
            continue
        
        # Analyze each selected pattern
        for pattern in selected_patterns:
            detected, confidence, info = detect_pattern(data, pattern, market_context, timeframe)
            
            # Apply consolidation-specific filters
            if pattern == "Consolidation Breakout" and consolidation_filters:
                skip_pattern = apply_consolidation_filters(info, consolidation_filters)
                if skip_pattern:
                    continue
            
            # Apply timing adjustments
            confidence, info = adjust_confidence_for_timing(confidence, info, market_context)
            
            # Apply volume filter
            skip_pattern = False
            if require_volume:
                volume_multiplier = info.get('volume_multiplier', 0)
                threshold_map = {"1.3x (Good)": 1.3, "1.5x (Strong)": 1.5, "2.0x (Exceptional)": 2.0}
                required_threshold = threshold_map[volume_threshold]
                
                if volume_multiplier < required_threshold:
                    skip_pattern = True
                    st.info(f"{pattern}: {confidence:.0f}% - Filtered by volume requirement")
                    continue
            
            if detected and confidence >= min_confidence:
                # Calculate trading levels
                levels = calculate_levels(data, info, pattern)
                
                # Display results
                display_pattern_results(
                    ticker, pattern, confidence, info, levels, data, 
                    market_context, period, show_timing_adjustments, timeframe_info
                )
                
                # Add to results
                result_dict = create_result_dict(
                    ticker, pattern, confidence, info, levels, timeframe_info
                )
                results.append(result_dict)
                
            else:
                if not skip_pattern:
                    st.info(f"ℹ️ {pattern}: {confidence:.0f}% (below threshold)")
    
    # Display summary
    if results:
        display_summary(results, market_context)
    else:
        st.info("📊 No patterns detected. Try lowering the confidence threshold or adjusting filters.")

def apply_consolidation_filters(pattern_info, filters):
    """Apply consolidation-specific filters"""
    if not filters:
        return False
    
    # Require full breakout confirmation
    if filters.get('require_breakout_confirmation'):
        if not pattern_info.get('breakout_confirmed'):
            return True  # Skip this pattern
    
    # Check consolidation bar count
    box_bars = pattern_info.get('box_bars', 0)
    if box_bars < filters.get('min_consolidation_bars', 0):
        return True  # Skip this pattern
    
    # Check box width
    box_width_pct = pattern_info.get('box_width_pct', 0)
    if box_width_pct > filters.get('max_box_width', 1.0):
        return True  # Skip this pattern
    
    return False  # Don't skip

def display_pattern_results(ticker, pattern, confidence, info, levels, data, 
                           market_context, period, show_timing_adjustments, timeframe_info):
    """Display individual pattern results"""
    
    col1, col2 = st.columns([1, 2])
    
    with col1:
        # Confidence display
        if confidence >= 80:
            st.success(f"{pattern} DETECTED")
        elif confidence >= 70:
            st.success(f"{pattern} DETECTED")
        else:
            st.info(f"{pattern} DETECTED")
        
        # Display timing-adjusted confidence
        if show_timing_adjustments and 'timing_adjusted_confidence' in info:
            original_conf = info['original_confidence']
            adjusted_conf = info['timing_adjusted_confidence']
            if abs(original_conf - adjusted_conf) > 0.5:
                st.metric("Confidence", f"{confidence:.0f}%", 
                         f"{adjusted_conf - original_conf:+.0f}% (timing)")
            else:
                st.metric("Confidence", f"{confidence:.0f}%")
        else:
            st.metric("Confidence", f"{confidence:.0f}%")
        
        # Volume status
        display_volume_status(info)
        
        # Show confidence capping and timing adjustments
        display_adjustments(info, show_timing_adjustments)
        
        # Trading levels
        display_trading_levels(levels)
        
    with col2:
        # Pattern and market information
        display_pattern_info(pattern, info, levels, market_context)
    
    # Create and display chart
    fig = create_chart(data, ticker, pattern, info, levels, market_context, period)
    st.plotly_chart(fig, use_container_width=True)

def display_volume_status(info):
    """Display volume status with appropriate styling"""
    volume_status = info.get('volume_status', 'Unknown')
    if info.get('exceptional_volume'):
        st.success(f"{volume_status}")
    elif info.get('strong_volume'):
        st.success(f"{volume_status}")
    elif info.get('good_volume'):
        st.info(f"{volume_status}")
    else:
        st.warning(f"{volume_status}")

def display_adjustments(info, show_timing_adjustments):
    """Display confidence adjustments"""
    if info.get('confidence_capped'):
        st.warning(f"Capped: {info['confidence_capped']}")
    
    if show_timing_adjustments and 'timing_adjustments' in info:
        with st.expander("Timing Details"):
            for adjustment in info['timing_adjustments']:
                st.write(f"• {adjustment}")
    
    # Special warnings
    if info.get('friday_risk'):
        st.warning(f"{info['friday_risk']}")
    if info.get('monday_gap_check'):
        st.info(f"{info['monday_gap_check']}")

def display_trading_levels(levels):
    """Display trading levels"""
    st.write("**Trading Levels:**")
    st.write(f"**Entry**: ${levels['entry']:.2f}")
    st.write(f"**Stop**: ${levels['stop']:.2f}")
    st.write(f"**Target 1**: ${levels['target1']:.2f}")
    st.write(f"**Target 2**: ${levels['target2']:.2f}")
    if levels.get('has_target3'):
        st.write(f"**Target 3**: ${levels['target3']:.2f}")
    
    st.write("**Risk/Reward:**")
    st.write(f"**T1 R/R**: {levels['rr_ratio1']:.1f}:1")
    st.write(f"**T2 R/R**: {levels['rr_ratio2']:.1f}:1")
    if levels.get('has_target3'):
        st.write(f"**T3 R/R**: {levels['rr_ratio3']:.1f}:1")
    
    st.info(f"**Method**: {levels['target_method']}")

def display_pattern_info(pattern, info, levels, market_context):
    """Display pattern-specific information"""
    # Market timing context
    st.write("**Market Context:**")
    st.write(f"• **Gap Risk**: {market_context['gap_risk']}")
    st.write(f"• **Entry Timing**: {market_context['entry_timing']}")
    
    # Pattern-specific information
    if pattern == "Consolidation Breakout":
        display_consolidation_breakout_info(info, levels)
    elif pattern == "Inside Bar":
        display_inside_bar_info(info, levels)
    elif pattern == "Inverse Head Shoulders":
        display_inverse_head_shoulders_info(info, levels)
    else:
        display_standard_pattern_info(info, levels)
    
    # Technical indicators
    display_technical_info(info)

def display_consolidation_breakout_info(info, levels):
    """Display Consolidation Breakout specific information"""
    # Box characteristics
    if info.get('box_width_pct'):
        st.write(f"📦 Box width: {info['box_width_pct']:.1%}")
    if info.get('box_bars'):
        st.write(f"📊 Consolidation: {info['box_bars']} bars")
    
    # Consolidation criteria met
    criteria = info.get('consolidation_criteria', [])
    if criteria:
        criteria_display = {
            'low_atr': 'Low ATR volatility',
            'tight_bb': 'Tight Bollinger Bands', 
            'nr_cluster': 'NR4/NR7 cluster',
            'tight_box': 'Tight price box',
            'ma_pinch': 'MA convergence',
            'volume_dryup': 'Volume dry-up'
        }
        st.success("✅ **Criteria Met**:")
        for criterion in criteria:
            display_name = criteria_display.get(criterion, criterion)
            st.write(f"  • {display_name}")
    
    # Breakout status
    if info.get('breakout_confirmed'):
        st.success("🚀 **Full Breakout Confirmed**")
        st.write(f"  • {info.get('breakout_type', 'Complete confirmation')}")
    elif info.get('partial_breakout'):
        st.warning("⚡ **Partial Breakout**")
        st.write(f"  • {info.get('breakout_type', 'Partial confirmation')}")
    elif info.get('price_breakout_only'):
        st.info("📈 **Price Breakout Only**")
        st.write(f"  • {info.get('breakout_type', 'Awaiting volume/TR confirmation')}")
    
    # Technical details
    if info.get('tr_expansion'):
        st.write(f"📈 True Range: {info['tr_expansion']}")
    if info.get('vol_expansion'):
        st.write(f"📊 Volume: {info['vol_expansion']}")
    if info.get('vol_dryup_ratio'):
        st.write(f"🔇 Dry-up: {info['vol_dryup_ratio']} of bars")
    
    # Measured move target
    if 'measured_move_target' in levels:
        st.success(f"🎯 **Measured Move**: ${levels['measured_move_target']:.2f}")

def display_inverse_head_shoulders_info(info, levels):
    """Display Inverse Head and Shoulders specific information"""
    if info.get('head_depth_percent'):
        st.write(f"🔽 Head depth: {info['head_depth_percent']}")
        st.success(f"🎯 **Measured Move**: ${levels['reward1']:.2f}")
    if info.get('shoulder_symmetry_score'):
        st.write(f"⚖️ Symmetry: {info['shoulder_symmetry_score']}")
    if info.get('pattern_width_bars'):
        st.write(f"📏 Pattern width: {info['pattern_width_bars']} bars")
    if info.get('excellent_symmetry'):
        st.success("✅ Excellent shoulder symmetry")
    elif info.get('good_symmetry'):
        st.success("✅ Good shoulder symmetry")
    if info.get('ideal_downward_neckline'):
        st.success("✅ Ideal downward-sloping neckline")
    elif info.get('good_downward_neckline'):
        st.success("✅ Good downward neckline")
    if info.get('near_breakout'):
        st.success("🎯 Near neckline breakout")
    if info.get('classic_volume_pattern'):
        st.success("📊 Classic volume pattern confirmed")

def display_inside_bar_info(info, levels):
    """Display Inside Bar specific information"""
    if info.get('single_inside_bar'):
        st.write("Single inside bar (preferred)")
    elif info.get('double_inside_bar'):
        st.write("Double inside bar")
    if info.get('size_ratio'):
        st.write(f"Consolidation: {info['size_ratio']}")
    if info.get('tight_consolidation'):
        st.success("Tight consolidation")
    if info.get('color_validated'):
        st.success("Mother Bar: Green | Inside Bar: Red")
    st.success("**Triple Targets**: T1 Mother Bar, T2 +13%, T3 +21%")

def display_standard_pattern_info(info, levels):
    """Display information for standard patterns"""
    if info.get('initial_ascension'):
        st.write(f"🚀 Initial rise: {info['initial_ascension']}")
    if info.get('flagpole_gain'):
        st.write(f"🚀 Flagpole: {info['flagpole_gain']}")
        st.success(f"🎯 **Measured Move**: ${levels['reward1']:.2f}")
    if info.get('cup_depth'):
        st.write(f"☕ Cup depth: {info['cup_depth']}")
        st.success(f"🎯 **Measured Move**: ${levels['reward1']:.2f}")

def display_technical_info(info):
    """Display technical indicator information"""
    if info.get('macd_bullish'):
        st.write("📈 MACD bullish")
    if info.get('momentum_recovering'):
        st.write("📈 Momentum recovering")
    if info.get('near_breakout'):
        st.write("🎯 Near breakout")

def create_result_dict(ticker, pattern, confidence, info, levels, timeframe_info):
    """Create result dictionary for summary table"""
    result_dict = {
        'Ticker': ticker,
        'Pattern': pattern,
        'Timeframe': timeframe_info['display_name'],
        'Confidence': f"{confidence:.0f}%",
        'Volume': info.get('volume_status', 'Unknown'),
        'Entry': f"${levels['entry']:.2f}",
        'Stop': f"${levels['stop']:.2f}",
        'Target 1': f"${levels['target1']:.2f}",
        'Target 2': f"${levels['target2']:.2f}",
        'R/R 1': f"{levels['rr_ratio1']:.1f}:1",
        'R/R 2': f"{levels['rr_ratio2']:.1f}:1",
        'Risk': f"${levels['risk']:.2f}",
        'Method': levels['target_method']
    }
    
    # Add Target 3 for Inside Bar patterns
    if levels.get('has_target3'):
        result_dict['Target 3'] = f"${levels['target3']:.2f}"
        result_dict['R/R 3'] = f"{levels['rr_ratio3']:.1f}:1"
    
    # Add consolidation-specific info
    if pattern == "Consolidation Breakout":
        breakout_status = "✅ Confirmed" if info.get('breakout_confirmed') else "⚡ Partial" if info.get('partial_breakout') else "📈 Price Only"
        result_dict['Breakout'] = breakout_status
        if info.get('box_width_pct'):
            result_dict['Box Width'] = f"{info['box_width_pct']:.1%}"
    
    return result_dict

def display_summary(results, market_context):
    """Display analysis summary"""
    st.header("📋 Summary")
    df = pd.DataFrame(results)
    st.dataframe(df, use_container_width=True)
    
    # Summary metrics
    col1, col2, col3, col4, col5 = st.columns(5)
    with col1:
        st.metric("Total Patterns", len(results))
    with col2:
        scores = [int(r['Confidence'].replace('%', '')) for r in results]
        avg_score = sum(scores) / len(scores) if scores else 0
        st.metric("Avg Confidence", f"{avg_score:.0f}%")
    with col3:
        if results:
            ratios = [float(r['R/R 1'].split(':')[0]) for r in results]
            avg_rr = sum(ratios) / len(ratios) if ratios else 0
            st.metric("Avg R/R T1", f"{avg_rr:.1f}:1")
    with col4:
        high_vol_count = sum(1 for r in results if 'Strong' in r['Volume'] or 'Exceptional' in r['Volume'])
        vol_quality = (high_vol_count / len(results)) * 100 if results else 0
        st.metric("High Volume %", f"{vol_quality:.0f}%")
    with col5:
        consol_count = sum(1 for r in results if r['Pattern'] == 'Consolidation Breakout')
        st.metric("Consolidation", consol_count)
    
    # Pattern distribution
    if len(results) > 1:
        display_pattern_distribution(results)
    
    # Download results
    csv = df.to_csv(index=False)
    filename = EXPORT_FILENAME_FORMAT.format(timestamp=datetime.now().strftime('%Y%m%d_%H%M'))
    st.download_button(
        "📥 Download Results",
        csv,
        filename,
        "text/csv"
    )

def display_pattern_distribution(results):
    """Display pattern distribution statistics"""
    st.subheader("📊 Pattern Distribution")
    pattern_counts = {}
    timeframe_counts = {}
    breakout_status_counts = {}
    
    for result in results:
        pattern = result['Pattern']
        timeframe = result['Timeframe']
        pattern_counts[pattern] = pattern_counts.get(pattern, 0) + 1
        timeframe_counts[timeframe] = timeframe_counts.get(timeframe, 0) + 1
        
        # Track consolidation breakout status
        if pattern == 'Consolidation Breakout' and 'Breakout' in result:
            status = result['Breakout']
            breakout_status_counts[status] = breakout_status_counts.get(status, 0) + 1
    
    col1, col2, col3 = st.columns(3)
    with col1:
        st.write("**By Pattern:**")
        for pattern, count in pattern_counts.items():
            pct = (count / len(results)) * 100
            st.write(f"• {pattern}: {count} ({pct:.0f}%)")
    
    with col2:
        st.write("**By Timeframe:**")
        for timeframe, count in timeframe_counts.items():
            pct = (count / len(results)) * 100
            st.write(f"• {timeframe}: {count} ({pct:.0f}%)")
    
    with col3:
        if breakout_status_counts:
            st.write("**Breakout Status:**")
            for status, count in breakout_status_counts.items():
                st.write(f"• {status}: {count}")

if __name__ == "__main__":
    main()
