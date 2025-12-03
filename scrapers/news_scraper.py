import requests
from bs4 import BeautifulSoup
from datetime import datetime, timedelta
import time
from typing import List, Dict
import json

class NewsScraper:
    """Simple news scraper for Indian stock market news"""
    
    def __init__(self):
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
        }
    
    def scrape_moneycontrol(self, stock_name: str, max_articles: int = 10) -> List[Dict]:
        """
        Scrape news from MoneyControl (simplified)
        Note: This is a basic implementation. For production, consider using official APIs
        """
        print(f"🔍 Scraping news for {stock_name}...")
        
        # This is a placeholder - MoneyControl requires more sophisticated scraping
        # For demo purposes, we'll return sample data
        news_data = self._get_sample_news(stock_name, max_articles)
        
        print(f"✓ Found {len(news_data)} articles")
        return news_data
    
    def _get_sample_news(self, stock_name: str, count: int = 10) -> List[Dict]:
        """Generate sample news data for demonstration"""
        
        sample_news_templates = {
            "Reliance": [
                {
                    "title": "Reliance Industries Q3 results exceed expectations",
                    "content": "Reliance Industries reported strong quarterly results with revenue growth of 12% YoY. The company's retail and digital services segments showed robust performance.",
                    "sentiment": "positive"
                },
                {
                    "title": "Reliance announces major investment in renewable energy",
                    "content": "RIL plans to invest $10 billion in green energy initiatives over the next 3 years, strengthening its position in the sustainability sector.",
                    "sentiment": "positive"
                },
                {
                    "title": "Analysts raise target price for Reliance stock",
                    "content": "Multiple brokerages have raised their target prices for Reliance Industries following strong performance across business verticals.",
                    "sentiment": "positive"
                },
            ],
            "TCS": [
                {
                    "title": "TCS wins multi-million dollar deal with European bank",
                    "content": "Tata Consultancy Services secured a major contract worth $500 million for digital transformation services with a leading European financial institution.",
                    "sentiment": "positive"
                },
                {
                    "title": "TCS reports healthy deal pipeline for Q4",
                    "content": "TCS management indicated strong deal momentum with total contract value exceeding $8 billion in the current quarter.",
                    "sentiment": "positive"
                },
                {
                    "title": "IT sector faces margin pressure: Analysts",
                    "content": "Indian IT companies including TCS may face margin headwinds due to wage inflation and increased competition.",
                    "sentiment": "negative"
                },
            ],
            "Infosys": [
                {
                    "title": "Infosys guidance maintained despite macro challenges",
                    "content": "Infosys retained its revenue growth guidance for FY25, showing confidence in business momentum despite global headwinds.",
                    "sentiment": "neutral"
                },
                {
                    "title": "Infosys expands AI capabilities with new partnerships",
                    "content": "The company announced strategic partnerships to enhance its AI and generative AI offerings for enterprise clients.",
                    "sentiment": "positive"
                },
            ],
            "HDFC Bank": [
                {
                    "title": "HDFC Bank reports strong loan growth in Q3",
                    "content": "HDFC Bank's loan book grew 16% YoY with healthy asset quality. Net interest margin remained stable at 4.1%.",
                    "sentiment": "positive"
                },
                {
                    "title": "Banking sector faces NPA concerns amid economic slowdown",
                    "content": "Analysts warn of potential asset quality stress in the banking sector if economic growth moderates further.",
                    "sentiment": "negative"
                },
            ],
            "default": [
                {
                    "title": f"{stock_name} shows steady performance in volatile market",
                    "content": f"{stock_name} maintained stable operations despite market volatility, with management expressing confidence in growth prospects.",
                    "sentiment": "neutral"
                },
                {
                    "title": f"Market outlook: {stock_name} among top picks",
                    "content": f"Analysts include {stock_name} in their top stock picks for the current quarter based on strong fundamentals.",
                    "sentiment": "positive"
                },
            ]
        }
        
        # Get relevant news or default
        templates = sample_news_templates.get(stock_name, sample_news_templates["default"])
        
        # Generate news with dates
        news_data = []
        base_date = datetime.now()
        
        for i in range(min(count, len(templates) * 3)):
            template = templates[i % len(templates)]
            date = base_date - timedelta(days=i*2)
            
            news_data.append({
                "title": template["title"],
                "content": template["content"],
                "date": date.strftime("%Y-%m-%d"),
                "source": "MoneyControl",
                "stock": stock_name,
                "url": f"https://example.com/news/{i}"
            })
        
        return news_data
    
    def scrape_economic_times(self, stock_name: str, max_articles: int = 10) -> List[Dict]:
        """Scrape from Economic Times (simplified)"""
        # Similar implementation as MoneyControl
        return self._get_sample_news(stock_name, max_articles)
    
    def scrape_multiple_sources(self, stock_names: List[str], 
                                 articles_per_stock: int = 10) -> List[Dict]:
        """Scrape news for multiple stocks"""
        all_news = []
        
        for stock in stock_names:
            news = self.scrape_moneycontrol(stock, articles_per_stock)
            all_news.extend(news)
            time.sleep(1)  # Be respectful to servers
        
        return all_news
    
    def save_to_json(self, news_data: List[Dict], filename: str):
        """Save scraped news to JSON file"""
        with open(filename, 'w', encoding='utf-8') as f:
            json.dump(news_data, f, indent=2, ensure_ascii=False)
        print(f"✓ Saved {len(news_data)} articles to {filename}")
    
    def load_from_json(self, filename: str) -> List[Dict]:
        """Load news from JSON file"""
        with open(filename, 'r', encoding='utf-8') as f:
            return json.load(f)