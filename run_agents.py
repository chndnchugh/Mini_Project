#!/usr/bin/env python3
"""
Main script to run the AI agents
"""

import sys
import os

# --- PATH FIX: ADD PROJECT ROOT TO SYSTEM PATH ---
# This ensures Python can find 'agents', 'scrapers', and 'utils'
PROJECT_ROOT = os.path.dirname(os.path.abspath(__file__))
if PROJECT_ROOT not in sys.path:
    sys.path.append(PROJECT_ROOT)
# ---------------------------------------------------

# NOW THE IMPORTS WILL WORK:
from agents.sentiment_agent import SentimentAgent
from agents.macro_agent import MacroEconomicAgent
from scrapers.news_scraper import NewsScraper # THIS LINE SHOULD NOW BE FOUND
from utils.data_loader import SampleDataLoader
import json

def print_banner():
    print("=" * 70)
    print("    AI STOCK ANALYSIS AGENTS - NSE INDIA")
    print("=" * 70)
    print()

def setup_data():
    """Setup sample data for testing"""
    print("\n📦 Setting up sample data...")
    
    # Create directories
    os.makedirs("./data/news", exist_ok=True)
    os.makedirs("./data/economic_data", exist_ok=True)
    
    # Generate and save economic data
    print("\n📊 Generating economic indicators...")
    economic_data = SampleDataLoader.load_all_indicators()
    SampleDataLoader.save_to_csv(economic_data)
    
    # Generate and save news data
    print("\n📰 Generating sample news...")
    scraper = NewsScraper()
    stocks = ["Reliance", "TCS", "Infosys", "HDFC Bank"]
    news_data = scraper.scrape_multiple_sources(stocks, articles_per_stock=5)
    scraper.save_to_json(news_data, "./data/news/sample_news.json")
    
    print("\n✓ Sample data setup complete!")
    return news_data, economic_data

def test_sentiment_agent(news_data):
    """Test Sentiment Analysis Agent"""
    print("\n" + "="*70)
    print("🧪 TESTING SENTIMENT ANALYSIS AGENT")
    print("="*70)
    
    try:
        # Initialize agent
        agent = SentimentAgent()
        
        # Load news data
        agent.load_news_data(news_data)
        
        # Analyze different stocks
        stocks_to_analyze = ["Reliance", "TCS", "HDFC Bank"]
        
        for stock in stocks_to_analyze:
            print(f"\n{'─'*70}")
            result = agent.analyze(stock, timeframe="30d", use_finbert=False)
            
            print(f"\n📈 Analysis for: {result['stock']}")
            print(f"   Timeframe: {result['timeframe']}")
            print(f"   Outlook: {result['outlook']}")
            print(f"   Recommendation: {result['recommendation']}")
            print(f"   Confidence: {result['confidence']:.2%}")
            
            print(f"\n   Sentiment Scores:")
            scores = result['sentiment_scores']
            print(f"   - Positive: {scores['positive']:.2%}")
            print(f"   - Negative: {scores['negative']:.2%}")
            print(f"   - Neutral: {scores['neutral']:.2%}")
            print(f"   - Compound: {scores['compound']:.3f}")
            
            print(f"\n   💡 AI Insight:")
            print(f"   {result['llm_insight'][:300]}...")
            
            print(f"\n   📰 Sample News Analyzed:")
            for i, news in enumerate(result['sample_news'][:2], 1):
                print(f"   {i}. {news['text'][:100]}...")
        
        print(f"\n✅ Sentiment Agent Test Complete!")
        return True
        
    except Exception as e:
        print(f"\n❌ Sentiment Agent Test Failed: {e}")
        import traceback
        traceback.print_exc()
        return False

def test_macro_agent(economic_data):
    """Test Macro Economic Agent"""
    print("\n" + "="*70)
    print("🧪 TESTING MACRO ECONOMIC AGENT")
    print("="*70)
    
    try:
        # Initialize agent
        agent = MacroEconomicAgent()
        
        # Load economic data
        agent.load_economic_data(economic_data)
        
        # Analyze overall economy
        print(f"\n{'─'*70}")
        print("\n📊 Overall Economic Analysis")
        result = agent.analyze()
        
        print(f"\n   Economic Health Score: {result['economic_health_score']:.1f}/100")
        print(f"   Outlook: {result['outlook']}")
        print(f"   Market Impact: {result['market_impact']}")
        
        print(f"\n   📈 Current Indicators:")
        for indicator, data in result['indicators'].items():
            print(f"   - {data['name']}: {data['value']:.2f}")
            print(f"     Trend: {result['trends'].get(indicator, 'N/A')}")
        
        print(f"\n   🔑 Key Factors:")
        for factor in result['key_factors']:
            print(f"   • {factor}")
        
        print(f"\n   💡 AI Insight:")
        print(f"   {result['llm_insight'][:400]}...")
        
        # Stock-specific analysis
        print(f"\n{'─'*70}")
        print("\n📊 Stock-Specific Analysis: Reliance")
        result = agent.analyze(stock_name="Reliance")
        
        print(f"\n   Stock: {result['stock']}")
        print(f"   Economic Health: {result['economic_health_score']:.1f}/100")
        print(f"   Market Impact: {result['market_impact']}")
        
        print(f"\n   💡 AI Insight:")
        print(f"   {result['llm_insight'][:300]}...")
        
        print(f"\n✅ Macro Agent Test Complete!")
        return True
        
    except Exception as e:
        print(f"\n❌ Macro Agent Test Failed: {e}")
        import traceback
        traceback.print_exc()
        return False

