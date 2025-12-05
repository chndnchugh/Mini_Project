from agents.base_agent import BaseAgent
from typing import Dict, List, Any, Optional
import pandas as pd
import numpy as np
from datetime import datetime, timedelta

class FundamentalAgent(BaseAgent):
    """
    Fundamental Analysis Agent
    Analyzes quarterly and annual reports of NSE-listed companies
    including income statements, balance sheets, cash flows, and key ratios
    """
    
    def __init__(self, model_name: str = "llama3.2"):
        super().__init__("Fundamental Agent", model_name)
        
        # Financial statement metrics
        self.income_statement_metrics = {
            'revenue': 'Total Revenue (Cr)',
            'revenue_growth': 'Revenue Growth (%)',
            'operating_profit': 'Operating Profit (Cr)',
            'operating_margin': 'Operating Margin (%)',
            'net_profit': 'Net Profit (Cr)',
            'net_margin': 'Net Profit Margin (%)',
            'ebitda': 'EBITDA (Cr)',
            'ebitda_margin': 'EBITDA Margin (%)',
            'eps': 'Earnings Per Share (₹)',
            'eps_growth': 'EPS Growth (%)'
        }
        
        self.balance_sheet_metrics = {
            'total_assets': 'Total Assets (Cr)',
            'total_liabilities': 'Total Liabilities (Cr)',
            'shareholders_equity': 'Shareholders Equity (Cr)',
            'total_debt': 'Total Debt (Cr)',
            'cash_equivalents': 'Cash & Equivalents (Cr)',
            'working_capital': 'Working Capital (Cr)',
            'inventory': 'Inventory (Cr)',
            'receivables': 'Trade Receivables (Cr)',
            'payables': 'Trade Payables (Cr)',
            'fixed_assets': 'Fixed Assets (Cr)'
        }
        
        self.cash_flow_metrics = {
            'operating_cash_flow': 'Operating Cash Flow (Cr)',
            'investing_cash_flow': 'Investing Cash Flow (Cr)',
            'financing_cash_flow': 'Financing Cash Flow (Cr)',
            'free_cash_flow': 'Free Cash Flow (Cr)',
            'capex': 'Capital Expenditure (Cr)',
            'dividends_paid': 'Dividends Paid (Cr)'
        }
        
        self.financial_ratios = {
            # Profitability
            'roe': 'Return on Equity (%)',
            'roce': 'Return on Capital Employed (%)',
            'roa': 'Return on Assets (%)',
            'gross_margin': 'Gross Margin (%)',
            
            # Liquidity
            'current_ratio': 'Current Ratio',
            'quick_ratio': 'Quick Ratio',
            'cash_ratio': 'Cash Ratio',
            
            # Leverage
            'debt_to_equity': 'Debt to Equity',
            'debt_to_assets': 'Debt to Assets',
            'interest_coverage': 'Interest Coverage Ratio',
            
            # Efficiency
            'asset_turnover': 'Asset Turnover',
            'inventory_turnover': 'Inventory Turnover',
            'receivables_turnover': 'Receivables Turnover',
            'payables_turnover': 'Payables Turnover',
            
            # Per Share
            'book_value_per_share': 'Book Value Per Share (₹)',
            'dividend_per_share': 'Dividend Per Share (₹)',
            'dividend_payout': 'Dividend Payout Ratio (%)'
        }
        
        # Store financial data
        self.quarterly_data = {}
        self.annual_data = {}
        self.company_profiles = {}
        
        # Sector benchmarks
        self.sector_benchmarks = {
            "IT": {
                'roe': 25.0, 'roce': 30.0, 'net_margin': 18.0,
                'debt_to_equity': 0.1, 'current_ratio': 2.5
            },
            "Banking": {
                'roe': 15.0, 'roce': 12.0, 'net_margin': 15.0,
                'debt_to_equity': 8.0, 'current_ratio': 1.0
            },
            "Pharma": {
                'roe': 18.0, 'roce': 20.0, 'net_margin': 12.0,
                'debt_to_equity': 0.3, 'current_ratio': 2.0
            },
            "Auto": {
                'roe': 15.0, 'roce': 18.0, 'net_margin': 8.0,
                'debt_to_equity': 0.5, 'current_ratio': 1.2
            },
            "FMCG": {
                'roe': 35.0, 'roce': 40.0, 'net_margin': 15.0,
                'debt_to_equity': 0.2, 'current_ratio': 1.5
            },
            "Infrastructure": {
                'roe': 12.0, 'roce': 14.0, 'net_margin': 8.0,
                'debt_to_equity': 1.0, 'current_ratio': 1.2
            },
            "Metals": {
                'roe': 12.0, 'roce': 15.0, 'net_margin': 10.0,
                'debt_to_equity': 0.8, 'current_ratio': 1.0
            },
            "Oil & Gas": {
                'roe': 15.0, 'roce': 18.0, 'net_margin': 8.0,
                'debt_to_equity': 0.6, 'current_ratio': 1.2
            },
            "Default": {
                'roe': 15.0, 'roce': 18.0, 'net_margin': 10.0,
                'debt_to_equity': 0.5, 'current_ratio': 1.5
            }
        }
        
        print("✓ Fundamental Analysis Agent initialized")
    
    def load_quarterly_data(self, data: Dict[str, pd.DataFrame]):
        """
        Load quarterly financial data
        
        Args:
            data: Dict with company names as keys and DataFrames as values
                  DataFrame should have columns for various financial metrics
        """
        self.quarterly_data = data
        
        texts = []
        metadatas = []
        
        for company, df in data.items():
            if df.empty:
                continue
            
            for _, row in df.iterrows():
                quarter = row.get('quarter', 'Unknown')
                year = row.get('year', 'Unknown')
                
                # Create summary text
                summary_parts = [f"{company} Q{quarter} {year}:"]
                
                for metric in ['revenue', 'net_profit', 'eps', 'roe']:
                    if metric in row and pd.notna(row[metric]):
                        metric_name = self.income_statement_metrics.get(
                            metric, self.financial_ratios.get(metric, metric)
                        )
                        summary_parts.append(f"{metric_name}: {row[metric]}")
                
                text = " ".join(summary_parts)
                texts.append(text)
                
                metadatas.append({
                    "company": company,
                    "quarter": str(quarter),
                    "year": str(year),
                    "type": "quarterly_results"
                })
        
        if texts:
            self.add_documents(texts, metadatas)
            print(f"✓ Loaded quarterly data for {len(data)} companies")
    
    def load_annual_data(self, data: Dict[str, pd.DataFrame]):
        """
        Load annual financial data
        
        Args:
            data: Dict with company names as keys and DataFrames as values
        """
        self.annual_data = data
        
        texts = []
        metadatas = []
        
        for company, df in data.items():
            if df.empty:
                continue
            
            for _, row in df.iterrows():
                year = row.get('year', 'Unknown')
                
                summary_parts = [f"{company} Annual {year}:"]
                
                key_metrics = ['revenue', 'net_profit', 'roe', 'roce', 'debt_to_equity']
                for metric in key_metrics:
                    if metric in row and pd.notna(row[metric]):
                        metric_name = self.income_statement_metrics.get(
                            metric, self.financial_ratios.get(metric, metric)
                        )
                        summary_parts.append(f"{metric_name}: {row[metric]}")
                
                text = " ".join(summary_parts)
                texts.append(text)
                
                metadatas.append({
                    "company": company,
                    "year": str(year),
                    "type": "annual_results"
                })
        
        if texts:
            self.add_documents(texts, metadatas)
            print(f"✓ Loaded annual data for {len(data)} companies")
    
    def load_company_profile(self, company: str, profile: Dict[str, Any]):
        """Load company profile information"""
        self.company_profiles[company] = profile
        
        # Add to vector store
        text = f"{company} Profile: Sector {profile.get('sector', 'Unknown')}, " \
               f"Industry {profile.get('industry', 'Unknown')}, " \
               f"Founded {profile.get('founded', 'Unknown')}, " \
               f"Headquarters {profile.get('headquarters', 'Unknown')}"
        
        self.add_documents([text], [{"company": company, "type": "profile"}])
    
    def analyze(self, stock_name: str, period: str = "quarterly") -> Dict[str, Any]:
        """
        Comprehensive fundamental analysis
        
        Args:
            stock_name: Name of the company
            period: "quarterly" or "annual"
            
        Returns:
            Dict containing fundamental analysis
        """
        print(f"\n📊 Analyzing fundamentals for {stock_name}...")
        
        result = {
            "stock": stock_name,
            "analysis_date": datetime.now().strftime("%Y-%m-%d"),
            "period": period
        }
        
        # Get relevant data
        if period == "quarterly":
            data = self.quarterly_data.get(stock_name)
        else:
            data = self.annual_data.get(stock_name)
        
        if data is None or data.empty:
            return {
                "stock": stock_name,
                "error": f"No {period} data available for {stock_name}",
                "recommendation": "Unable to analyze"
            }
        
        # Financial Performance Analysis
        performance = self._analyze_financial_performance(stock_name, data)
        result["financial_performance"] = performance
        
        # Ratio Analysis
        ratios = self._analyze_ratios(stock_name, data)
        result["ratio_analysis"] = ratios
        
        # Growth Analysis
        growth = self._analyze_growth_trends(stock_name, data)
        result["growth_analysis"] = growth
        
        # Quality Assessment
        quality = self._assess_earnings_quality(stock_name, data)
        result["quality_assessment"] = quality
        
        # Peer Comparison
        peer_comparison = self._compare_with_peers(stock_name, data)
        result["peer_comparison"] = peer_comparison
        
        # Generate Fundamental Score
        fundamental_score = self._calculate_fundamental_score(result)
        result["fundamental_score"] = fundamental_score
        
        # AI Insights
        ai_insight = self._generate_fundamental_insights(stock_name, result)
        result["ai_insight"] = ai_insight
        
        # Recommendation
        result["recommendation"] = self._get_fundamental_recommendation(fundamental_score)
        
        return result
    
    def _analyze_financial_performance(self, stock_name: str, data: pd.DataFrame) -> Dict[str, Any]:
        """Analyze key financial performance metrics"""
        latest = data.iloc[-1] if not data.empty else {}
        
        performance = {
            "latest_period": {},
            "yoy_comparison": {},
            "trends": {}
        }
        
        # Latest period metrics
        key_metrics = ['revenue', 'operating_profit', 'net_profit', 'ebitda', 'eps']
        for metric in key_metrics:
            if metric in data.columns:
                value = latest.get(metric)
                if pd.notna(value):
                    performance["latest_period"][metric] = {
                        "value": float(value),
                        "label": self.income_statement_metrics.get(metric, metric)
                    }
        
        # YoY Comparison (if enough data)
        if len(data) >= 4:
            yoy_data = data.iloc[-5] if len(data) >= 5 else data.iloc[0]
            for metric in key_metrics:
                if metric in data.columns:
                    current = latest.get(metric, 0)
                    previous = yoy_data.get(metric, 0)
                    if previous and previous != 0:
                        growth = ((current - previous) / abs(previous)) * 100
                        performance["yoy_comparison"][metric] = {
                            "current": float(current) if pd.notna(current) else None,
                            "previous": float(previous) if pd.notna(previous) else None,
                            "growth": float(growth) if pd.notna(growth) else None
                        }
        
        # Calculate trends
        for metric in ['revenue', 'net_profit', 'eps']:
            if metric in data.columns:
                values = data[metric].dropna()
                if len(values) >= 3:
                    trend = self._calculate_trend(values)
                    performance["trends"][metric] = trend
        
        return performance
    
    def _analyze_ratios(self, stock_name: str, data: pd.DataFrame) -> Dict[str, Any]:
        """Analyze financial ratios"""
        latest = data.iloc[-1] if not data.empty else {}
        
        ratios = {
            "profitability": {},
            "liquidity": {},
            "leverage": {},
            "efficiency": {}
        }
        
        # Profitability ratios
        profitability_metrics = ['roe', 'roce', 'roa', 'net_margin', 'operating_margin', 'ebitda_margin']
        for metric in profitability_metrics:
            if metric in data.columns:
                value = latest.get(metric)
                if pd.notna(value):
                    ratios["profitability"][metric] = {
                        "value": float(value),
                        "label": self.financial_ratios.get(metric, metric),
                        "rating": self._rate_ratio(metric, value)
                    }
        
        # Liquidity ratios
        liquidity_metrics = ['current_ratio', 'quick_ratio', 'cash_ratio']
        for metric in liquidity_metrics:
            if metric in data.columns:
                value = latest.get(metric)
                if pd.notna(value):
                    ratios["liquidity"][metric] = {
                        "value": float(value),
                        "label": self.financial_ratios.get(metric, metric),
                        "rating": self._rate_ratio(metric, value)
                    }
        
        # Leverage ratios
        leverage_metrics = ['debt_to_equity', 'debt_to_assets', 'interest_coverage']
        for metric in leverage_metrics:
            if metric in data.columns:
                value = latest.get(metric)
                if pd.notna(value):
                    ratios["leverage"][metric] = {
                        "value": float(value),
                        "label": self.financial_ratios.get(metric, metric),
                        "rating": self._rate_ratio(metric, value)
                    }
        
        # Efficiency ratios
        efficiency_metrics = ['asset_turnover', 'inventory_turnover', 'receivables_turnover']
        for metric in efficiency_metrics:
            if metric in data.columns:
                value = latest.get(metric)
                if pd.notna(value):
                    ratios["efficiency"][metric] = {
                        "value": float(value),
                        "label": self.financial_ratios.get(metric, metric),
                        "rating": self._rate_ratio(metric, value)
                    }
        
        return ratios
    
    def _rate_ratio(self, metric: str, value: float, sector: str = "Default") -> str:
        """Rate a ratio as Good, Average, or Poor"""
        benchmarks = self.sector_benchmarks.get(sector, self.sector_benchmarks["Default"])
        benchmark = benchmarks.get(metric)
        
        if benchmark is None:
            return "N/A"
        
        # Metrics where higher is better
        higher_better = ['roe', 'roce', 'roa', 'net_margin', 'operating_margin', 
                        'current_ratio', 'quick_ratio', 'interest_coverage', 'asset_turnover']
        
        # Metrics where lower is better
        lower_better = ['debt_to_equity', 'debt_to_assets']
        
        if metric in higher_better:
            if value >= benchmark * 1.2:
                return "Excellent"
            elif value >= benchmark:
                return "Good"
            elif value >= benchmark * 0.8:
                return "Average"
            else:
                return "Below Average"
        elif metric in lower_better:
            if value <= benchmark * 0.8:
                return "Excellent"
            elif value <= benchmark:
                return "Good"
            elif value <= benchmark * 1.2:
                return "Average"
            else:
                return "Concerning"
        else:
            return "N/A"
    
    def _analyze_growth_trends(self, stock_name: str, data: pd.DataFrame) -> Dict[str, Any]:
        """Analyze growth trends"""
        growth = {
            "revenue_cagr": None,
            "profit_cagr": None,
            "eps_cagr": None,
            "trend_analysis": {},
            "growth_consistency": None
        }
        
        # Calculate CAGR for key metrics
        if 'revenue' in data.columns and len(data) >= 4:
            revenue_cagr = self._calculate_cagr(data['revenue'])
            if revenue_cagr is not None:
                growth["revenue_cagr"] = float(revenue_cagr)
        
        if 'net_profit' in data.columns and len(data) >= 4:
            profit_cagr = self._calculate_cagr(data['net_profit'])
            if profit_cagr is not None:
                growth["profit_cagr"] = float(profit_cagr)
        
        if 'eps' in data.columns and len(data) >= 4:
            eps_cagr = self._calculate_cagr(data['eps'])
            if eps_cagr is not None:
                growth["eps_cagr"] = float(eps_cagr)
        
        # Trend analysis
        for metric in ['revenue', 'net_profit', 'operating_margin']:
            if metric in data.columns:
                values = data[metric].dropna()
                if len(values) >= 3:
                    growth["trend_analysis"][metric] = self._calculate_trend(values)
        
        # Growth consistency
        growth["growth_consistency"] = self._assess_growth_consistency(data)
        
        return growth
    
    def _calculate_cagr(self, series: pd.Series) -> Optional[float]:
        """Calculate Compound Annual Growth Rate"""
        clean_series = series.dropna()
        if len(clean_series) < 2:
            return None
        
        start_value = clean_series.iloc[0]
        end_value = clean_series.iloc[-1]
        periods = len(clean_series) - 1
        
        if start_value <= 0 or periods == 0:
            return None
        
        cagr = ((end_value / start_value) ** (1 / periods) - 1) * 100
        return cagr
    
    def _calculate_trend(self, series: pd.Series) -> str:
        """Calculate trend direction"""
        if len(series) < 3:
            return "Insufficient Data"
        
        # Simple linear regression trend
        x = np.arange(len(series))
        y = series.values
        
        slope = np.polyfit(x, y, 1)[0]
        mean_val = np.mean(y)
        
        if mean_val == 0:
            return "Flat"
        
        slope_pct = (slope / mean_val) * 100
        
        if slope_pct > 5:
            return "Strong Uptrend"
        elif slope_pct > 1:
            return "Uptrend"
        elif slope_pct > -1:
            return "Flat"
        elif slope_pct > -5:
            return "Downtrend"
        else:
            return "Strong Downtrend"
    
    def _assess_growth_consistency(self, data: pd.DataFrame) -> str:
        """Assess consistency of growth"""
        if 'revenue_growth' not in data.columns:
            return "Unable to assess"
        
        growth_values = data['revenue_growth'].dropna()
        if len(growth_values) < 4:
            return "Insufficient data"
        
        positive_growth = sum(1 for g in growth_values if g > 0)
        total = len(growth_values)
        
        ratio = positive_growth / total
        
        if ratio >= 0.9:
            return "Highly Consistent"
        elif ratio >= 0.7:
            return "Consistent"
        elif ratio >= 0.5:
            return "Moderate"
        else:
            return "Inconsistent"
    
    def _assess_earnings_quality(self, stock_name: str, data: pd.DataFrame) -> Dict[str, Any]:
        """Assess earnings quality"""
        quality = {
            "cash_conversion": None,
            "earnings_persistence": None,
            "accrual_ratio": None,
            "quality_score": None,
            "flags": []
        }
        
        latest = data.iloc[-1] if not data.empty else {}
        
        # Cash conversion (OCF / Net Profit)
        ocf = latest.get('operating_cash_flow', 0)
        net_profit = latest.get('net_profit', 0)
        
        if net_profit and net_profit > 0:
            cash_conversion = (ocf / net_profit) * 100
            quality["cash_conversion"] = float(cash_conversion)
            
            if cash_conversion < 50:
                quality["flags"].append("Low cash conversion - earnings quality concern")
            elif cash_conversion > 150:
                quality["flags"].append("High cash conversion - strong earnings quality")
        
        # Earnings persistence (correlation of earnings over time)
        if 'net_profit' in data.columns and len(data) >= 4:
            profits = data['net_profit'].dropna()
            if len(profits) >= 4:
                # Check if earnings are stable/growing
                std_dev = profits.std()
                mean_val = profits.mean()
                if mean_val != 0:
                    cv = std_dev / abs(mean_val)  # Coefficient of variation
                    if cv < 0.3:
                        quality["earnings_persistence"] = "High"
                    elif cv < 0.5:
                        quality["earnings_persistence"] = "Moderate"
                    else:
                        quality["earnings_persistence"] = "Low"
                        quality["flags"].append("Volatile earnings - lower predictability")
        
        # Overall quality score
        score = 70  # Base score
        
        if quality["cash_conversion"]:
            if quality["cash_conversion"] > 100:
                score += 15
            elif quality["cash_conversion"] > 70:
                score += 5
            elif quality["cash_conversion"] < 50:
                score -= 15
        
        if quality["earnings_persistence"] == "High":
            score += 15
        elif quality["earnings_persistence"] == "Low":
            score -= 10
        
        quality["quality_score"] = min(max(score, 0), 100)
        
        return quality
    
    def _compare_with_peers(self, stock_name: str, data: pd.DataFrame) -> Dict[str, Any]:
        """Compare with sector peers"""
        # Get sector
        profile = self.company_profiles.get(stock_name, {})
        sector = profile.get('sector', 'Default')
        
        benchmarks = self.sector_benchmarks.get(sector, self.sector_benchmarks["Default"])
        
        latest = data.iloc[-1] if not data.empty else {}
        
        comparison = {
            "sector": sector,
            "metrics_comparison": {},
            "vs_benchmark": {}
        }
        
        for metric, benchmark in benchmarks.items():
            if metric in data.columns:
                value = latest.get(metric)
                if pd.notna(value):
                    diff = value - benchmark
                    pct_diff = (diff / benchmark) * 100 if benchmark != 0 else 0
                    
                    comparison["metrics_comparison"][metric] = {
                        "company_value": float(value),
                        "sector_benchmark": float(benchmark),
                        "difference": float(diff),
                        "pct_difference": float(pct_diff),
                        "assessment": self._assess_vs_benchmark(metric, pct_diff)
                    }
        
        return comparison
    
    def _assess_vs_benchmark(self, metric: str, pct_diff: float) -> str:
        """Assess performance vs benchmark"""
        higher_better = ['roe', 'roce', 'net_margin', 'current_ratio']
        lower_better = ['debt_to_equity']
        
        if metric in higher_better:
            if pct_diff > 20:
                return "Significantly Above Benchmark"
            elif pct_diff > 5:
                return "Above Benchmark"
            elif pct_diff > -5:
                return "In Line with Benchmark"
            elif pct_diff > -20:
                return "Below Benchmark"
            else:
                return "Significantly Below Benchmark"
        elif metric in lower_better:
            if pct_diff < -20:
                return "Significantly Better than Benchmark"
            elif pct_diff < -5:
                return "Better than Benchmark"
            elif pct_diff < 5:
                return "In Line with Benchmark"
            elif pct_diff < 20:
                return "Worse than Benchmark"
            else:
                return "Significantly Worse than Benchmark"
        else:
            return "N/A"
    
    def _calculate_fundamental_score(self, result: Dict) -> Dict[str, Any]:
        """Calculate overall fundamental score"""
        scores = {}
        weights = {
            "profitability": 0.3,
            "growth": 0.25,
            "leverage": 0.2,
            "quality": 0.15,
            "liquidity": 0.1
        }
        
        # Profitability score
        prof_ratios = result.get("ratio_analysis", {}).get("profitability", {})
        prof_score = self._score_ratios(prof_ratios)
        scores["profitability"] = prof_score
        
        # Growth score
        growth = result.get("growth_analysis", {})
        growth_score = 50  # Base
        if growth.get("revenue_cagr"):
            if growth["revenue_cagr"] > 15:
                growth_score += 25
            elif growth["revenue_cagr"] > 10:
                growth_score += 15
            elif growth["revenue_cagr"] > 5:
                growth_score += 5
            elif growth["revenue_cagr"] < 0:
                growth_score -= 20
        
        if growth.get("profit_cagr"):
            if growth["profit_cagr"] > 20:
                growth_score += 25
            elif growth["profit_cagr"] > 10:
                growth_score += 15
            elif growth["profit_cagr"] < 0:
                growth_score -= 20
        
        scores["growth"] = min(max(growth_score, 0), 100)
        
        # Leverage score
        lev_ratios = result.get("ratio_analysis", {}).get("leverage", {})
        lev_score = self._score_ratios(lev_ratios, inverse=True)
        scores["leverage"] = lev_score
        
        # Quality score
        quality = result.get("quality_assessment", {})
        scores["quality"] = quality.get("quality_score", 50)
        
        # Liquidity score
        liq_ratios = result.get("ratio_analysis", {}).get("liquidity", {})
        liq_score = self._score_ratios(liq_ratios)
        scores["liquidity"] = liq_score
        
        # Calculate weighted total
        total_score = sum(
            scores.get(cat, 50) * weight 
            for cat, weight in weights.items()
        )
        
        # Determine rating
        if total_score >= 80:
            rating = "Excellent"
        elif total_score >= 65:
            rating = "Good"
        elif total_score >= 50:
            rating = "Average"
        elif total_score >= 35:
            rating = "Below Average"
        else:
            rating = "Poor"
        
        return {
            "overall_score": float(total_score),
            "rating": rating,
            "component_scores": scores,
            "weights": weights
        }
    
    def _score_ratios(self, ratios: Dict, inverse: bool = False) -> float:
        """Score a set of ratios"""
        if not ratios:
            return 50  # Neutral
        
        rating_scores = {
            "Excellent": 100,
            "Good": 75,
            "Average": 50,
            "Below Average": 25,
            "Concerning": 10
        }
        
        if inverse:
            rating_scores = {
                "Excellent": 100,
                "Good": 75,
                "Average": 50,
                "Below Average": 75,  # For leverage, lower is better
                "Concerning": 25
            }
        
        scores = []
        for metric, data in ratios.items():
            rating = data.get("rating", "Average")
            score = rating_scores.get(rating, 50)
            scores.append(score)
        
        return np.mean(scores) if scores else 50
    
    def _generate_fundamental_insights(self, stock_name: str, result: Dict) -> str:
        """Generate AI-powered fundamental insights"""
        
        context_parts = [f"Company: {stock_name}"]
        
        # Add key metrics
        perf = result.get("financial_performance", {})
        latest = perf.get("latest_period", {})
        for metric, data in latest.items():
            context_parts.append(f"{data.get('label', metric)}: {data.get('value', 'N/A')}")
        
        # Add growth
        growth = result.get("growth_analysis", {})
        if growth.get("revenue_cagr"):
            context_parts.append(f"Revenue CAGR: {growth['revenue_cagr']:.1f}%")
        if growth.get("profit_cagr"):
            context_parts.append(f"Profit CAGR: {growth['profit_cagr']:.1f}%")
        
        # Add score
        score = result.get("fundamental_score", {})
        context_parts.append(f"Fundamental Score: {score.get('overall_score', 0):.0f}/100")
        context_parts.append(f"Rating: {score.get('rating', 'N/A')}")
        
        # Add quality flags
        quality = result.get("quality_assessment", {})
        flags = quality.get("flags", [])
        if flags:
            context_parts.append("Quality Concerns: " + "; ".join(flags))
        
        context = "\n".join(context_parts)
        
        prompt = f"""You are a fundamental analyst covering NSE stocks. Analyze the following:

{context}

Provide insights including:
1. Financial health assessment
2. Key strengths and weaknesses
3. Areas of concern (if any)
4. Investment thesis summary

Keep response under 200 words and focus on actionable insights."""

        return self.generate_response(prompt)
    
    def _get_fundamental_recommendation(self, score: Dict) -> Dict[str, Any]:
        """Get recommendation based on fundamental analysis"""
        overall = score.get("overall_score", 50)
        rating = score.get("rating", "Average")
        
        if overall >= 75:
            action = "Strong Buy"
            rationale = "Excellent fundamentals across all parameters"
            confidence = 0.85
        elif overall >= 60:
            action = "Buy"
            rationale = "Good fundamentals with room for improvement"
            confidence = 0.7
        elif overall >= 45:
            action = "Hold"
            rationale = "Average fundamentals, monitor for changes"
            confidence = 0.5
        elif overall >= 30:
            action = "Sell"
            rationale = "Below average fundamentals, consider exiting"
            confidence = 0.65
        else:
            action = "Strong Sell"
            rationale = "Poor fundamentals, avoid or exit"
            confidence = 0.8
        
        return {
            "action": action,
            "rationale": rationale,
            "confidence": confidence,
            "fundamental_rating": rating,
            "score": float(overall)
        }
    
    def get_quick_analysis(self, stock_name: str) -> Dict[str, Any]:
        """Get quick fundamental overview"""
        data = self.quarterly_data.get(stock_name) or self.annual_data.get(stock_name)
        
        if data is None or data.empty:
            return {"error": f"No data available for {stock_name}"}
        
        latest = data.iloc[-1]
        
        return {
            "stock": stock_name,
            "revenue": float(latest.get('revenue', 0)) if pd.notna(latest.get('revenue')) else None,
            "net_profit": float(latest.get('net_profit', 0)) if pd.notna(latest.get('net_profit')) else None,
            "roe": float(latest.get('roe', 0)) if pd.notna(latest.get('roe')) else None,
            "debt_to_equity": float(latest.get('debt_to_equity', 0)) if pd.notna(latest.get('debt_to_equity')) else None,
            "eps": float(latest.get('eps', 0)) if pd.notna(latest.get('eps')) else None
        }