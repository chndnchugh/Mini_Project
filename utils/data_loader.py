import pandas as pd
import numpy as np
from datetime import datetime, timedelta
from typing import Dict, List, Any
import os

class SampleDataLoader:
    """
    Sample Data Loader for Economic Indicators
    Generates sample economic data for testing the Macro Economic Agent
    """
    
    # Economic indicators configuration
    INDICATORS = {
        'gdp_growth': {
            'name': 'GDP Growth Rate',
            'unit': '%',
            'base_value': 6.5,
            'volatility': 0.5,
            'trend': 0.1
        },
        'inflation_cpi': {
            'name': 'CPI Inflation',
            'unit': '%',
            'base_value': 5.0,
            'volatility': 0.3,
            'trend': 0.05
        },
        'repo_rate': {
            'name': 'RBI Repo Rate',
            'unit': '%',
            'base_value': 6.5,
            'volatility': 0.1,
            'trend': 0
        },
        'unemployment': {
            'name': 'Unemployment Rate',
            'unit': '%',
            'base_value': 7.5,
            'volatility': 0.4,
            'trend': -0.05
        },
        'iip_growth': {
            'name': 'Industrial Production Growth',
            'unit': '%',
            'base_value': 4.0,
            'volatility': 1.0,
            'trend': 0.1
        },
        'trade_balance': {
            'name': 'Trade Balance',
            'unit': 'USD Billion',
            'base_value': -20.0,
            'volatility': 3.0,
            'trend': -0.5
        },
        'forex_reserves': {
            'name': 'Forex Reserves',
            'unit': 'USD Billion',
            'base_value': 600.0,
            'volatility': 10.0,
            'trend': 2.0
        },
        'rupee_dollar': {
            'name': 'USD/INR Exchange Rate',
            'unit': 'INR',
            'base_value': 83.0,
            'volatility': 0.5,
            'trend': 0.1
        }
    }
    
    @staticmethod
    def generate_indicator_data(indicator: str, periods: int = 24) -> pd.DataFrame:
        """
        Generate sample time series data for an economic indicator
        
        Args:
            indicator: Name of the indicator
            periods: Number of monthly periods to generate
            
        Returns:
            DataFrame with date and value columns
        """
        if indicator not in SampleDataLoader.INDICATORS:
            raise ValueError(f"Unknown indicator: {indicator}")
        
        config = SampleDataLoader.INDICATORS[indicator]
        
        # Generate dates (monthly, going back from current date)
        end_date = datetime.now()
        dates = pd.date_range(end=end_date, periods=periods, freq='M')
        
        # Generate values with trend and noise
        base = config['base_value']
        volatility = config['volatility']
        trend = config['trend']
        
        values = []
        current_value = base - (trend * periods)  # Start from earlier value
        
        for i in range(periods):
            # Add trend
            current_value += trend
            # Add noise
            noise = np.random.normal(0, volatility)
            value = current_value + noise
            values.append(value)
        
        df = pd.DataFrame({
            'date': dates,
            'value': values,
            'indicator': indicator,
            'unit': config['unit']
        })
        
        return df
    
    @staticmethod
    def load_all_indicators(periods: int = 24) -> Dict[str, pd.DataFrame]:
        """
        Load all economic indicators
        
        Args:
            periods: Number of monthly periods
            
        Returns:
            Dict with indicator names as keys and DataFrames as values
        """
        data = {}
        
        for indicator in SampleDataLoader.INDICATORS.keys():
            data[indicator] = SampleDataLoader.generate_indicator_data(indicator, periods)
        
        print(f"✓ Generated data for {len(data)} economic indicators")
        return data
    
    @staticmethod
    def save_to_csv(data: Dict[str, pd.DataFrame], directory: str = "./data/economic_data"):
        """
        Save indicator data to CSV files
        
        Args:
            data: Dict of indicator DataFrames
            directory: Output directory
        """
        os.makedirs(directory, exist_ok=True)
        
        for indicator, df in data.items():
            filepath = f"{directory}/{indicator}.csv"
            df.to_csv(filepath, index=False)
        
        print(f"✓ Saved economic data to {directory}")
    
    @staticmethod
    def load_from_csv(directory: str = "./data/economic_data") -> Dict[str, pd.DataFrame]:
        """
        Load indicator data from CSV files
        
        Args:
            directory: Directory containing CSV files
            
        Returns:
            Dict with indicator names as keys and DataFrames as values
        """
        import glob
        
        data = {}
        csv_files = glob.glob(f"{directory}/*.csv")
        
        for filepath in csv_files:
            indicator = os.path.basename(filepath).replace('.csv', '')
            df = pd.read_csv(filepath)
            df['date'] = pd.to_datetime(df['date'])
            data[indicator] = df
        
        if data:
            print(f"✓ Loaded data for {len(data)} economic indicators from {directory}")
        else:
            print(f"⚠ No data found in {directory}, generating sample data...")
            data = SampleDataLoader.load_all_indicators()
            SampleDataLoader.save_to_csv(data, directory)
        
        return data
    
    @staticmethod
    def get_latest_values(data: Dict[str, pd.DataFrame]) -> Dict[str, float]:
        """
        Get the latest value for each indicator
        
        Args:
            data: Dict of indicator DataFrames
            
        Returns:
            Dict with indicator names and their latest values
        """
        latest = {}
        
        for indicator, df in data.items():
            if not df.empty:
                latest[indicator] = df.iloc[-1]['value']
        
        return latest
    
    @staticmethod
    def get_indicator_trend(data: Dict[str, pd.DataFrame], indicator: str, periods: int = 6) -> str:
        """
        Determine the trend of an indicator
        
        Args:
            data: Dict of indicator DataFrames
            indicator: Name of the indicator
            periods: Number of periods to analyze
            
        Returns:
            Trend description string
        """
        if indicator not in data:
            return "Unknown"
        
        df = data[indicator]
        if len(df) < periods:
            return "Insufficient data"
        
        recent = df.tail(periods)['value']
        
        # Calculate slope
        x = np.arange(len(recent))
        slope = np.polyfit(x, recent.values, 1)[0]
        
        # Determine trend based on slope
        mean_value = recent.mean()
        if mean_value == 0:
            return "Flat"
        
        slope_pct = (slope / abs(mean_value)) * 100
        
        if slope_pct > 2:
            return "Rising"
        elif slope_pct < -2:
            return "Falling"
        else:
            return "Stable"


