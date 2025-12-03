from agents.base_agent import BaseAgent
from typing import Dict, List, Any
import pandas as pd
import numpy as np
from datetime import datetime, timedelta

class MacroEconomicAgent(BaseAgent):
    """Macro Economic Indicator Analysis Agent"""
    
    def __init__(self, model_name: str = "llama3.2"):
        super().__init__("Macro Economic Agent", model_name)
        
        # Key indicators to track
        self.indicators = {
            "gdp_growth": "GDP Growth Rate (%)",
            "inflation_cpi": "CPI Inflation (%)",
            "inflation_wpi": "WPI Inflation (%)",
            "repo_rate": "RBI Repo Rate (%)",
            "usd_inr": "USD-INR Exchange Rate",
            "crude_oil": "Crude Oil Price (USD/barrel)",
            "industrial_production": "IIP Growth (%)",
            "fiscal_deficit": "Fiscal Deficit (% of GDP)"
        }
        
        self.economic_data = {}
        print("✓ Macro Economic Agent initialized")
    
    def load_economic_data(self, data: Dict[str, pd.DataFrame]):
        """
        Load economic indicator data
        
        Args:
            data: Dict with indicator names as keys and DataFrames as values
                  Each DataFrame should have columns: 'date', 'value'
        """
        self.economic_data = data
        
        # Create embeddings from economic reports
        texts = []
        metadatas = []
        
        for indicator, df in data.items():
            if df.empty:
                continue
            
            # Create summary text for each time period
            for idx, row in df.iterrows():
                text = f"{self.indicators.get(indicator, indicator)}: {row['value']} on {row['date']}"
                texts.append(text)
                metadatas.append({
                    "indicator": indicator,
                    "date": str(row['date']),
                    "value": float(row['value'])
                })
        
        if texts:
            self.add_documents(texts, metadatas)
            print(f"✓ Loaded {len(texts)} economic data points")
    
    def get_latest_indicators(self) -> Dict[str, Any]:
        """Get latest values of all indicators"""
        latest = {}
        for indicator, df in self.economic_data.items():
            if not df.empty:
                latest[indicator] = {
                    "value": float(df.iloc[-1]['value']),
                    "date": str(df.iloc[-1]['date']),
                    "name": self.indicators.get(indicator, indicator)
                }
        return latest
    
    def calculate_trend(self, indicator: str, periods: int = 3) -> str:
        """Calculate trend for an indicator"""
        if indicator not in self.economic_data:
            return "unknown"
        
        df = self.economic_data[indicator]
        if len(df) < periods:
            return "insufficient_data"
        
        recent_values = df.tail(periods)['value'].values
        
        # Calculate simple trend
        if all(recent_values[i] <= recent_values[i+1] for i in range(len(recent_values)-1)):
            return "increasing"
        elif all(recent_values[i] >= recent_values[i+1] for i in range(len(recent_values)-1)):
            return "decreasing"
        else:
            return "stable"
    
    def analyze(self, stock_name: str = None, timeframe: str = "current") -> Dict[str, Any]:
        """
        Analyze macro economic indicators and their impact
        
        Args:
            stock_name: Optional stock name for sector-specific analysis
            timeframe: Analysis timeframe ("current", "1m", "3m", "1y")
        """
        print(f"\n📊 Analyzing macro economic indicators...")
        
        if not self.economic_data:
            return {
                "error": "No economic data loaded. Please load data first.",
                "indicators": {},
                "outlook": "unknown"
            }
        
        # Get latest indicators
        latest = self.get_latest_indicators()
        
        # Calculate trends
        trends = {}
        for indicator in self.economic_data.keys():
            trends[indicator] = self.calculate_trend(indicator)
        
        # Retrieve relevant economic context
        query = f"economic indicators impact on {stock_name if stock_name else 'Indian stock market'}"
        context_docs = self.retrieve_context(query, k=5)
        
        # Build context for LLM
        indicator_summary = []
        for indicator, data in latest.items():
            trend = trends.get(indicator, "stable")
            indicator_summary.append(
                f"- {data['name']}: {data['value']:.2f} ({trend})"
            )
        
        context_text = "\n".join(indicator_summary)
        
        # Generate LLM analysis
        prompt = f"""You are a macro economist analyzing the Indian economy. Based on the following indicators, provide analysis.

Current Economic Indicators:
{context_text}

{"Analysis for: " + stock_name if stock_name else "General Market Analysis"}

Provide:
1. Overall economic outlook (Positive/Negative/Neutral)
2. Key concerns or opportunities
3. Impact on {"the stock/sector" if stock_name else "Indian equity markets"}
4. Expected trend for next 3-6 months

Consider:
- Inflation trends and monetary policy
- GDP growth momentum
- Currency stability
- Global factors (crude oil, USD)

Keep response under 200 words."""

        llm_insight = self.generate_response(prompt)
        
        # Calculate economic health score (0-100)
        scores = []
        
        # GDP growth (higher is better)
        if "gdp_growth" in latest:
            gdp = latest["gdp_growth"]["value"]
            scores.append(min(gdp * 10, 100))
        
        # Inflation (5-6% is optimal, higher/lower is worse)
        if "inflation_cpi" in latest:
            inflation = latest["inflation_cpi"]["value"]
            inflation_score = 100 - abs(inflation - 5.5) * 10
            scores.append(max(inflation_score, 0))
        
        # Repo rate (stable is good)
        if "repo_rate" in latest:
            scores.append(60)  # Neutral score
        
        # USD-INR (lower is better)
        if "usd_inr" in latest:
            usd_inr = latest["usd_inr"]["value"]
            usd_score = 100 - (usd_inr - 75) * 2  # 75 as baseline
            scores.append(max(min(usd_score, 100), 0))
        
        health_score = np.mean(scores) if scores else 50
        
        # Determine overall outlook
        if health_score > 70:
            outlook = "Positive"
            market_impact = "Bullish"
        elif health_score < 40:
            outlook = "Negative"
            market_impact = "Bearish"
        else:
            outlook = "Neutral"
            market_impact = "Mixed"
        
        return {
            "timeframe": timeframe,
            "stock": stock_name,
            "indicators": latest,
            "trends": trends,
            "economic_health_score": float(health_score),
            "outlook": outlook,
            "market_impact": market_impact,
            "llm_insight": llm_insight,
            "key_factors": self._identify_key_factors(latest, trends)
        }
    
    def _identify_key_factors(self, indicators: Dict, trends: Dict) -> List[str]:
        """Identify key factors affecting the economy"""
        factors = []
        
        # Check inflation
        if "inflation_cpi" in indicators:
            inflation = indicators["inflation_cpi"]["value"]
            if inflation > 6:
                factors.append(f"High inflation at {inflation:.1f}% (above RBI target)")
            elif inflation < 2:
                factors.append(f"Low inflation at {inflation:.1f}% (below target)")
        
        # Check GDP
        if "gdp_growth" in indicators:
            gdp = indicators["gdp_growth"]["value"]
            if gdp > 7:
                factors.append(f"Strong GDP growth at {gdp:.1f}%")
            elif gdp < 5:
                factors.append(f"Weak GDP growth at {gdp:.1f}%")
        
        # Check currency
        if "usd_inr" in indicators:
            usd_inr = indicators["usd_inr"]["value"]
            if usd_inr > 83:
                factors.append(f"Rupee weakness at ₹{usd_inr:.2f}/USD")
        
        # Check crude oil
        if "crude_oil" in indicators:
            crude = indicators["crude_oil"]["value"]
            if crude > 90:
                factors.append(f"High crude oil at ${crude:.2f}/barrel")
        
        return factors if factors else ["Economic indicators within normal ranges"]
    
    def compare_periods(self, indicator: str, periods: List[str]) -> Dict[str, Any]:
        """Compare indicator across different time periods"""
        if indicator not in self.economic_data:
            return {"error": f"Indicator {indicator} not found"}
        
        df = self.economic_data[indicator]
        comparison = {}
        
        for period in periods:
            # Simple implementation - can be enhanced
            if period in df['date'].astype(str).values:
                value = df[df['date'].astype(str) == period]['value'].iloc[0]
                comparison[period] = float(value)
        
        return {
            "indicator": self.indicators.get(indicator, indicator),
            "comparison": comparison
        }