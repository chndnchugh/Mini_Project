import pandas as pd
import numpy as np
from datetime import datetime, timedelta
from typing import Dict, List, Any
import json
import os

class ValuationDataLoader:
    """Generate sample valuation and price data for testing"""
    
    # NSE 50 stocks with their sectors
    NSE_50_STOCKS = {
        "Reliance Industries Ltd.": "Oil & Gas",
        "Tata Consultancy Services Ltd. (TCS)": "IT",
        "HDFC Bank Ltd.": "Banking",
        "Infosys Ltd.": "IT",
        "ICICI Bank Ltd.": "Banking",
        "Hindustan Unilever Ltd.": "FMCG",
        "State Bank of India (SBI)": "Banking",
        "Bharti Airtel Ltd.": "Telecom",
        "ITC Ltd.": "FMCG",
        "Kotak Mahindra Bank Ltd.": "Banking",
        "Larsen & Toubro Ltd.": "Infrastructure",
        "Axis Bank Ltd.": "Banking",
        "Asian Paints Ltd.": "FMCG",
        "Bajaj Finance Ltd.": "Banking",
        "Maruti Suzuki India Ltd.": "Auto",
        "Titan Company Ltd.": "FMCG",
        "Sun Pharmaceutical Industries Ltd.": "Pharma",
        "Wipro Ltd.": "IT",
        "Tech Mahindra Ltd.": "IT",
        "Tata Motors Ltd.": "Auto",
        "HCL Technologies Ltd.": "IT",
        "NTPC Ltd.": "Infrastructure",
        "Tata Steel Ltd.": "Metals",
        "Power Grid Corporation of India Ltd.": "Infrastructure",
        "Oil & Natural Gas Corporation Ltd. (ONGC)": "Oil & Gas",
    }
    
    # Base prices for stocks
    BASE_PRICES = {
        "Reliance Industries Ltd.": 2450,
        "Tata Consultancy Services Ltd. (TCS)": 3850,
        "HDFC Bank Ltd.": 1650,
        "Infosys Ltd.": 1520,
        "ICICI Bank Ltd.": 1050,
        "Hindustan Unilever Ltd.": 2350,
        "State Bank of India (SBI)": 625,
        "Bharti Airtel Ltd.": 1180,
        "ITC Ltd.": 435,
        "Kotak Mahindra Bank Ltd.": 1780,
        "Larsen & Toubro Ltd.": 3450,
        "Axis Bank Ltd.": 1120,
        "Asian Paints Ltd.": 2680,
        "Bajaj Finance Ltd.": 6850,
        "Maruti Suzuki India Ltd.": 10500,
        "Titan Company Ltd.": 3250,
        "Sun Pharmaceutical Industries Ltd.": 1420,
        "Wipro Ltd.": 485,
        "Tech Mahindra Ltd.": 1380,
        "Tata Motors Ltd.": 785,
        "HCL Technologies Ltd.": 1650,
        "NTPC Ltd.": 345,
        "Tata Steel Ltd.": 142,
        "Power Grid Corporation of India Ltd.": 285,
        "Oil & Natural Gas Corporation Ltd. (ONGC)": 245,
    }
    
    @staticmethod
    def generate_valuation_data(stocks: List[str] = None) -> Dict[str, pd.DataFrame]:
        """Generate sample valuation metrics for stocks"""
        if stocks is None:
            stocks = list(ValuationDataLoader.NSE_50_STOCKS.keys())
        
        data = {}
        
        for stock in stocks:
            sector = ValuationDataLoader.NSE_50_STOCKS.get(stock, "General")
            base_price = ValuationDataLoader.BASE_PRICES.get(stock, 1000)
            
            # Generate metrics based on sector
            metrics = ValuationDataLoader._generate_sector_metrics(sector, base_price)
            
            rows = []
            date = datetime.now().strftime("%Y-%m-%d")
            
            for metric, value in metrics.items():
                rows.append({
                    "date": date,
                    "metric": metric,
                    "value": value
                })
            
            data[stock] = pd.DataFrame(rows)
        
        return data
    
    @staticmethod
    def _generate_sector_metrics(sector: str, base_price: float) -> Dict[str, float]:
        """Generate metrics based on sector characteristics"""
        
        sector_characteristics = {
            "IT": {"pe": (25, 35), "pb": (5, 10), "roe": (20, 35), "de": (0, 0.2)},
            "Banking": {"pe": (12, 20), "pb": (1.5, 3), "roe": (12, 18), "de": (6, 10)},
            "FMCG": {"pe": (50, 80), "pb": (10, 20), "roe": (30, 50), "de": (0, 0.3)},
            "Pharma": {"pe": (20, 40), "pb": (3, 8), "roe": (15, 25), "de": (0.1, 0.5)},
            "Auto": {"pe": (15, 30), "pb": (2, 5), "roe": (12, 20), "de": (0.3, 0.8)},
            "Infrastructure": {"pe": (15, 25), "pb": (2, 4), "roe": (10, 18), "de": (0.5, 1.5)},
            "Metals": {"pe": (8, 15), "pb": (1, 2.5), "roe": (10, 20), "de": (0.5, 1.2)},
            "Oil & Gas": {"pe": (10, 18), "pb": (1.5, 3), "roe": (12, 20), "de": (0.3, 0.8)},
            "Telecom": {"pe": (30, 60), "pb": (2, 5), "roe": (8, 15), "de": (0.8, 1.5)},
        }
        
        char = sector_characteristics.get(sector, {"pe": (15, 25), "pb": (2, 4), "roe": (12, 18), "de": (0.3, 0.8)})
        
        pe = np.random.uniform(*char["pe"])
        pb = np.random.uniform(*char["pb"])
        roe = np.random.uniform(*char["roe"])
        de = np.random.uniform(*char["de"])
        
        eps = base_price / pe
        book_value = base_price / pb
        
        return {
            "current_price": base_price + np.random.uniform(-base_price*0.05, base_price*0.05),
            "pe_ratio": pe,
            "pb_ratio": pb,
            "ps_ratio": np.random.uniform(2, 8),
            "peg_ratio": np.random.uniform(0.8, 2.5),
            "ev_ebitda": np.random.uniform(10, 25),
            "dividend_yield": np.random.uniform(0.5, 3),
            "market_cap": base_price * np.random.uniform(10000, 500000),
            "eps": eps,
            "book_value": book_value,
            "roe": roe,
            "roce": roe + np.random.uniform(-3, 5),
            "debt_to_equity": de,
            "current_ratio": np.random.uniform(1, 3),
        }
    
    @staticmethod
    def generate_price_data(stocks: List[str] = None, days: int = 252) -> Dict[str, pd.DataFrame]:
        """Generate sample historical price data"""
        if stocks is None:
            stocks = list(ValuationDataLoader.NSE_50_STOCKS.keys())[:10]
        
        data = {}
        
        for stock in stocks:
            base_price = ValuationDataLoader.BASE_PRICES.get(stock, 1000)
            
            dates = pd.date_range(end=datetime.now(), periods=days, freq='D')
            
            # Generate price series with trend and volatility
            returns = np.random.normal(0.0005, 0.02, days)  # Daily returns
            price_series = base_price * np.cumprod(1 + returns)
            
            df = pd.DataFrame({
                'date': dates,
                'open': price_series * np.random.uniform(0.99, 1.01, days),
                'high': price_series * np.random.uniform(1.01, 1.03, days),
                'low': price_series * np.random.uniform(0.97, 0.99, days),
                'close': price_series,
                'volume': np.random.randint(100000, 10000000, days)
            })
            
            data[stock] = df
        
        return data
    
    @staticmethod
    def save_to_csv(data: Dict[str, pd.DataFrame], directory: str = "./data/valuation"):
        """Save valuation data to CSV"""
        os.makedirs(directory, exist_ok=True)
        
        for stock, df in data.items():
            safe_name = stock.replace(" ", "_").replace(".", "").replace("(", "").replace(")", "")[:30]
            filepath = f"{directory}/{safe_name}.csv"
            df.to_csv(filepath, index=False)
        
        print(f"✓ Saved valuation data for {len(data)} stocks to {directory}")
    
    @staticmethod
    def load_from_csv(directory: str = "./data/valuation") -> Dict[str, pd.DataFrame]:
        """Load valuation data from CSV"""
        import glob
        
        data = {}
        csv_files = glob.glob(f"{directory}/*.csv")
        
        for filepath in csv_files:
            name = os.path.basename(filepath).replace('.csv', '').replace('_', ' ')
            df = pd.read_csv(filepath)
            data[name] = df
        
        return data


