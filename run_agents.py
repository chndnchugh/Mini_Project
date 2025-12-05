#!/usr/bin/env python3
"""
Main script to run the AI agents - Updated with all 5 agents
"""

import sys
import os

# --- PATH FIX: ADD PROJECT ROOT TO SYSTEM PATH ---
PROJECT_ROOT = os.path.dirname(os.path.abspath(__file__))
if PROJECT_ROOT not in sys.path:
    sys.path.append(PROJECT_ROOT)
# ---------------------------------------------------

# Import all agents
from agents.sentiment_agent import SentimentAgent
from agents.macro_agent import MacroEconomicAgent
from agents.valuation_agent import ValuationAgent
from agents.geopolitical_agent import GeopoliticalAgent
from agents.fundamental_agent import FundamentalAgent

# Import data loaders
from scrapers.news_scraper import NewsScraper
from utils.data_loader import SampleDataLoader
from utils.new_data_loaders import ValuationDataLoader, GeopoliticalDataLoader, FundamentalDataLoader
import json

def print_banner():
    print("=" * 70)
    print("    AI STOCK ANALYSIS AGENTS - NSE INDIA")
    print("    Complete Multi-Agent System (5 Agents)")
    print("=" * 70)
    print()
    print("Available Agents:")
    print("  1. Sentiment Agent - News sentiment analysis")
    print("  2. Macro Economic Agent - Economic indicators analysis")
    print("  3. Valuation Agent - Technical & valuation analysis")
    print("  4. Geopolitical Agent - Global events impact analysis")
    print("  5. Fundamental Agent - Financial statements analysis")
    print()

def setup_data():
    """Setup sample data for all agents"""
    print("\n📦 Setting up sample data for all agents...")
    
    # Create directories
    os.makedirs("./data/news", exist_ok=True)
    os.makedirs("./data/economic_data", exist_ok=True)
    os.makedirs("./data/valuation", exist_ok=True)
    os.makedirs("./data/geopolitical", exist_ok=True)
    os.makedirs("./data/fundamentals/quarterly", exist_ok=True)
    os.makedirs("./data/fundamentals/annual", exist_ok=True)
    
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
    
    # Generate valuation data
    print("\n💰 Generating valuation data...")
    valuation_stocks = [
        "Reliance Industries Ltd.", 
        "Tata Consultancy Services Ltd. (TCS)",
        "HDFC Bank Ltd.",
        "Infosys Ltd.",
        "ICICI Bank Ltd."
    ]
    valuation_data = ValuationDataLoader.generate_valuation_data(valuation_stocks)
    price_data = ValuationDataLoader.generate_price_data(valuation_stocks, days=252)
    ValuationDataLoader.save_to_csv(valuation_data, "./data/valuation/metrics")
    ValuationDataLoader.save_to_csv(price_data, "./data/valuation/prices")
    
    # Generate geopolitical events
    print("\n🌍 Generating geopolitical events...")
    geo_events = GeopoliticalDataLoader.generate_sample_events()
    GeopoliticalDataLoader.save_to_json(geo_events, "./data/geopolitical/events.json")
    
    # Generate fundamental data
    print("\n📈 Generating fundamental data...")
    quarterly_data = FundamentalDataLoader.generate_quarterly_data(valuation_stocks)
    annual_data = FundamentalDataLoader.generate_annual_data(valuation_stocks)
    FundamentalDataLoader.save_to_csv(quarterly_data, annual_data, "./data/fundamentals")
    
    print("\n✓ All sample data setup complete!")
    return news_data, economic_data, valuation_data, price_data, geo_events, quarterly_data, annual_data

