import streamlit as st
import plotly.graph_objects as go
import plotly.express as px
from agents.sentiment_agent import SentimentAgent
from agents.macro_agent import MacroEconomicAgent
from agents.valuation_agent import ValuationAgent
from agents.geopolitical_agent import GeopoliticalAgent
from agents.fundamental_agent import FundamentalAgent
from scrapers.news_scraper import NewsScraper
from utils.data_loader import SampleDataLoader
from utils.new_data_loaders import ValuationDataLoader, GeopoliticalDataLoader, FundamentalDataLoader
import pandas as pd
from datetime import datetime
import numpy as np

# Page configuration
st.set_page_config(
    page_title="AI Stock Analysis - NSE India",
    page_icon="📈",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS
st.markdown("""
<style>
    .main-header {
        font-size: 2.5rem;
        font-weight: bold;
        color: #1f77b4;
        text-align: center;
        padding: 1rem;
    }
    .metric-card {
        background-color: #f0f2f6;
        padding: 1rem;
        border-radius: 0.5rem;
        margin: 0.5rem 0;
    }
    .positive {color: #28a745;}
    .negative {color: #dc3545;}
    .neutral {color: #ffc107;}
    .agent-card {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        padding: 1rem;
        border-radius: 0.5rem;
        margin: 0.5rem 0;
    }
</style>
""", unsafe_allow_html=True)

# NSE 50 Stocks
NSE_50_STOCKS = [
    "Adani Enterprises Ltd.",
    "Adani Ports and Special Economic Zone Ltd.",
    "Apollo Hospitals Enterprise Ltd.",
    "Asian Paints Ltd.",
    "Axis Bank Ltd.",
    "Bajaj Auto Ltd.",
    "Bajaj Finance Ltd.",
    "Bajaj Finserv Ltd.",
    "Bharat Electronics Ltd.",
    "Bharti Airtel Ltd.",
    "Cipla Ltd.",
    "Coal India Ltd.",
    "Dr. Reddy's Laboratories Ltd.",
    "Eicher Motors Ltd.",
    "Grasim Industries Ltd.",
    "HCL Technologies Ltd.",
    "HDFC Bank Ltd.",
    "HDFC Life Insurance Co. Ltd.",
    "Hindalco Industries Ltd.",
    "Hindustan Unilever Ltd.",
    "ICICI Bank Ltd.",
    "InterGlobe Aviation Ltd. (IndiGo)",
    "Infosys Ltd.",
    "ITC Ltd.",
    "Jio Financial Services Ltd.",
    "JSW Steel Ltd.",
    "Kotak Mahindra Bank Ltd.",
    "Larsen & Toubro Ltd.",
    "Mahindra & Mahindra Ltd.",
    "Maruti Suzuki India Ltd.",
    "Max Healthcare Institute Ltd.",
    "Nestle India Ltd.",
    "NTPC Ltd.",
    "Oil & Natural Gas Corporation Ltd. (ONGC)",
    "Power Grid Corporation of India Ltd.",
    "Reliance Industries Ltd.",
    "SBI Life Insurance Company Ltd.",
    "Shriram Finance Ltd.",
    "State Bank of India (SBI)",
    "Sun Pharmaceutical Industries Ltd.",
    "Tata Consultancy Services Ltd. (TCS)",
    "Tata Consumer Products Ltd.",
    "Tata Motors Ltd.",
    "Tata Steel Ltd.",
    "Tech Mahindra Ltd.",
    "Titan Company Ltd.",
    "Trent Ltd.",
    "UltraTech Cement Ltd.",
    "Wipro Ltd.",
    "Zomato Ltd."
]

@st.cache_resource
def initialize_agents():
    """Initialize all agents (cached)"""
    sentiment_agent = SentimentAgent()
    macro_agent = MacroEconomicAgent()
    valuation_agent = ValuationAgent()
    geo_agent = GeopoliticalAgent()
    fundamental_agent = FundamentalAgent()
    return sentiment_agent, macro_agent, valuation_agent, geo_agent, fundamental_agent

@st.cache_data
def load_sample_data():
    """Load sample data for all agents (cached)"""
    # News data
    try:
        scraper = NewsScraper()
        news_data = scraper.load_from_json("./data/news/sample_news.json")
    except:
        scraper = NewsScraper()
        stocks = ["Reliance", "TCS", "Infosys", "HDFC Bank"]
        news_data = scraper.scrape_multiple_sources(stocks, articles_per_stock=5)
        scraper.save_to_json(news_data, "./data/news/sample_news.json")
    
    # Economic data
    try:
        economic_data = SampleDataLoader.load_from_csv()
    except:
        economic_data = SampleDataLoader.load_all_indicators()
        SampleDataLoader.save_to_csv(economic_data)
    
    # Valuation data - generate for all NSE 50 stocks
    valuation_stocks = NSE_50_STOCKS
    valuation_data = ValuationDataLoader.generate_valuation_data(valuation_stocks)
    price_data = ValuationDataLoader.generate_price_data(valuation_stocks)
    
    # Geopolitical data
    try:
        geo_events = GeopoliticalDataLoader.load_from_json("./data/geopolitical/events.json")
    except:
        geo_events = GeopoliticalDataLoader.generate_sample_events()
        GeopoliticalDataLoader.save_to_json(geo_events)
    
    # Fundamental data - generate for all NSE 50 stocks
    quarterly_data = FundamentalDataLoader.generate_quarterly_data(valuation_stocks)
    annual_data = FundamentalDataLoader.generate_annual_data(valuation_stocks)
    
    return news_data, economic_data, valuation_data, price_data, geo_events, quarterly_data, annual_data

def create_sentiment_gauge(compound_score):
    """Create a gauge chart for sentiment"""
    fig = go.Figure(go.Indicator(
        mode="gauge+number+delta",
        value=compound_score,
        domain={'x': [0, 1], 'y': [0, 1]},
        title={'text': "Sentiment Score"},
        delta={'reference': 0},
        gauge={
            'axis': {'range': [-1, 1]},
            'bar': {'color': "darkblue"},
            'steps': [
                {'range': [-1, -0.3], 'color': "lightcoral"},
                {'range': [-0.3, 0.3], 'color': "lightyellow"},
                {'range': [0.3, 1], 'color': "lightgreen"}
            ],
            'threshold': {
                'line': {'color': "red", 'width': 4},
                'thickness': 0.75,
                'value': 0
            }
        }
    ))
    fig.update_layout(height=300)
    return fig

def create_indicator_chart(economic_data, indicator):
    """Create line chart for economic indicator"""
    if indicator not in economic_data:
        return None
    
    df = economic_data[indicator]
    fig = px.line(df, x='date', y='value', 
                  title=f"{indicator.replace('_', ' ').title()} Trend")
    fig.update_layout(height=300)
    return fig

def create_score_gauge(score, title, max_val=100):
    """Create a score gauge"""
    if score >= 70:
        color = "green"
    elif score >= 40:
        color = "orange"
    else:
        color = "red"
    
    fig = go.Figure(go.Indicator(
        mode="gauge+number",
        value=score,
        domain={'x': [0, 1], 'y': [0, 1]},
        title={'text': title},
        gauge={
            'axis': {'range': [0, max_val]},
            'bar': {'color': color},
            'steps': [
                {'range': [0, 40], 'color': "lightcoral"},
                {'range': [40, 70], 'color': "lightyellow"},
                {'range': [70, 100], 'color': "lightgreen"}
            ]
        }
    ))
    fig.update_layout(height=250)
    return fig

def create_technical_chart(indicators):
    """Create technical indicators visualization"""
    if not indicators:
        return None
    
    # Filter out None values
    valid_indicators = {k: v for k, v in indicators.items() if v is not None}
    
    if not valid_indicators:
        return None
    
    fig = go.Figure()
    
    # RSI subplot
    if 'rsi' in valid_indicators:
        fig.add_trace(go.Indicator(
            mode="gauge+number",
            value=valid_indicators['rsi'],
            title={'text': "RSI"},
            domain={'row': 0, 'column': 0},
            gauge={
                'axis': {'range': [0, 100]},
                'bar': {'color': "blue"},
                'steps': [
                    {'range': [0, 30], 'color': "green"},
                    {'range': [30, 70], 'color': "gray"},
                    {'range': [70, 100], 'color': "red"}
                ]
            }
        ))
    
    fig.update_layout(height=300)
    return fig

def main():
    # Header
    st.markdown('<div class="main-header">📈 AI Stock Analysis Agents - NSE India</div>', 
                unsafe_allow_html=True)
    st.markdown('<p style="text-align:center">Complete Multi-Agent System with 5 Specialized AI Agents</p>',
                unsafe_allow_html=True)
    
    # Sidebar
    st.sidebar.title("🎯 Control Panel")
    page = st.sidebar.radio("Select Agent", 
                            ["🏠 Home", 
                             "😊 Sentiment Analysis", 
                             "📊 Macro Economic",
                             "💰 Valuation & Technical",
                             "🌍 Geopolitical Analysis",
                             "📈 Fundamental Analysis",
                             "🔍 Comprehensive Analysis"])
    
    # Initialize
    with st.spinner("Initializing agents..."):
        sentiment_agent, macro_agent, valuation_agent, geo_agent, fundamental_agent = initialize_agents()
        news_data, economic_data, valuation_data, price_data, geo_events, quarterly_data, annual_data = load_sample_data()
        
        # Load data into agents
        sentiment_agent.load_news_data(news_data)
        macro_agent.load_economic_data(economic_data)
        valuation_agent.load_valuation_data(valuation_data)
        valuation_agent.load_price_data(price_data)
        geo_agent.load_geopolitical_events(geo_events)
        fundamental_agent.load_quarterly_data(quarterly_data)
        fundamental_agent.load_annual_data(annual_data)
    
    # HOME PAGE
    if page == "🏠 Home":
        st.header("Welcome to AI Stock Analysis System")
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.subheader("📊 System Overview")
            st.info("""
            This system uses 5 AI agents to analyze NSE India stocks:
            
            **1. Sentiment Analysis Agent**
            - Analyzes news sentiment using FinBERT/VADER
            - Provides buy/hold/sell recommendations
            
            **2. Macro Economic Agent**
            - Analyzes 8 key economic indicators
            - Assesses market conditions
            
            **3. Valuation & Technical Agent**
            - Technical indicators (RSI, MACD, Bollinger)
            - Valuation metrics (P/E, P/B, PEG)
            
            **4. Geopolitical Agent**
            - Tracks tariffs, G20, conflicts
            - Analyzes policy changes impact
            
            **5. Fundamental Agent**
            - Quarterly/Annual report analysis
            - Financial ratios & growth trends
            """)
        
        with col2:
            st.subheader("📈 Quick Stats")
            
            # Agent stats
            col_a, col_b = st.columns(2)
            with col_a:
                st.metric("News Articles", sentiment_agent.get_stats()['documents_count'])
                st.metric("Geo Events", len(geo_events))
            with col_b:
                st.metric("Economic Indicators", len(economic_data))
                st.metric("Stocks Tracked", len(valuation_data))
            
            st.metric("LLM Model", sentiment_agent.get_stats()['model'])
        
        st.subheader("🚀 Getting Started")
        st.write("1. Select an agent from the sidebar")
        st.write("2. Choose a stock to analyze")
        st.write("3. View AI-powered insights and recommendations")
        
        # Quick Analysis Cards - ALL 5 AGENTS
        st.subheader("🎯 Quick Analysis")
        quick_stock = st.selectbox("Select stock for quick analysis", NSE_50_STOCKS)
        
        if st.button("⚡ Quick Scan", type="primary"):
            
            # Row 1: Sentiment, Economic Health, Geo Risk
            col1, col2, col3 = st.columns(3)
            
            with col1:
                with st.spinner("Analyzing sentiment..."):
                    short_name = quick_stock.split()[0]
                    sent_result = sentiment_agent.analyze(short_name, use_finbert=False)
                    st.metric("😊 Sentiment", sent_result['outlook'], 
                             f"{sent_result['sentiment_scores']['compound']:.2f}")
            
            with col2:
                with st.spinner("Analyzing macro..."):
                    macro_result = macro_agent.analyze()
                    st.metric("📊 Economic Health", f"{macro_result['economic_health_score']:.0f}/100",
                             macro_result['outlook'])
            
            with col3:
                with st.spinner("Analyzing geo risk..."):
                    geo_result = geo_agent.analyze(stock_name=quick_stock)
                    risk = geo_result.get('risk_assessment', {})
                    st.metric("🌍 Geo Risk", f"{risk.get('overall_risk_score', 0):.0f}/100",
                             risk.get('risk_level', 'N/A'))
            
            # Row 2: Valuation and Fundamental
            col4, col5 = st.columns(2)
            
            with col4:
                with st.spinner("Analyzing valuation..."):
                    try:
                        val_result = valuation_agent.analyze(quick_stock)
                        if 'upside_potential' in val_result:
                            upside = val_result['upside_potential']
                            rating = val_result.get('valuation_rating', 'N/A')
                            st.metric("💰 Valuation", rating, f"{upside:.1f}% upside")
                        else:
                            st.metric("💰 Valuation", "N/A", "No data")
                    except Exception as e:
                        st.metric("💰 Valuation", "Error", str(e)[:20])
            
            with col5:
                with st.spinner("Analyzing fundamentals..."):
                    try:
                        fund_result = fundamental_agent.analyze(quick_stock)
                        score = fund_result.get('fundamental_score', {})
                        overall = score.get('overall_score', 0)
                        rating = score.get('rating', 'N/A')
                        st.metric("📈 Fundamental", f"{overall:.0f}/100", rating)
                    except Exception as e:
                        st.metric("📈 Fundamental", "Error", str(e)[:20])
            
            # Technical Indicators Summary
            st.subheader("📊 Technical Indicators")
            try:
                if 'technical_analysis' in val_result and isinstance(val_result['technical_analysis'], dict):
                    tech = val_result['technical_analysis']
                    tech_col1, tech_col2, tech_col3, tech_col4 = st.columns(4)
                    
                    indicators = tech.get('indicators', {})
                    
                    with tech_col1:
                        rsi = indicators.get('rsi')
                        if rsi:
                            rsi_status = "Oversold" if rsi < 30 else "Overbought" if rsi > 70 else "Neutral"
                            st.metric("RSI", f"{rsi:.1f}", rsi_status)
                        else:
                            st.metric("RSI", "N/A", "")
                    
                    with tech_col2:
                        macd = indicators.get('macd')
                        if macd:
                            macd_status = "Bullish" if macd > 0 else "Bearish"
                            st.metric("MACD", f"{macd:.2f}", macd_status)
                        else:
                            st.metric("MACD", "N/A", "")
                    
                    with tech_col3:
                        st.metric("Tech Rating", tech.get('technical_rating', 'N/A'), 
                                 f"{tech.get('buy_signals', 0)} buy / {tech.get('sell_signals', 0)} sell")
                    
                    with tech_col4:
                        if 'recommendation' in val_result:
                            rec = val_result['recommendation']
                            st.metric("Recommendation", rec.get('action', 'N/A'),
                                     f"{rec.get('confidence', 0):.0%} confidence")
            except:
                st.write("Technical analysis data not available")
            
            # Combined Score
            st.subheader("🎯 Combined Analysis Score")
            
            try:
                scores = []
                
                # Sentiment score (convert -1 to 1 -> 0 to 100)
                compound = sent_result.get('sentiment_scores', {}).get('compound', 0)
                sent_score = (compound + 1) * 50
                scores.append(('Sentiment', sent_score))
                
                # Macro score
                macro_score = macro_result.get('economic_health_score', 50)
                scores.append(('Macro', macro_score))
                
                # Geo score (inverse - lower risk is better)
                geo_risk = risk.get('overall_risk_score', 50)
                geo_score = 100 - geo_risk
                scores.append(('Geopolitical', geo_score))
                
                # Valuation score
                if 'upside_potential' in val_result:
                    upside = val_result['upside_potential']
                    val_score = min(max(50 + upside, 0), 100)
                    scores.append(('Valuation', val_score))
                
                # Fundamental score
                fund_score = fund_result.get('fundamental_score', {}).get('overall_score', 50)
                scores.append(('Fundamental', fund_score))
                
                # Calculate combined score
                combined_score = np.mean([s[1] for s in scores])
                
                # Display combined score
                score_col1, score_col2 = st.columns([1, 2])
                
                with score_col1:
                    if combined_score >= 70:
                        action = "🟢 STRONG BUY"
                        color = "green"
                    elif combined_score >= 55:
                        action = "🟢 BUY"
                        color = "lightgreen"
                    elif combined_score >= 45:
                        action = "🟡 HOLD"
                        color = "orange"
                    elif combined_score >= 30:
                        action = "🔴 SELL"
                        color = "red"
                    else:
                        action = "🔴 STRONG SELL"
                        color = "darkred"
                    
                    st.markdown(f"### Combined Score: {combined_score:.0f}/100")
                    st.markdown(f"### {action}")
                
                with score_col2:
                    # Create bar chart for score breakdown
                    score_df = pd.DataFrame(scores, columns=['Agent', 'Score'])
                    fig = px.bar(score_df, x='Agent', y='Score', 
                                color='Score',
                                color_continuous_scale=['red', 'yellow', 'green'],
                                range_color=[0, 100])
                    fig.update_layout(height=250, showlegend=False)
                    fig.add_hline(y=combined_score, line_dash="dash", 
                                 annotation_text=f"Combined: {combined_score:.0f}")
                    st.plotly_chart(fig, use_container_width=True)
                    
            except Exception as e:
                st.error(f"Error calculating combined score: {e}")
    
    # SENTIMENT ANALYSIS PAGE
    elif page == "😊 Sentiment Analysis":
        st.header("😊 Sentiment Analysis Agent")
        
        col1, col2 = st.columns([2, 1])
        
        with col1:
            stock = st.selectbox("Select Stock", NSE_50_STOCKS)
        
        with col2:
            timeframe = st.selectbox("Timeframe", ["7d", "30d", "90d"])
        
        if st.button("🔍 Analyze Sentiment", type="primary"):
            with st.spinner(f"Analyzing {stock}..."):
                short_name = stock.split()[0]
                result = sentiment_agent.analyze(short_name, timeframe, use_finbert=False)
                
                if "error" in result:
                    st.error(result["error"])
                else:
                    st.success(f"Analysis complete for {result['stock']}")
                    
                    # Metrics row
                    col1, col2, col3, col4 = st.columns(4)
                    
                    with col1:
                        outlook_color = ("positive" if result['outlook'] == "Bullish" 
                                       else "negative" if result['outlook'] == "Bearish" 
                                       else "neutral")
                        st.markdown(f"### Outlook\n### <span class='{outlook_color}'>{result['outlook']}</span>", 
                                   unsafe_allow_html=True)
                    
                    with col2:
                        st.metric("Recommendation", result['recommendation'])
                    
                    with col3:
                        st.metric("Confidence", f"{result['confidence']:.1%}")
                    
                    with col4:
                        st.metric("News Analyzed", result['total_news_analyzed'])
                    
                    # Sentiment gauge
                    st.plotly_chart(
                        create_sentiment_gauge(result['sentiment_scores']['compound']),
                        use_container_width=True
                    )
                    
                    # Sentiment breakdown
                    col1, col2 = st.columns(2)
                    
                    with col1:
                        st.subheader("📊 Sentiment Breakdown")
                        scores = result['sentiment_scores']
                        df = pd.DataFrame({
                            'Sentiment': ['Positive', 'Negative', 'Neutral'],
                            'Score': [scores['positive'], scores['negative'], scores['neutral']]
                        })
                        fig = px.bar(df, x='Sentiment', y='Score', color='Sentiment',
                                    color_discrete_map={
                                        'Positive': 'green',
                                        'Negative': 'red',
                                        'Neutral': 'gray'
                                    })
                        st.plotly_chart(fig, use_container_width=True)
                    
                    with col2:
                        st.subheader("💡 AI Insight")
                        st.info(result['llm_insight'])
    
    # MACRO ECONOMIC PAGE
    elif page == "📊 Macro Economic":
        st.header("📊 Macro Economic Agent")
        
        col1, col2 = st.columns([2, 1])
        
        with col1:
            analysis_type = st.radio("Analysis Type", ["General Market", "Stock-Specific"])
        
        with col2:
            if analysis_type == "Stock-Specific":
                stock = st.selectbox("Select Stock", NSE_50_STOCKS)
            else:
                stock = None
        
        if st.button("🔍 Analyze Economy", type="primary"):
            with st.spinner("Analyzing economic indicators..."):
                result = macro_agent.analyze(stock_name=stock)
                
                if "error" in result:
                    st.error(result["error"])
                else:
                    st.success("Economic analysis complete")
                    
                    # Metrics row
                    col1, col2, col3 = st.columns(3)
                    
                    with col1:
                        health_score = result['economic_health_score']
                        st.plotly_chart(create_score_gauge(health_score, "Economic Health"), 
                                       use_container_width=True)
                    
                    with col2:
                        st.metric("Outlook", result['outlook'])
                        st.metric("Market Impact", result['market_impact'])
                    
                    with col3:
                        st.subheader("🔑 Key Factors")
                        for factor in result['key_factors']:
                            st.write(f"• {factor}")
                    
                    # Indicator charts
                    col1, col2 = st.columns(2)
                    
                    with col1:
                        if 'gdp_growth' in economic_data:
                            fig = create_indicator_chart(economic_data, 'gdp_growth')
                            st.plotly_chart(fig, use_container_width=True)
                    
                    with col2:
                        if 'inflation_cpi' in economic_data:
                            fig = create_indicator_chart(economic_data, 'inflation_cpi')
                            st.plotly_chart(fig, use_container_width=True)
                    
                    # AI Insight
                    st.subheader("💡 AI Economic Insight")
                    st.info(result['llm_insight'])
    
    # VALUATION & TECHNICAL PAGE
    elif page == "💰 Valuation & Technical":
        st.header("💰 Valuation & Technical Analysis Agent")
        
        stock = st.selectbox("Select Stock", NSE_50_STOCKS)
        
        if st.button("🔍 Analyze Valuation", type="primary"):
            with st.spinner(f"Analyzing {stock}..."):
                result = valuation_agent.analyze(stock)
                
                if "error" in result:
                    st.error(result.get("error", "Analysis failed"))
                else:
                    st.success(f"Analysis complete for {result['stock']}")
                    
                    # Key metrics
                    col1, col2, col3, col4 = st.columns(4)
                    
                    with col1:
                        if 'current_price' in result:
                            st.metric("Current Price", f"₹{result['current_price']:.2f}")
                    
                    with col2:
                        if 'fair_value' in result:
                            st.metric("Fair Value", f"₹{result['fair_value']:.2f}")
                    
                    with col3:
                        if 'upside_potential' in result:
                            upside = result['upside_potential']
                            st.metric("Upside Potential", f"{upside:.1f}%",
                                     delta=f"{upside:.1f}%")
                    
                    with col4:
                        if 'valuation_rating' in result:
                            st.metric("Rating", result['valuation_rating'])
                    
                    # Technical Analysis
                    st.subheader("📊 Technical Analysis")
                    
                    if 'technical_analysis' in result and isinstance(result['technical_analysis'], dict):
                        tech = result['technical_analysis']
                        
                        col1, col2 = st.columns(2)
                        
                        with col1:
                            st.write(f"**Technical Rating:** {tech.get('technical_rating', 'N/A')}")
                            st.write(f"**Buy Signals:** {tech.get('buy_signals', 0)}")
                            st.write(f"**Sell Signals:** {tech.get('sell_signals', 0)}")
                            
                            # Signals table
                            if 'signals' in tech:
                                st.write("**Signal Details:**")
                                for signal in tech['signals']:
                                    emoji = "🟢" if signal['action'] == 'Buy' else "🔴" if signal['action'] == 'Sell' else "🟡"
                                    st.write(f"{emoji} {signal['indicator']}: {signal['signal']} ({signal['action']})")
                        
                        with col2:
                            indicators = tech.get('indicators', {})
                            if indicators:
                                st.write("**Key Indicators:**")
                                for ind, val in indicators.items():
                                    if val is not None:
                                        st.write(f"• {ind.upper()}: {val:.2f}")
                    
                    # Support/Resistance
                    if 'technical_analysis' in result and 'support_resistance' in result['technical_analysis']:
                        st.subheader("📍 Support & Resistance")
                        sr = result['technical_analysis']['support_resistance']
                        col1, col2 = st.columns(2)
                        with col1:
                            st.write(f"**Support 1:** ₹{sr.get('support_1', 0):.2f}")
                            st.write(f"**Support 2:** ₹{sr.get('support_2', 0):.2f}")
                        with col2:
                            st.write(f"**Resistance 1:** ₹{sr.get('resistance_1', 0):.2f}")
                            st.write(f"**Resistance 2:** ₹{sr.get('resistance_2', 0):.2f}")
                    
                    # Recommendation
                    if 'recommendation' in result:
                        rec = result['recommendation']
                        st.subheader("📝 Recommendation")
                        st.write(f"**Action:** {rec.get('action', 'N/A')}")
                        st.write(f"**Confidence:** {rec.get('confidence', 0):.1%}")
                    
                    # AI Insight
                    st.subheader("💡 AI Insight")
                    st.info(result.get('ai_insight', 'No insight available'))
    
    # GEOPOLITICAL PAGE
    elif page == "🌍 Geopolitical Analysis":
        st.header("🌍 Geopolitical Analysis Agent")
        
        col1, col2 = st.columns([2, 1])
        
        with col1:
            stock = st.selectbox("Select Stock", NSE_50_STOCKS)
        
        with col2:
            timeframe = st.selectbox("Analysis Period", ["30d", "90d", "180d"])
        
        if st.button("🔍 Analyze Geopolitical Factors", type="primary"):
            with st.spinner(f"Analyzing geopolitical factors for {stock}..."):
                result = geo_agent.analyze(stock_name=stock, timeframe=timeframe)
                
                st.success(f"Analysis complete for {result['stock']}")
                
                # Risk Assessment
                risk = result.get('risk_assessment', {})
                
                col1, col2, col3 = st.columns(3)
                
                with col1:
                    st.plotly_chart(
                        create_score_gauge(risk.get('overall_risk_score', 0), "Risk Score"),
                        use_container_width=True
                    )
                
                with col2:
                    st.metric("Risk Level", risk.get('risk_level', 'N/A'))
                    st.metric("Market Outlook", risk.get('market_outlook', 'N/A'))
                    st.metric("Sector", result.get('sector', 'N/A'))
                
                with col3:
                    st.subheader("🔑 Key Risk Factors")
                    for factor in risk.get('key_risk_factors', [])[:5]:
                        st.write(f"⚠️ {factor}")
                
                # Event Summary
                event_summary = result.get('event_summary', {})
                if event_summary:
                    st.subheader("📰 Event Summary")
                    
                    col1, col2 = st.columns(2)
                    
                    with col1:
                        st.write(f"**Total Events:** {event_summary.get('total_events', 0)}")
                        impact = event_summary.get('impact_distribution', {})
                        st.write(f"**High Impact:** {impact.get('high', 0)}")
                        st.write(f"**Medium Impact:** {impact.get('medium', 0)}")
                        st.write(f"**Low Impact:** {impact.get('low', 0)}")
                    
                    with col2:
                        concerns = event_summary.get('top_concerns', [])
                        if concerns:
                            st.write("**Top Concerns:**")
                            for concern in concerns[:3]:
                                st.write(f"• {concern['category']}: {concern['severity']}")
                
                # Recommendation
                rec = result.get('recommendation', {})
                st.subheader("📝 Recommendation")
                col1, col2 = st.columns(2)
                with col1:
                    st.write(f"**Action:** {rec.get('action', 'N/A')}")
                    st.write(f"**Strategy:** {rec.get('strategy', 'N/A')}")
                with col2:
                    st.write(f"**Portfolio Suggestion:** {rec.get('portfolio_suggestion', 'N/A')}")
                
                # AI Insight
                st.subheader("💡 AI Insight")
                st.info(result.get('ai_insight', 'No insight available'))
    
    # FUNDAMENTAL ANALYSIS PAGE
    elif page == "📈 Fundamental Analysis":
        st.header("📈 Fundamental Analysis Agent")
        
        col1, col2 = st.columns([2, 1])
        
        with col1:
            stock = st.selectbox("Select Stock", NSE_50_STOCKS)
        
        with col2:
            period = st.selectbox("Analysis Period", ["quarterly", "annual"])
        
        if st.button("🔍 Analyze Fundamentals", type="primary"):
            with st.spinner(f"Analyzing fundamentals for {stock}..."):
                result = fundamental_agent.analyze(stock, period=period)
                
                if "error" in result:
                    st.error(result["error"])
                else:
                    st.success(f"Analysis complete for {result['stock']}")
                    
                    # Fundamental Score
                    score = result.get('fundamental_score', {})
                    
                    col1, col2, col3 = st.columns(3)
                    
                    with col1:
                        st.plotly_chart(
                            create_score_gauge(score.get('overall_score', 0), "Fundamental Score"),
                            use_container_width=True
                        )
                    
                    with col2:
                        st.metric("Rating", score.get('rating', 'N/A'))
                        
                        # Component scores
                        st.write("**Component Scores:**")
                        for comp, comp_score in score.get('component_scores', {}).items():
                            st.write(f"• {comp.title()}: {comp_score:.0f}")
                    
                    with col3:
                        rec = result.get('recommendation', {})
                        st.metric("Recommendation", rec.get('action', 'N/A'))
                        st.metric("Confidence", f"{rec.get('confidence', 0):.0%}")
                    
                    # Financial Performance
                    st.subheader("📊 Financial Performance")
                    
                    perf = result.get('financial_performance', {})
                    latest = perf.get('latest_period', {})
                    
                    if latest:
                        cols = st.columns(4)
                        metrics = list(latest.items())[:4]
                        for i, (metric, data) in enumerate(metrics):
                            with cols[i]:
                                st.metric(data.get('label', metric)[:20], 
                                         f"{data.get('value', 0):.2f}")
                    
                    # Growth Analysis
                    growth = result.get('growth_analysis', {})
                    
                    col1, col2 = st.columns(2)
                    
                    with col1:
                        st.subheader("📈 Growth Metrics")
                        if growth.get('revenue_cagr'):
                            st.write(f"**Revenue CAGR:** {growth['revenue_cagr']:.1f}%")
                        if growth.get('profit_cagr'):
                            st.write(f"**Profit CAGR:** {growth['profit_cagr']:.1f}%")
                        if growth.get('eps_cagr'):
                            st.write(f"**EPS CAGR:** {growth['eps_cagr']:.1f}%")
                        st.write(f"**Growth Consistency:** {growth.get('growth_consistency', 'N/A')}")
                    
                    with col2:
                        st.subheader("✅ Quality Assessment")
                        quality = result.get('quality_assessment', {})
                        st.write(f"**Quality Score:** {quality.get('quality_score', 0):.0f}/100")
                        if quality.get('cash_conversion'):
                            st.write(f"**Cash Conversion:** {quality['cash_conversion']:.0f}%")
                        st.write(f"**Earnings Persistence:** {quality.get('earnings_persistence', 'N/A')}")
                        
                        flags = quality.get('flags', [])
                        if flags:
                            st.write("**Flags:**")
                            for flag in flags:
                                st.write(f"⚠️ {flag}")
                    
                    # AI Insight
                    st.subheader("💡 AI Insight")
                    st.info(result.get('ai_insight', 'No insight available'))
    
    # COMPREHENSIVE ANALYSIS PAGE
    elif page == "🔍 Comprehensive Analysis":
        st.header("🔍 Comprehensive Analysis - All Agents")
        
        stock = st.selectbox("Select Stock for Full Analysis", NSE_50_STOCKS)
        
        if st.button("🚀 Run Full Analysis", type="primary"):
            progress = st.progress(0)
            status = st.empty()
            
            results = {}
            
            # Sentiment
            status.text("Analyzing sentiment...")
            progress.progress(10)
            short_name = stock.split()[0]
            results['sentiment'] = sentiment_agent.analyze(short_name, use_finbert=False)
            
            # Macro
            status.text("Analyzing macro economics...")
            progress.progress(30)
            results['macro'] = macro_agent.analyze(stock_name=stock)
            
            # Valuation
            status.text("Analyzing valuation...")
            progress.progress(50)
            results['valuation'] = valuation_agent.analyze(stock)
            
            # Geopolitical
            status.text("Analyzing geopolitical factors...")
            progress.progress(70)
            results['geopolitical'] = geo_agent.analyze(stock_name=stock)
            
            # Fundamental
            status.text("Analyzing fundamentals...")
            progress.progress(90)
            results['fundamental'] = fundamental_agent.analyze(stock)
            
            progress.progress(100)
            status.text("Analysis complete!")
            
            st.success(f"Comprehensive Analysis Complete for {stock}")
            
            # Summary Cards
            st.subheader("📊 Analysis Summary")
            
            col1, col2, col3, col4, col5 = st.columns(5)
            
            with col1:
                st.markdown("**😊 Sentiment**")
                sent = results['sentiment']
                st.metric("Outlook", sent.get('outlook', 'N/A'))
                st.write(f"Score: {sent.get('sentiment_scores', {}).get('compound', 0):.2f}")
            
            with col2:
                st.markdown("**📊 Macro**")
                macro = results['macro']
                st.metric("Health", f"{macro.get('economic_health_score', 0):.0f}")
                st.write(f"Impact: {macro.get('market_impact', 'N/A')}")
            
            with col3:
                st.markdown("**💰 Valuation**")
                val = results['valuation']
                st.metric("Rating", val.get('valuation_rating', 'N/A'))
                if 'upside_potential' in val:
                    st.write(f"Upside: {val['upside_potential']:.1f}%")
            
            with col4:
                st.markdown("**🌍 Geopolitical**")
                geo = results['geopolitical']
                risk = geo.get('risk_assessment', {})
                st.metric("Risk", risk.get('risk_level', 'N/A'))
                st.write(f"Score: {risk.get('overall_risk_score', 0):.0f}")
            
            with col5:
                st.markdown("**📈 Fundamental**")
                fund = results['fundamental']
                score = fund.get('fundamental_score', {})
                st.metric("Score", f"{score.get('overall_score', 0):.0f}")
                st.write(f"Rating: {score.get('rating', 'N/A')}")
            
            # Combined Recommendation
            st.subheader("🎯 Combined Recommendation")
            
            # Calculate combined score
            scores = []
            
            # Sentiment score
            compound = results['sentiment'].get('sentiment_scores', {}).get('compound', 0)
            scores.append(('Sentiment', (compound + 1) * 50))  # Convert -1 to 1 -> 0 to 100
            
            # Macro score
            scores.append(('Macro', results['macro'].get('economic_health_score', 50)))
            
            # Valuation score (based on upside)
            upside = results['valuation'].get('upside_potential', 0)
            val_score = min(max(50 + upside, 0), 100)
            scores.append(('Valuation', val_score))
            
            # Geopolitical (inverse - lower risk is better)
            geo_risk = results['geopolitical'].get('risk_assessment', {}).get('overall_risk_score', 50)
            scores.append(('Geopolitical', 100 - geo_risk))
            
            # Fundamental
            scores.append(('Fundamental', results['fundamental'].get('fundamental_score', {}).get('overall_score', 50)))
            
            # Calculate weighted average
            combined_score = np.mean([s[1] for s in scores])
            
            col1, col2 = st.columns(2)
            
            with col1:
                st.plotly_chart(create_score_gauge(combined_score, "Combined Score"), 
                               use_container_width=True)
            
            with col2:
                if combined_score >= 70:
                    action = "🟢 STRONG BUY"
                    rationale = "All indicators point to a favorable investment opportunity"
                elif combined_score >= 55:
                    action = "🟢 BUY"
                    rationale = "Most indicators are positive, consider accumulating"
                elif combined_score >= 45:
                    action = "🟡 HOLD"
                    rationale = "Mixed signals, maintain current position"
                elif combined_score >= 30:
                    action = "🔴 SELL"
                    rationale = "Multiple concerns identified, consider reducing exposure"
                else:
                    action = "🔴 STRONG SELL"
                    rationale = "Significant risks identified across multiple factors"
                
                st.markdown(f"### {action}")
                st.write(rationale)
                
                st.write("**Score Breakdown:**")
                for name, score in scores:
                    st.write(f"• {name}: {score:.0f}/100")
            
            # Detailed Insights
            st.subheader("💡 Detailed AI Insights")
            
            with st.expander("Sentiment Insight"):
                st.write(results['sentiment'].get('llm_insight', 'No insight available'))
            
            with st.expander("Macro Economic Insight"):
                st.write(results['macro'].get('llm_insight', 'No insight available'))
            
            with st.expander("Valuation Insight"):
                st.write(results['valuation'].get('ai_insight', 'No insight available'))
            
            with st.expander("Geopolitical Insight"):
                st.write(results['geopolitical'].get('ai_insight', 'No insight available'))
            
            with st.expander("Fundamental Insight"):
                st.write(results['fundamental'].get('ai_insight', 'No insight available'))
    
    # Footer
    st.sidebar.markdown("---")
    st.sidebar.info("""
    **About**
    
    AI-powered stock analysis system using:
    - Local LLMs (Ollama - Llama 3.2)
    - RAG with ChromaDB
    - FinBERT sentiment analysis
    - Technical indicators
    - Fundamental metrics
    
    **5 Specialized Agents:**
    1. Sentiment Analysis
    2. Macro Economic
    3. Valuation & Technical
    4. Geopolitical
    5. Fundamental Analysis
    
    Developed for MTech Applied AI Project
    """)

if __name__ == "__main__":
    main()