class GeopoliticalDataLoader:
    """Generate sample geopolitical events data"""
    
    @staticmethod
    def generate_sample_events() -> List[Dict[str, Any]]:
        """Generate sample geopolitical events"""
        
        events = [
            # Tariff Events
            {
                "title": "US increases tariffs on Chinese imports",
                "description": "The United States announced a 25% tariff increase on Chinese goods worth $200 billion, escalating trade tensions.",
                "category": "tariffs",
                "date": (datetime.now() - timedelta(days=15)).strftime("%Y-%m-%d"),
                "countries_affected": ["USA", "China", "India"],
                "sectors_affected": ["IT", "Metals", "Auto"],
                "impact_level": "high",
                "source": "Reuters"
            },
            {
                "title": "India revises import duties on electronics",
                "description": "Government of India increased customs duty on imported electronics to boost domestic manufacturing.",
                "category": "tariffs",
                "date": (datetime.now() - timedelta(days=20)).strftime("%Y-%m-%d"),
                "countries_affected": ["India", "China", "Taiwan"],
                "sectors_affected": ["IT", "Auto"],
                "impact_level": "medium",
                "source": "Economic Times"
            },
            
            # G20 Events
            {
                "title": "G20 Summit focuses on global economic recovery",
                "description": "G20 leaders agreed on coordinated measures to support economic recovery and address inflation concerns.",
                "category": "g20",
                "date": (datetime.now() - timedelta(days=30)).strftime("%Y-%m-%d"),
                "countries_affected": ["Global"],
                "sectors_affected": ["Banking", "Infrastructure"],
                "impact_level": "medium",
                "source": "Financial Times"
            },
            {
                "title": "G20 finance ministers discuss crypto regulations",
                "description": "Finance ministers from G20 nations discussed implementing unified cryptocurrency regulations.",
                "category": "g20",
                "date": (datetime.now() - timedelta(days=45)).strftime("%Y-%m-%d"),
                "countries_affected": ["Global"],
                "sectors_affected": ["Banking", "IT"],
                "impact_level": "low",
                "source": "Bloomberg"
            },
            
            # Policy Changes
            {
                "title": "RBI holds repo rate steady amid inflation concerns",
                "description": "Reserve Bank of India maintained the repo rate at 6.5% while signaling vigilance on inflation.",
                "category": "monetary_policy",
                "date": (datetime.now() - timedelta(days=10)).strftime("%Y-%m-%d"),
                "countries_affected": ["India"],
                "sectors_affected": ["Banking", "Infrastructure", "Auto"],
                "impact_level": "high",
                "source": "RBI"
            },
            {
                "title": "Government announces PLI scheme expansion",
                "description": "Production Linked Incentive scheme expanded to include more sectors with ₹50,000 crore allocation.",
                "category": "policy_changes",
                "date": (datetime.now() - timedelta(days=25)).strftime("%Y-%m-%d"),
                "countries_affected": ["India"],
                "sectors_affected": ["Auto", "Pharma", "IT"],
                "impact_level": "high",
                "source": "Ministry of Commerce"
            },
            
            # Conflicts
            {
                "title": "Middle East tensions impact oil markets",
                "description": "Escalating tensions in the Middle East region led to crude oil price volatility.",
                "category": "conflicts",
                "date": (datetime.now() - timedelta(days=5)).strftime("%Y-%m-%d"),
                "countries_affected": ["Middle East", "India", "Global"],
                "sectors_affected": ["Oil & Gas", "Airlines", "FMCG"],
                "impact_level": "high",
                "source": "Reuters"
            },
            {
                "title": "Russia-Ukraine situation affects commodity supplies",
                "description": "Ongoing conflict continues to impact global supply chains for metals and agricultural commodities.",
                "category": "conflicts",
                "date": (datetime.now() - timedelta(days=60)).strftime("%Y-%m-%d"),
                "countries_affected": ["Russia", "Ukraine", "Europe", "India"],
                "sectors_affected": ["Metals", "FMCG", "Oil & Gas"],
                "impact_level": "medium",
                "source": "Bloomberg"
            },
            
            # Sanctions
            {
                "title": "New sanctions on Russian entities",
                "description": "Western nations imposed additional sanctions affecting trade with Russian companies.",
                "category": "sanctions",
                "date": (datetime.now() - timedelta(days=40)).strftime("%Y-%m-%d"),
                "countries_affected": ["Russia", "Europe", "India"],
                "sectors_affected": ["Oil & Gas", "Banking", "Metals"],
                "impact_level": "medium",
                "source": "US Treasury"
            },
            
            # Natural Disasters
            {
                "title": "Flooding in key manufacturing regions",
                "description": "Severe flooding in South Asia affected industrial production and supply chains.",
                "category": "natural_disasters",
                "date": (datetime.now() - timedelta(days=35)).strftime("%Y-%m-%d"),
                "countries_affected": ["India", "Bangladesh"],
                "sectors_affected": ["FMCG", "Auto", "Infrastructure"],
                "impact_level": "medium",
                "source": "IMD"
            },
            
            # Trade Agreements
            {
                "title": "India-UAE trade agreement implementation",
                "description": "Comprehensive Economic Partnership Agreement between India and UAE comes into effect.",
                "category": "trade_agreements",
                "date": (datetime.now() - timedelta(days=50)).strftime("%Y-%m-%d"),
                "countries_affected": ["India", "UAE"],
                "sectors_affected": ["FMCG", "Pharma", "IT"],
                "impact_level": "medium",
                "source": "Ministry of Commerce"
            },
            {
                "title": "India-EFTA FTA negotiations progress",
                "description": "Free Trade Agreement talks between India and EFTA nations show positive progress.",
                "category": "trade_agreements",
                "date": (datetime.now() - timedelta(days=55)).strftime("%Y-%m-%d"),
                "countries_affected": ["India", "Switzerland", "Norway"],
                "sectors_affected": ["Pharma", "IT", "Banking"],
                "impact_level": "low",
                "source": "Economic Times"
            },
            
            # Supply Chain
            {
                "title": "Semiconductor shortage continues to affect auto sector",
                "description": "Global chip shortage leads to production cuts in automobile manufacturing.",
                "category": "supply_chain",
                "date": (datetime.now() - timedelta(days=12)).strftime("%Y-%m-%d"),
                "countries_affected": ["Global", "India"],
                "sectors_affected": ["Auto", "IT"],
                "impact_level": "high",
                "source": "Industry Reports"
            },
        ]
        
        return events
    
    @staticmethod
    def save_to_json(events: List[Dict], filepath: str = "./data/geopolitical/events.json"):
        """Save events to JSON file"""
        os.makedirs(os.path.dirname(filepath), exist_ok=True)
        
        with open(filepath, 'w', encoding='utf-8') as f:
            json.dump(events, f, indent=2, ensure_ascii=False)
        
        print(f"✓ Saved {len(events)} geopolitical events to {filepath}")
    
    @staticmethod
    def load_from_json(filepath: str = "./data/geopolitical/events.json") -> List[Dict]:
        """Load events from JSON file"""
        with open(filepath, 'r', encoding='utf-8') as f:
            return json.load(f)