def test_sentiment_agent(news_data):
    """Test Sentiment Analysis Agent"""
    print("\n" + "="*70)
    print("🧪 TESTING SENTIMENT ANALYSIS AGENT")
    print("="*70)
    
    try:
        agent = SentimentAgent()
        agent.load_news_data(news_data)
        
        stocks_to_analyze = ["Reliance", "TCS"]
        
        for stock in stocks_to_analyze:
            print(f"\n{'─'*70}")
            result = agent.analyze(stock, timeframe="30d", use_finbert=False)
            
            print(f"\n📈 Analysis for: {result['stock']}")
            print(f"   Outlook: {result['outlook']}")
            print(f"   Recommendation: {result['recommendation']}")
            print(f"   Confidence: {result['confidence']:.2%}")
            print(f"   Compound Score: {result['sentiment_scores']['compound']:.3f}")
        
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
        agent = MacroEconomicAgent()
        agent.load_economic_data(economic_data)
        
        print(f"\n{'─'*70}")
        result = agent.analyze()
        
        print(f"\n   Economic Health Score: {result['economic_health_score']:.1f}/100")
        print(f"   Outlook: {result['outlook']}")
        print(f"   Market Impact: {result['market_impact']}")
        
        print(f"\n✅ Macro Agent Test Complete!")
        return True
        
    except Exception as e:
        print(f"\n❌ Macro Agent Test Failed: {e}")
        import traceback
        traceback.print_exc()
        return False

def test_valuation_agent(valuation_data, price_data):
    """Test Valuation Agent"""
    print("\n" + "="*70)
    print("🧪 TESTING VALUATION AGENT")
    print("="*70)
    
    try:
        agent = ValuationAgent()
        agent.load_valuation_data(valuation_data)
        agent.load_price_data(price_data)
        
        stock = "Reliance Industries Ltd."
        print(f"\n{'─'*70}")
        result = agent.analyze(stock)
        
        print(f"\n💰 Valuation Analysis for: {result['stock']}")
        
        if 'current_price' in result:
            print(f"   Current Price: ₹{result['current_price']:.2f}")
        if 'fair_value' in result:
            print(f"   Fair Value: ₹{result['fair_value']:.2f}")
        if 'upside_potential' in result:
            print(f"   Upside Potential: {result['upside_potential']:.1f}%")
        if 'valuation_rating' in result:
            print(f"   Valuation Rating: {result['valuation_rating']}")
        
        if 'technical_analysis' in result and isinstance(result['technical_analysis'], dict):
            tech = result['technical_analysis']
            print(f"\n   📊 Technical Analysis:")
            print(f"   Technical Rating: {tech.get('technical_rating', 'N/A')}")
            if 'indicators' in tech:
                indicators = tech['indicators']
                if indicators.get('rsi'):
                    print(f"   RSI: {indicators['rsi']:.1f}")
                if indicators.get('macd'):
                    print(f"   MACD: {indicators['macd']:.2f}")
        
        if 'recommendation' in result:
            rec = result['recommendation']
            print(f"\n   📝 Recommendation: {rec.get('action', 'N/A')}")
            print(f"   Confidence: {rec.get('confidence', 0):.1%}")
        
        print(f"\n✅ Valuation Agent Test Complete!")
        return True
        
    except Exception as e:
        print(f"\n❌ Valuation Agent Test Failed: {e}")
        import traceback
        traceback.print_exc()
        return False

def test_geopolitical_agent(geo_events):
    """Test Geopolitical Agent"""
    print("\n" + "="*70)
    print("🧪 TESTING GEOPOLITICAL AGENT")
    print("="*70)
    
    try:
        agent = GeopoliticalAgent()
        agent.load_geopolitical_events(geo_events)
        
        stock = "Reliance Industries Ltd."
        print(f"\n{'─'*70}")
        result = agent.analyze(stock_name=stock)
        
        print(f"\n🌍 Geopolitical Analysis for: {result['stock']}")
        print(f"   Sector: {result['sector']}")
        
        risk = result.get('risk_assessment', {})
        print(f"\n   Risk Assessment:")
        print(f"   Overall Risk Score: {risk.get('overall_risk_score', 0):.0f}/100")
        print(f"   Risk Level: {risk.get('risk_level', 'N/A')}")
        print(f"   Market Outlook: {risk.get('market_outlook', 'N/A')}")
        
        key_risks = risk.get('key_risk_factors', [])
        if key_risks:
            print(f"\n   Key Risk Factors:")
            for r in key_risks[:3]:
                print(f"   • {r}")
        
        rec = result.get('recommendation', {})
        print(f"\n   📝 Recommendation: {rec.get('action', 'N/A')}")
        print(f"   Strategy: {rec.get('strategy', 'N/A')}")
        
        print(f"\n✅ Geopolitical Agent Test Complete!")
        return True
        
    except Exception as e:
        print(f"\n❌ Geopolitical Agent Test Failed: {e}")
        import traceback
        traceback.print_exc()
        return False

