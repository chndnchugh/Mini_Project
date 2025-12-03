from agents.base_agent import BaseAgent
from typing import Dict, List, Any
import pandas as pd
import numpy as np

class ValuationAgent(BaseAgent):
    """Valuation Analysis Agent"""
    
    def __init__(self, model_name: str = "llama3.2"):
        super().__init__("Valuation Agent", model_name)
        
        self.metrics = {
            'pe_ratio': 'Price to Earnings (P/E)',
            'pb_ratio': 'Price to Book (P/B)',
            'ps_ratio': 'Price to Sales (P/S)',
            'peg_ratio': 'PEG Ratio',
            'ev_ebitda': 'EV/EBITDA',
            'dividend_yield': 'Dividend Yield (%)',
            'market_cap': 'Market Cap (Cr)',
            'current_price': 'Current Price (₹)'
        }
        
        self.valuation_data = {}
        
        self.industry_averages = {
            'pe_ratio': 22.0,
            'pb_ratio': 3.5,
            'ps_ratio': 2.8,
            'ev_ebitda': 15.0,
            'peg_ratio': 1.5,
            'dividend_yield': 1.5
        }
        
        print("✓ Valuation Agent initialized")
    
    def load_valuation_data(self, data: Dict[str, pd.DataFrame], 
                           industry_averages: Dict[str, float] = None):
        """Load valuation data for companies"""
        self.valuation_data = data
        
        if industry_averages:
            self.industry_averages = industry_averages
        
        texts = []
        metadatas = []
        
        for company, df in data.items():
            if df.empty:
                continue
            
            for date in df['date'].unique():
                date_data = df[df['date'] == date]
                
                summary_parts = []
                for _, row in date_data.iterrows():
                    metric_name = self.metrics.get(row['metric'], row['metric'])
                    summary_parts.append(f"{metric_name}: {row['value']}")
                
                text = f"{company} Valuation {date}: " + ", ".join(summary_parts)
                texts.append(text)
                
                metadatas.append({
                    "company": company,
                    "date": str(date),
                    "type": "valuation_data"
                })
        
        if texts:
            self.add_documents(texts, metadatas)
            print(f"✓ Loaded valuation data for {len(data)} companies")
    
    def analyze(self, stock_name: str, target_period: int = 12) -> Dict[str, Any]:
        """Comprehensive valuation analysis"""
        print(f"\n💰 Analyzing valuation for {stock_name}...")
        
        if stock_name not in self.valuation_data:
            return {
                "stock": stock_name,
                "error": "No valuation data found.",
                "valuation_rating": "Unknown"
            }
        
        df = self.valuation_data[stock_name]
        latest_date = df['date'].max()
        latest_data = df[df['date'] == latest_date]
        
        metrics = {}
        for _, row in latest_data.iterrows():
            metrics[row['metric']] = float(row['value'])
        
        current_price = metrics.get('current_price', 0)
        
        valuations = {}
        
        if 'pe_ratio' in metrics:
            pe_fair_value = self._pe_valuation(metrics, current_price)
            valuations['pe_method'] = pe_fair_value
        
        if 'pb_ratio' in metrics:
            pb_fair_value = self._pb_valuation(metrics, current_price)
            valuations['pb_method'] = pb_fair_value
        
        if 'peg_ratio' in metrics:
            peg_fair_value = self._peg_valuation(metrics, current_price)
            valuations['peg_method'] = peg_fair_value
        
        if valuations:
            fair_value = np.mean(list(valuations.values()))
        else:
            fair_value = current_price
        
        if current_price > 0:
            upside_potential = ((fair_value - current_price) / current_price) * 100
        else:
            upside_potential = 0
        
        valuation_rating = self._get_valuation_rating(upside_potential)
        
        ai_insight = self._generate_valuation_insights(
            stock_name, metrics, fair_value, current_price, upside_potential
        )
        
        return {
            "stock": stock_name,
            "analysis_date": str(latest_date),
            "target_period_months": target_period,
            "current_price": float(current_price),
            "fair_value": float(fair_value),
            "target_price": float(fair_value),
            "upside_potential": float(upside_potential),
            "valuation_rating": valuation_rating,
            "valuation_methods": {
                method: {"fair_value": float(value), 
                        "upside": float(((value - current_price) / current_price) * 100)}
                for method, value in valuations.items()
            },
            "key_ratios": {
                "pe_ratio": metrics.get('pe_ratio', None),
                "pb_ratio": metrics.get('pb_ratio', None),
                "peg_ratio": metrics.get('peg_ratio', None),
                "ev_ebitda": metrics.get('ev_ebitda', None),
                "dividend_yield": metrics.get('dividend_yield', None)
            },
            "vs_industry": self._compare_to_industry(metrics),
            "ai_insight": ai_insight,
            "recommendation": self._get_recommendation(upside_potential, valuation_rating)
        }
    
    def _pe_valuation(self, metrics: Dict, current_price: float) -> float:
        """P/E ratio based valuation"""
        pe_ratio = metrics.get('pe_ratio', 0)
        industry_pe = self.industry_averages.get('pe_ratio', 20)
        
        if pe_ratio > 0:
            fair_value = current_price * (industry_pe / pe_ratio)
            return fair_value
        
        return current_price
    
    def _pb_valuation(self, metrics: Dict, current_price: float) -> float:
        """P/B ratio based valuation"""
        pb_ratio = metrics.get('pb_ratio', 0)
        industry_pb = self.industry_averages.get('pb_ratio', 3.0)
        
        if pb_ratio > 0:
            fair_value = current_price * (industry_pb / pb_ratio)
            return fair_value
        
        return current_price
    
    def _peg_valuation(self, metrics: Dict, current_price: float) -> float:
        """PEG ratio based valuation"""
        peg_ratio = metrics.get('peg_ratio', 0)
        
        if peg_ratio > 0:
            fair_value = current_price * (1.0 / peg_ratio)
            return fair_value
        
        return current_price
    
    def _compare_to_industry(self, metrics: Dict) -> Dict[str, str]:
        """Compare ratios to industry averages"""
        comparisons = {}
        
        for metric, industry_avg in self.industry_averages.items():
            if metric in metrics:
                current = metrics[metric]
                
                if metric in ['pe_ratio', 'pb_ratio', 'ps_ratio', 'ev_ebitda', 'peg_ratio']:
                    if current < industry_avg * 0.8:
                        comparisons[metric] = f"Undervalued ({current:.1f} vs {industry_avg:.1f})"
                    elif current > industry_avg * 1.2:
                        comparisons