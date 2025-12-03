import streamlit as st
import plotly.graph_objects as go
import plotly.express as px
from agents.sentiment_agent import SentimentAgent
from agents.macro_agent import MacroEconomicAgent
from scrapers.news_scraper import NewsScraper
from utils.data_loader import SampleDataLoader
import pandas as pd
from datetime import datetime

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
</style>
""", unsafe_allow_html=True)

@st.cache_resource
def initialize_agents():
    """Initialize agents (cached)"""
    sentiment_agent = SentimentAgent()
    macro_agent = MacroEconomicAgent()
    return sentiment_agent, macro_agent

@st.cache_data
def load_sample_data():
    """Load sample data (cached)"""
    try:
        scraper = NewsScraper()
        news_data = scraper.load_from_json("./data/news/sample_news.json")
    except:
        scraper = NewsScraper()
        stocks = [
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
    "Dr. Reddy’s Laboratories Ltd.",
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
        news_data = scraper.scrape_multiple_sources(stocks, articles_per_stock=5)
        scraper.save_to_json(news_data, "./data/news/sample_news.json")
    
    try:
        economic_data = SampleDataLoader.load_from_csv()
    except:
        economic_data = SampleDataLoader.load_all_indicators()
        SampleDataLoader.save_to_csv(economic_data)
    
    return news_data, economic_data

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

def main():
    # Header
    st.markdown('<div class="main-header">📈 AI Stock Analysis Agents - NSE India</div>', 
                unsafe_allow_html=True)
    
    # Sidebar
    st.sidebar.title("🎯 Control Panel")
    page = st.sidebar.radio("Select Agent", 
                            ["🏠 Home", "😊 Sentiment Analysis", "📊 Macro Economic"])
    
    # Initialize
    with st.spinner("Initializing agents..."):
        sentiment_agent, macro_agent = initialize_agents()
        news_data, economic_data = load_sample_data()
        
        # Load data into agents
        sentiment_agent.load_news_data(news_data)
        macro_agent.load_economic_data(economic_data)
    
    # HOME PAGE
    if page == "🏠 Home":
        st.header("Welcome to AI Stock Analysis System")
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.subheader("📊 System Overview")
            st.info("""
            This system uses AI agents to analyze NSE India stocks:
            
            **Sentiment Analysis Agent**
            - Analyzes news sentiment using FinBERT
            - Provides buy/hold/sell recommendations
            - Tracks sentiment trends
            
            **Macro Economic Agent**
            - Analyzes economic indicators
            - Assesses market conditions
            - Provides outlook predictions
            """)
        
        with col2:
            st.subheader("📈 Quick Stats")
            stats = sentiment_agent.get_stats()
            
            st.metric("News Articles", stats['documents_count'])
            st.metric("Economic Indicators", len(economic_data))
            st.metric("Model", stats['model'])
        
        st.subheader("🚀 Getting Started")
        st.write("1. Select an agent from the sidebar")
        st.write("2. Choose a stock to analyze")
        st.write("3. View AI-powered insights and recommendations")
    
    # SENTIMENT ANALYSIS PAGE
    elif page == "😊 Sentiment Analysis":
        st.header("😊 Sentiment Analysis Agent")
        
        col1, col2 = st.columns([2, 1])
        
        with col1:
            stock = st.selectbox(
                "Select Stock",
                [
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
    "Dr. Reddy’s Laboratories Ltd.",
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
            )
        
        with col2:
            timeframe = st.selectbox("Timeframe", ["7d", "30d", "90d"])
        
        if st.button("🔍 Analyze Sentiment", type="primary"):
            with st.spinner(f"Analyzing {stock}..."):
                result = sentiment_agent.analyze(stock, timeframe, use_finbert=False)
                
                if "error" in result:
                    st.error(result["error"])
                else:
                    # Display results
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
                    
                    # Sample news
                    st.subheader("📰 Sample News Analyzed")
                    for i, news in enumerate(result['sample_news'], 1):
                        with st.expander(f"News {i}: {news['text'][:80]}..."):
                            st.write(news['text'])
                            st.write(f"**Sentiment:** {news['sentiment']}")
    
    # MACRO ECONOMIC PAGE
    elif page == "📊 Macro Economic":
        st.header("📊 Macro Economic Agent")
        
        col1, col2 = st.columns([2, 1])
        
        with col1:
            analysis_type = st.radio(
                "Analysis Type",
                ["General Market", "Stock-Specific"]
            )
        
        with col2:
            if analysis_type == "Stock-Specific":
                stock = st.selectbox(
                    "Select Stock",
                    [
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
    "Dr. Reddy’s Laboratories Ltd.",
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
                )
            else:
                stock = None
        
        if st.button("🔍 Analyze Economy", type="primary"):
            with st.spinner("Analyzing economic indicators..."):
                result = macro_agent.analyze(stock_name=stock)
                
                if "error" in result:
                    st.error(result["error"])
                else:
                    # Display results
                    st.success("Economic analysis complete")
                    
                    # Metrics row
                    col1, col2, col3 = st.columns(3)
                    
                    with col1:
                        health_score = result['economic_health_score']
                        color = ("🟢" if health_score > 70 
                               else "🔴" if health_score < 40 
                               else "🟡")
                        st.metric("Economic Health", f"{health_score:.0f}/100 {color}")
                    
                    with col2:
                        st.metric("Outlook", result['outlook'])
                    
                    with col3:
                        st.metric("Market Impact", result['market_impact'])
                    
                    # Key indicators
                    st.subheader("📈 Current Economic Indicators")
                    
                    indicators_df = []
                    for indicator, data in result['indicators'].items():
                        indicators_df.append({
                            'Indicator': data['name'],
                            'Value': f"{data['value']:.2f}",
                            'Trend': result['trends'].get(indicator, 'N/A'),
                            'Date': data['date']
                        })
                    
                    df = pd.DataFrame(indicators_df)
                    st.dataframe(df, use_container_width=True)
                    
                    # Charts
                    col1, col2 = st.columns(2)
                    
                    with col1:
                        # GDP Chart
                        if 'gdp_growth' in economic_data:
                            fig = create_indicator_chart(economic_data, 'gdp_growth')
                            st.plotly_chart(fig, use_container_width=True)
                    
                    with col2:
                        # Inflation Chart
                        if 'inflation_cpi' in economic_data:
                            fig = create_indicator_chart(economic_data, 'inflation_cpi')
                            st.plotly_chart(fig, use_container_width=True)
                    
                    # Key factors
                    st.subheader("🔑 Key Economic Factors")
                    for factor in result['key_factors']:
                        st.write(f"• {factor}")
                    
                    # AI Insight
                    st.subheader("💡 AI Economic Insight")
                    st.info(result['llm_insight'])
    
    # Footer
    st.sidebar.markdown("---")
    st.sidebar.info("""
    **About**
    
    AI-powered stock analysis system using:
    - Local LLMs (Ollama)
    - RAG with ChromaDB
    - FinBERT sentiment analysis
    
    Developed for MTech Applied AI Project
    """)

if __name__ == "__main__":
    main()