def test_fundamental_agent(quarterly_data, annual_data):
    """Test Fundamental Agent"""
    print("\n" + "="*70)
    print("🧪 TESTING FUNDAMENTAL AGENT")
    print("="*70)
    
    try:
        agent = FundamentalAgent()
        agent.load_quarterly_data(quarterly_data)
        agent.load_annual_data(annual_data)
        
        stock = "Reliance Industries Ltd."
        print(f"\n{'─'*70}")
        result = agent.analyze(stock, period="quarterly")
        
        print(f"\n📊 Fundamental Analysis for: {result['stock']}")
        
        # Financial Performance
        perf = result.get('financial_performance', {})
        latest = perf.get('latest_period', {})
        if latest:
            print(f"\n   Latest Financial Performance:")
            for metric, data in list(latest.items())[:4]:
                print(f"   • {data.get('label', metric)}: {data.get('value', 'N/A'):.2f}")
        
        # Growth Analysis
        growth = result.get('growth_analysis', {})
        if growth.get('revenue_cagr'):
            print(f"\n   Growth Analysis:")
            print(f"   Revenue CAGR: {growth['revenue_cagr']:.1f}%")
        if growth.get('profit_cagr'):
            print(f"   Profit CAGR: {growth['profit_cagr']:.1f}%")
        
        # Fundamental Score
        score = result.get('fundamental_score', {})
        print(f"\n   Fundamental Score: {score.get('overall_score', 0):.0f}/100")
        print(f"   Rating: {score.get('rating', 'N/A')}")
        
        rec = result.get('recommendation', {})
        print(f"\n   📝 Recommendation: {rec.get('action', 'N/A')}")
        print(f"   Confidence: {rec.get('confidence', 0):.1%}")
        
        print(f"\n✅ Fundamental Agent Test Complete!")
        return True
        
    except Exception as e:
        print(f"\n❌ Fundamental Agent Test Failed: {e}")
        import traceback
        traceback.print_exc()
        return False