def interactive_mode():
    """Interactive mode for querying agents"""
    print("\n" + "="*70)
    print("🤖 INTERACTIVE MODE")
    print("="*70)
    print("\nAvailable commands:")
    print("  sentiment <stock_name>  - Analyze sentiment for a stock")
    print("  macro [stock_name]      - Analyze macro indicators")
    print("  stats                   - Show agent statistics")
    print("  quit                    - Exit")
    print()
    
    # Load data
    news_data = []
    economic_data = {}
    
    try:
        scraper = NewsScraper()
        news_data = scraper.load_from_json("./data/news/sample_news.json")
        economic_data = SampleDataLoader.load_from_csv()
    except:
        print("⚠ No existing data found. Generating new data...")
        news_data, economic_data = setup_data()
    
    # Initialize agents
    sentiment_agent = SentimentAgent()
    sentiment_agent.load_news_data(news_data)
    
    macro_agent = MacroEconomicAgent()
    macro_agent.load_economic_data(economic_data)
    
    print("\n✓ Agents ready!")
    
    while True:
        try:
            command = input("\n> ").strip().lower()
            
            if command == "quit":
                print("Goodbye! 👋")
                break
            
            elif command == "stats":
                print("\n📊 Agent Statistics:")
                print(f"   Sentiment Agent: {sentiment_agent.get_stats()}")
                print(f"   Macro Agent: {macro_agent.get_stats()}")
            
            elif command.startswith("sentiment"):
                parts = command.split(maxsplit=1)
                if len(parts) < 2:
                    print("Usage: sentiment <stock_name>")
                    continue
                
                stock = parts[1].title()
                result = sentiment_agent.analyze(stock)
                
                print(f"\n📈 {result['stock']} - {result['outlook']}")
                print(f"   Recommendation: {result['recommendation']}")
                print(f"   Compound Score: {result['sentiment_scores']['compound']:.3f}")
                print(f"\n   {result['llm_insight'][:200]}...")
            
            elif command.startswith("macro"):
                parts = command.split(maxsplit=1)
                stock = parts[1].title() if len(parts) > 1 else None
                
                result = macro_agent.analyze(stock_name=stock)
                
                print(f"\n📊 Economic Analysis")
                if stock:
                    print(f"   Stock: {stock}")
                print(f"   Health Score: {result['economic_health_score']:.1f}/100")
                print(f"   Outlook: {result['outlook']}")
                print(f"\n   {result['llm_insight'][:200]}...")
            
            else:
                print("Unknown command. Type 'quit' to exit.")
        
        except KeyboardInterrupt:
            print("\nGoodbye! 👋")
            break
        except Exception as e:
            print(f"Error: {e}")

def main():
    print_banner()
    
    if len(sys.argv) > 1 and sys.argv[1] == "setup":
        setup_data()
        return
    
    if len(sys.argv) > 1 and sys.argv[1] == "interactive":
        interactive_mode()
        return
    
    # Run full test suite
    print("🚀 Starting Agent Tests...\n")
    
    # Setup data
    news_data, economic_data = setup_data()
    
    # Test agents
    sentiment_ok = test_sentiment_agent(news_data)
    macro_ok = test_macro_agent(economic_data)
    
    # Summary
    print("\n" + "="*70)
    print("📋 TEST SUMMARY")
    print("="*70)
    print(f"   Sentiment Agent: {'✅ PASS' if sentiment_ok else '❌ FAIL'}")
    print(f"   Macro Agent: {'✅ PASS' if macro_ok else '❌ FAIL'}")
    print("="*70)
    
    if sentiment_ok and macro_ok:
        print("\n🎉 All tests passed! Agents are ready to use.")
        print("\nNext steps:")
        print("  1. Run 'python run_agents.py interactive' for interactive mode")
        print("  2. Run 'streamlit run app.py' for web interface")
    else:
        print("\n⚠ Some tests failed. Please check the errors above.")

if __name__ == "__main__":
    main()