class NewsDataLoader:
    """
    Sample News Data Loader
    Generates sample news data for testing the Sentiment Agent
    """
    
    SAMPLE_NEWS_TEMPLATES = {
        "positive": [
            "{company} reports strong quarterly earnings, beats estimates",
            "{company} announces expansion plans, stock surges",
            "{company} wins major contract worth Rs 1000 crore",
            "Analysts upgrade {company} to 'Buy' rating",
            "{company} launches innovative new product line",
            "{company} reports record revenue growth of 25%",
            "FIIs increase stake in {company}",
            "{company} announces special dividend for shareholders"
        ],
        "negative": [
            "{company} misses quarterly earnings estimates",
            "{company} faces regulatory scrutiny",
            "Analysts downgrade {company} amid concerns",
            "{company} reports decline in profit margins",
            "{company} faces supply chain disruptions",
            "FIIs reduce holdings in {company}",
            "{company} warns of challenging market conditions",
            "Competition intensifies for {company} in key markets"
        ],
        "neutral": [
            "{company} holds annual general meeting",
            "{company} appoints new board member",
            "{company} maintains guidance for fiscal year",
            "{company} announces routine management changes",
            "{company} participates in industry conference",
            "{company} files quarterly compliance report"
        ]
    }
    
    COMPANIES = [
        "Reliance", "TCS", "Infosys", "HDFC Bank", "ICICI Bank",
        "HUL", "SBI", "Airtel", "ITC", "Kotak Bank",
        "L&T", "Axis Bank", "Asian Paints", "Bajaj Finance", "Maruti"
    ]
    
    @staticmethod
    def generate_sample_news(num_articles: int = 50) -> List[Dict[str, Any]]:
        """
        Generate sample news articles
        
        Args:
            num_articles: Number of articles to generate
            
        Returns:
            List of news article dicts
        """
        articles = []
        
        sentiments = ['positive', 'negative', 'neutral']
        weights = [0.4, 0.3, 0.3]  # More positive news
        
        for i in range(num_articles):
            sentiment = np.random.choice(sentiments, p=weights)
            company = np.random.choice(NewsDataLoader.COMPANIES)
            template = np.random.choice(NewsDataLoader.SAMPLE_NEWS_TEMPLATES[sentiment])
            
            title = template.format(company=company)
            
            # Generate random date within last 30 days
            days_ago = np.random.randint(0, 30)
            date = (datetime.now() - timedelta(days=days_ago)).strftime("%Y-%m-%d")
            
            articles.append({
                "title": title,
                "company": company,
                "date": date,
                "source": np.random.choice(["Economic Times", "Moneycontrol", "Business Standard", "LiveMint"]),
                "sentiment_label": sentiment
            })
        
        return articles
    
    @staticmethod
    def save_to_json(articles: List[Dict], filepath: str = "./data/news/sample_news.json"):
        """Save news articles to JSON file"""
        import json
        
        os.makedirs(os.path.dirname(filepath), exist_ok=True)
        
        with open(filepath, 'w', encoding='utf-8') as f:
            json.dump(articles, f, indent=2, ensure_ascii=False)
        
        print(f"✓ Saved {len(articles)} news articles to {filepath}")
    
    @staticmethod
    def load_from_json(filepath: str = "./data/news/sample_news.json") -> List[Dict]:
        """Load news articles from JSON file"""
        import json
        
        try:
            with open(filepath, 'r', encoding='utf-8') as f:
                return json.load(f)
        except FileNotFoundError:
            print(f"⚠ File not found: {filepath}, generating sample data...")
            articles = NewsDataLoader.generate_sample_news()
            NewsDataLoader.save_to_json(articles, filepath)
            return articles