def interactive_mode():
    """Interactive mode for querying all agents"""
    print("\n" + "="*70)
    print("🤖 INTERACTIVE MODE - All Agents")
    print("="*70)
    print("\nAvailable commands:")
    print("  sentiment <stock_name>    - Analyze news sentiment")
    print("  macro [stock_name]        - Analyze macro indicators")
    print("  valuation <stock_name>    - Technical & valuation analysis")
    print("  geopolitical <stock_name> - Geopolitical impact analysis")
    print("  fundamental <stock_name>  - Financial statements analysis")
    print("  full <stock_name>         - Run all agents for comprehensive analysis")
    print("  stats                     - Show agent statistics")
    print("  help                      - Show this help")
    print("  quit                      - Exit")
    print()
    
    # Load data
    print("Loading data...")
    try:
        scraper = NewsScraper()
        news_data = scraper.load_from_json("./data/news/sample_news.json")
        economic_data = SampleDataLoader.load_from_csv()
        geo_events = GeopoliticalDataLoader.load_from_json("./data/geopolitical/events.json")
        
        valuation_stocks = [
            "Reliance Industries Ltd.", 
            "Tata Consultancy Services Ltd. (TCS)",
            "HDFC Bank Ltd.",
        ]
        valuation_data = ValuationDataLoader.generate_valuation_data(valuation_stocks)
        price_data = ValuationDataLoader.generate_price_data(valuation_stocks)
        quarterly_data = FundamentalDataLoader.generate_quarterly_data(valuation_stocks)
        annual_data = FundamentalDataLoader.generate_annual_data(valuation_stocks)
        
    except Exception as e:
        print(f"⚠ Error loading data: {e}")
        print("Generating new data...")
        news_data, economic_data, valuation_data, price_data, geo_events, quarterly_data, annual_data = setup_data()
    
    # Initialize agents
    print("Initializing agents...")
    sentiment_agent = SentimentAgent()
    sentiment_agent.load_news_data(news_data)
    
    macro_agent = MacroEconomicAgent()
    macro_agent.load_economic_data(economic_data)
    
    valuation_agent = ValuationAgent()
    valuation_agent.load_valuation_data(valuation_data)
    valuation_agent.load_price_data(price_data)
    
    geo_agent = GeopoliticalAgent()
    geo_agent.load_geopolitical_events(geo_events)
    
    fundamental_agent = FundamentalAgent()
    fundamental_agent.load_quarterly_data(quarterly_data)
    fundamental_agent.load_annual_data(annual_data)
    
    print("\n✓ All agents ready!")
    print("\nNote: For valuation/geopolitical/fundamental agents, use full stock names like:")
    print("  'Reliance Industries Ltd.' or 'Tata Consultancy Services Ltd. (TCS)'")
    
    while True:
        try:
            command = input("\n> ").strip()
            
            if not command:
                continue
            
            parts = command.split(maxsplit=1)
            cmd = parts[0].lower()
            arg = parts[1] if len(parts) > 1 else None
            
            if cmd == "quit":
                print("Goodbye! 👋")
                break
            
            elif cmd == "help":
                print("\nCommands:")
                print("  sentiment <stock>    - News sentiment analysis")
                print("  macro [stock]        - Macro economic analysis")
                print("  valuation <stock>    - Valuation & technical analysis")
                print("  geopolitical <stock> - Geopolitical impact")
                print("  fundamental <stock>  - Financial analysis")
                print("  full <stock>         - All agents analysis")
                print("  stats                - Agent statistics")
                print("  quit                 - Exit")
            
            elif cmd == "stats":
                print("\n📊 Agent Statistics:")
                print(f"   Sentiment Agent: {sentiment_agent.get_stats()}")
                print(f"   Macro Agent: {macro_agent.get_stats()}")
                print(f"   Valuation Agent: {valuation_agent.get_stats()}")
                print(f"   Geopolitical Agent: {geo_agent.get_stats()}")
                print(f"   Fundamental Agent: {fundamental_agent.get_stats()}")
            
            elif cmd == "sentiment":
                if not arg:
                    print("Usage: sentiment <stock_name>")
                    continue
                
                result = sentiment_agent.analyze(arg.title())
                print(f"\n📈 {result['stock']} - {result['outlook']}")
                print(f"   Recommendation: {result['recommendation']}")
                print(f"   Confidence: {result['confidence']:.1%}")
            
            elif cmd == "macro":
                result = macro_agent.analyze(stock_name=arg.title() if arg else None)
                print(f"\n📊 Economic Analysis")
                if arg:
                    print(f"   Stock: {arg.title()}")
                print(f"   Health Score: {result['economic_health_score']:.1f}/100")
                print(f"   Outlook: {result['outlook']}")
            
            elif cmd == "valuation":
                if not arg:
                    print("Usage: valuation <stock_name>")
                    continue
                
                result = valuation_agent.analyze(arg)
                print(f"\n💰 Valuation Analysis: {result['stock']}")
                if 'current_price' in result:
                    print(f"   Price: ₹{result['current_price']:.2f}")
                if 'upside_potential' in result:
                    print(f"   Upside: {result['upside_potential']:.1f}%")
                if 'recommendation' in result:
                    print(f"   Recommendation: {result['recommendation'].get('action', 'N/A')}")
            
            elif cmd == "geopolitical":
                if not arg:
                    print("Usage: geopolitical <stock_name>")
                    continue
                
                result = geo_agent.analyze(stock_name=arg)
                risk = result.get('risk_assessment', {})
                print(f"\n🌍 Geopolitical Analysis: {result['stock']}")
                print(f"   Sector: {result['sector']}")
                print(f"   Risk Score: {risk.get('overall_risk_score', 0):.0f}/100")
                print(f"   Risk Level: {risk.get('risk_level', 'N/A')}")
            
            elif cmd == "fundamental":
                if not arg:
                    print("Usage: fundamental <stock_name>")
                    continue
                
                result = fundamental_agent.analyze(arg)
                score = result.get('fundamental_score', {})
                print(f"\n📊 Fundamental Analysis: {result['stock']}")
                print(f"   Score: {score.get('overall_score', 0):.0f}/100")
                print(f"   Rating: {score.get('rating', 'N/A')}")
                rec = result.get('recommendation', {})
                print(f"   Recommendation: {rec.get('action', 'N/A')}")
            
            elif cmd == "full":
                if not arg:
                    print("Usage: full <stock_name>")
                    continue
                
                print(f"\n🔍 COMPREHENSIVE ANALYSIS: {arg}")
                print("="*50)
                
                # Sentiment
                try:
                    sent_result = sentiment_agent.analyze(arg.split()[0])
                    print(f"\n😊 Sentiment: {sent_result['outlook']} ({sent_result['recommendation']})")
                except:
                    print(f"\n😊 Sentiment: No data available")
                
                # Macro
                macro_result = macro_agent.analyze(stock_name=arg)
                print(f"\n📈 Macro: Health {macro_result['economic_health_score']:.0f}/100 ({macro_result['outlook']})")
                
                # Valuation
                try:
                    val_result = valuation_agent.analyze(arg)
                    if 'upside_potential' in val_result:
                        print(f"\n💰 Valuation: {val_result['valuation_rating']} ({val_result['upside_potential']:.1f}% upside)")
                    else:
                        print(f"\n💰 Valuation: No data available")
                except:
                    print(f"\n💰 Valuation: No data available")
                
                # Geopolitical
                geo_result = geo_agent.analyze(stock_name=arg)
                risk = geo_result.get('risk_assessment', {})
                print(f"\n🌍 Geopolitical: {risk.get('risk_level', 'N/A')} risk ({risk.get('overall_risk_score', 0):.0f}/100)")
                
                # Fundamental
                try:
                    fund_result = fundamental_agent.analyze(arg)
                    score = fund_result.get('fundamental_score', {})
                    print(f"\n📊 Fundamental: {score.get('rating', 'N/A')} ({score.get('overall_score', 0):.0f}/100)")
                except:
                    print(f"\n📊 Fundamental: No data available")
                
                print("\n" + "="*50)
            
            else:
                print("Unknown command. Type 'help' for available commands.")
        
        except KeyboardInterrupt:
            print("\nGoodbye! 👋")
            break
        except Exception as e:
            print(f"Error: {e}")