class FundamentalDataLoader:
    """Generate sample fundamental/financial data"""
    
    @staticmethod
    def generate_quarterly_data(stocks: List[str] = None, quarters: int = 8) -> Dict[str, pd.DataFrame]:
        """Generate sample quarterly financial data"""
        if stocks is None:
            stocks = list(ValuationDataLoader.NSE_50_STOCKS.keys())[:15]
        
        data = {}
        
        for stock in stocks:
            sector = ValuationDataLoader.NSE_50_STOCKS.get(stock, "General")
            rows = []
            
            # Base values
            base_revenue = np.random.uniform(5000, 50000)
            base_profit = base_revenue * np.random.uniform(0.08, 0.20)
            
            for i in range(quarters):
                year = 2024 - (i // 4)
                quarter = 4 - (i % 4)
                
                # Add growth trend with some variation
                growth_factor = 1 + (quarters - i) * 0.02 + np.random.uniform(-0.05, 0.05)
                
                revenue = base_revenue * growth_factor
                operating_profit = revenue * np.random.uniform(0.12, 0.22)
                net_profit = operating_profit * np.random.uniform(0.6, 0.85)
                
                rows.append({
                    'quarter': quarter,
                    'year': year,
                    'revenue': revenue,
                    'revenue_growth': np.random.uniform(-5, 20),
                    'operating_profit': operating_profit,
                    'operating_margin': (operating_profit / revenue) * 100,
                    'net_profit': net_profit,
                    'net_margin': (net_profit / revenue) * 100,
                    'ebitda': operating_profit * np.random.uniform(1.1, 1.3),
                    'ebitda_margin': np.random.uniform(15, 30),
                    'eps': net_profit / np.random.uniform(100, 500),
                    'eps_growth': np.random.uniform(-10, 25),
                    'roe': np.random.uniform(10, 30),
                    'roce': np.random.uniform(12, 35),
                    'roa': np.random.uniform(5, 15),
                    'current_ratio': np.random.uniform(1, 3),
                    'quick_ratio': np.random.uniform(0.8, 2.5),
                    'debt_to_equity': np.random.uniform(0.1, 1.5),
                    'interest_coverage': np.random.uniform(3, 20),
                    'asset_turnover': np.random.uniform(0.5, 2),
                    'operating_cash_flow': net_profit * np.random.uniform(0.8, 1.5),
                    'free_cash_flow': net_profit * np.random.uniform(0.5, 1.2),
                })
            
            data[stock] = pd.DataFrame(rows)
        
        return data
    
    @staticmethod
    def generate_annual_data(stocks: List[str] = None, years: int = 5) -> Dict[str, pd.DataFrame]:
        """Generate sample annual financial data"""
        if stocks is None:
            stocks = list(ValuationDataLoader.NSE_50_STOCKS.keys())[:15]
        
        data = {}
        
        for stock in stocks:
            rows = []
            
            base_revenue = np.random.uniform(20000, 200000)
            base_profit = base_revenue * np.random.uniform(0.08, 0.18)
            
            for i in range(years):
                year = 2024 - i
                growth_factor = 1 + (years - i) * 0.08 + np.random.uniform(-0.1, 0.1)
                
                revenue = base_revenue * growth_factor
                operating_profit = revenue * np.random.uniform(0.12, 0.20)
                net_profit = operating_profit * np.random.uniform(0.65, 0.85)
                
                total_assets = revenue * np.random.uniform(1.5, 3)
                total_equity = total_assets * np.random.uniform(0.4, 0.7)
                total_debt = total_assets - total_equity
                
                rows.append({
                    'year': year,
                    'revenue': revenue,
                    'revenue_growth': np.random.uniform(5, 20),
                    'operating_profit': operating_profit,
                    'operating_margin': (operating_profit / revenue) * 100,
                    'net_profit': net_profit,
                    'net_margin': (net_profit / revenue) * 100,
                    'ebitda': operating_profit * np.random.uniform(1.15, 1.35),
                    'ebitda_margin': np.random.uniform(15, 28),
                    'eps': net_profit / np.random.uniform(100, 500),
                    'roe': (net_profit / total_equity) * 100,
                    'roce': np.random.uniform(12, 30),
                    'roa': (net_profit / total_assets) * 100,
                    'total_assets': total_assets,
                    'total_liabilities': total_assets - total_equity,
                    'shareholders_equity': total_equity,
                    'total_debt': total_debt,
                    'debt_to_equity': total_debt / total_equity,
                    'current_ratio': np.random.uniform(1.2, 2.8),
                    'book_value_per_share': total_equity / np.random.uniform(100, 500),
                    'dividend_per_share': np.random.uniform(5, 50),
                    'dividend_payout': np.random.uniform(20, 50),
                    'operating_cash_flow': net_profit * np.random.uniform(0.9, 1.4),
                    'investing_cash_flow': -net_profit * np.random.uniform(0.3, 0.8),
                    'financing_cash_flow': net_profit * np.random.uniform(-0.5, 0.3),
                    'free_cash_flow': net_profit * np.random.uniform(0.5, 1.1),
                    'capex': net_profit * np.random.uniform(0.2, 0.6),
                })
            
            data[stock] = pd.DataFrame(rows)
        
        return data
    
    @staticmethod
    def save_to_csv(quarterly_data: Dict, annual_data: Dict, 
                    directory: str = "./data/fundamentals"):
        """Save fundamental data to CSV"""
        os.makedirs(f"{directory}/quarterly", exist_ok=True)
        os.makedirs(f"{directory}/annual", exist_ok=True)
        
        for stock, df in quarterly_data.items():
            safe_name = stock.replace(" ", "_").replace(".", "").replace("(", "").replace(")", "")[:30]
            df.to_csv(f"{directory}/quarterly/{safe_name}.csv", index=False)
        
        for stock, df in annual_data.items():
            safe_name = stock.replace(" ", "_").replace(".", "").replace("(", "").replace(")", "")[:30]
            df.to_csv(f"{directory}/annual/{safe_name}.csv", index=False)
        
        print(f"✓ Saved fundamental data to {directory}")
    
    @staticmethod
    def load_from_csv(directory: str = "./data/fundamentals") -> tuple:
        """Load fundamental data from CSV"""
        import glob
        
        quarterly_data = {}
        annual_data = {}
        
        # Load quarterly
        for filepath in glob.glob(f"{directory}/quarterly/*.csv"):
            name = os.path.basename(filepath).replace('.csv', '').replace('_', ' ')
            quarterly_data[name] = pd.read_csv(filepath)
        
        # Load annual
        for filepath in glob.glob(f"{directory}/annual/*.csv"):
            name = os.path.basename(filepath).replace('.csv', '').replace('_', ' ')
            annual_data[name] = pd.read_csv(filepath)
        
        return quarterly_data, annual_data