def main():
    print_banner()
    
    if len(sys.argv) > 1:
        if sys.argv[1] == "setup":
            setup_data()
            return
        elif sys.argv[1] == "interactive":
            interactive_mode()
            return
    
    # Run full test suite
    print("🚀 Starting All Agent Tests...\n")
    
    # Setup data
    news_data, economic_data, valuation_data, price_data, geo_events, quarterly_data, annual_data = setup_data()
    
    # Test all agents
    sentiment_ok = test_sentiment_agent(news_data)
    macro_ok = test_macro_agent(economic_data)
    valuation_ok = test_valuation_agent(valuation_data, price_data)
    geo_ok = test_geopolitical_agent(geo_events)
    fundamental_ok = test_fundamental_agent(quarterly_data, annual_data)
    
    # Summary
    print("\n" + "="*70)
    print("📋 TEST SUMMARY")
    print("="*70)
    print(f"   Sentiment Agent:    {'✅ PASS' if sentiment_ok else '❌ FAIL'}")
    print(f"   Macro Agent:        {'✅ PASS' if macro_ok else '❌ FAIL'}")
    print(f"   Valuation Agent:    {'✅ PASS' if valuation_ok else '❌ FAIL'}")
    print(f"   Geopolitical Agent: {'✅ PASS' if geo_ok else '❌ FAIL'}")
    print(f"   Fundamental Agent:  {'✅ PASS' if fundamental_ok else '❌ FAIL'}")
    print("="*70)
    
    all_passed = sentiment_ok and macro_ok and valuation_ok and geo_ok and fundamental_ok
    
    if all_passed:
        print("\n🎉 All tests passed! All 5 agents are ready to use.")
        print("\nNext steps:")
        print("  1. Run 'python run_agents.py interactive' for interactive mode")
        print("  2. Run 'streamlit run app.py' for web interface")
    else:
        print("\n⚠ Some tests failed. Please check the errors above.")

if __name__ == "__main__":
    main()