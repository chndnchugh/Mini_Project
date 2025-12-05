from agents.base_agent import BaseAgent
from typing import Dict, List, Any, Optional
import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import json

class GeopoliticalAgent(BaseAgent):
    """
    Geopolitical Analysis Agent
    Tracks tariffs, G20 meetings, policy changes, wars/conflicts, pandemics, 
    and natural disasters that may affect NSE stock prices
    """
    
    def __init__(self, model_name: str = "llama3.2"):
        super().__init__("Geopolitical Agent", model_name)
        
        # Categories of geopolitical events
        self.event_categories = {
            "tariffs": "Trade Tariffs & Duties",
            "trade_agreements": "Trade Agreements",
            "g20": "G20 Meetings & Summits",
            "policy_changes": "Government Policy Changes",
            "monetary_policy": "Central Bank Policies",
            "conflicts": "Wars & Conflicts",
            "sanctions": "Economic Sanctions",
            "pandemics": "Pandemics & Health Crises",
            "natural_disasters": "Natural Disasters",
            "elections": "Elections & Political Changes",
            "diplomatic": "Diplomatic Relations",
            "supply_chain": "Supply Chain Disruptions"
        }
        
        # Sector impact mapping
        self.sector_impact = {
            "IT": ["tariffs", "trade_agreements", "policy_changes", "sanctions"],
            "Banking": ["monetary_policy", "policy_changes", "elections", "sanctions"],
            "Oil & Gas": ["conflicts", "sanctions", "tariffs", "natural_disasters"],
            "Pharma": ["pandemics", "trade_agreements", "policy_changes", "tariffs"],
            "Auto": ["tariffs", "supply_chain", "trade_agreements", "policy_changes"],
            "Metals": ["tariffs", "conflicts", "sanctions", "trade_agreements"],
            "FMCG": ["pandemics", "natural_disasters", "supply_chain", "policy_changes"],
            "Infrastructure": ["policy_changes", "elections", "natural_disasters"],
            "Telecom": ["policy_changes", "sanctions", "trade_agreements"],
            "Airlines": ["conflicts", "pandemics", "natural_disasters", "oil_prices"]
        }
        
        # Stock to sector mapping (NSE 50 stocks)
        self.stock_sectors = {
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
            "JSW Steel Ltd.": "Metals",
            "Cipla Ltd.": "Pharma",
            "Dr. Reddy's Laboratories Ltd.": "Pharma",
            "Bajaj Finserv Ltd.": "Banking",
            "Adani Enterprises Ltd.": "Infrastructure",
            "Nestle India Ltd.": "FMCG",
            "Coal India Ltd.": "Metals",
            "Hindalco Industries Ltd.": "Metals",
            "Grasim Industries Ltd.": "Infrastructure",
            "UltraTech Cement Ltd.": "Infrastructure",
            "Adani Ports and Special Economic Zone Ltd.": "Infrastructure",
            "Eicher Motors Ltd.": "Auto",
            "Bajaj Auto Ltd.": "Auto",
            "Tata Consumer Products Ltd.": "FMCG",
            "Apollo Hospitals Enterprise Ltd.": "Pharma",
            "Bharat Electronics Ltd.": "Infrastructure",
            "HDFC Life Insurance Co. Ltd.": "Banking",
            "SBI Life Insurance Company Ltd.": "Banking",
            "InterGlobe Aviation Ltd. (IndiGo)": "Airlines",
            "Shriram Finance Ltd.": "Banking",
            "Trent Ltd.": "FMCG",
            "Zomato Ltd.": "FMCG",
            "Max Healthcare Institute Ltd.": "Pharma",
            "Jio Financial Services Ltd.": "Banking"
        }
        
        # Geopolitical events storage
        self.events_data = []
        self.impact_scores = {}
        
        print("✓ Geopolitical Agent initialized")
    
    def load_geopolitical_events(self, events: List[Dict[str, Any]]):
        """
        Load geopolitical events data
        
        Args:
            events: List of event dicts with keys:
                   - title: Event title
                   - description: Event description
                   - category: Event category
                   - date: Event date
                   - countries_affected: List of countries
                   - sectors_affected: List of sectors
                   - impact_level: high/medium/low
                   - source: News source
        """
        self.events_data = events
        
        texts = []
        metadatas = []
        
        for event in events:
            text = f"{event.get('title', '')} - {event.get('description', '')} " \
                   f"Category: {event.get('category', 'unknown')} " \
                   f"Impact: {event.get('impact_level', 'medium')}"
            
            texts.append(text)
            metadatas.append({
                "category": event.get('category', 'unknown'),
                "date": str(event.get('date', '')),
                "impact_level": event.get('impact_level', 'medium'),
                "countries": ','.join(event.get('countries_affected', [])),
                "sectors": ','.join(event.get('sectors_affected', []))
            })
        
        if texts:
            self.add_documents(texts, metadatas)
            print(f"✓ Loaded {len(events)} geopolitical events")
    
    def analyze(self, stock_name: str = None, timeframe: str = "30d") -> Dict[str, Any]:
        """
        Analyze geopolitical factors affecting a stock or the overall market
        
        Args:
            stock_name: Optional stock name for specific analysis
            timeframe: Analysis timeframe (7d, 30d, 90d)
            
        Returns:
            Dict containing geopolitical analysis and impact assessment
        """
        print(f"\n🌍 Analyzing geopolitical factors...")
        
        # Determine sector if stock provided
        sector = None
        if stock_name:
            sector = self.stock_sectors.get(stock_name, "General")
            print(f"   Stock: {stock_name}, Sector: {sector}")
        
        # Get relevant events
        query = f"geopolitical events {sector if sector else 'India market'} impact"
        relevant_events = self.retrieve_context(query, k=10)
        
        # Analyze events
        event_analysis = self._analyze_events(relevant_events, sector)
        
        # Calculate risk scores
        risk_assessment = self._calculate_risk_scores(event_analysis, sector)
        
        # Generate AI insights
        ai_insight = self._generate_geopolitical_insights(stock_name, sector, event_analysis, risk_assessment)
        
        # Get sector-specific factors
        sector_factors = self._get_sector_factors(sector) if sector else self._get_market_factors()
        
        return {
            "stock": stock_name,
            "sector": sector,
            "analysis_date": datetime.now().strftime("%Y-%m-%d"),
            "timeframe": timeframe,
            "event_summary": event_analysis,
            "risk_assessment": risk_assessment,
            "sector_factors": sector_factors,
            "ai_insight": ai_insight,
            "recommendation": self._get_geopolitical_recommendation(risk_assessment)
        }
    
    def _analyze_events(self, events: List[Dict], sector: str = None) -> Dict[str, Any]:
        """Analyze retrieved events and categorize them"""
        categories = {cat: [] for cat in self.event_categories.keys()}
        
        impact_counts = {"high": 0, "medium": 0, "low": 0}
        
        for event in events:
            content = event.get('content', '')
            metadata = event.get('metadata', {})
            
            category = metadata.get('category', 'policy_changes')
            impact = metadata.get('impact_level', 'medium')
            
            if category in categories:
                categories[category].append({
                    "content": content[:200],
                    "date": metadata.get('date', 'Unknown'),
                    "impact": impact
                })
            
            impact_counts[impact] = impact_counts.get(impact, 0) + 1
        
        # Filter to relevant categories if sector provided
        relevant_categories = {}
        if sector and sector in self.sector_impact:
            relevant_cats = self.sector_impact[sector]
            relevant_categories = {cat: categories[cat] for cat in relevant_cats if categories[cat]}
        else:
            relevant_categories = {cat: events for cat, events in categories.items() if events}
        
        return {
            "total_events": len(events),
            "impact_distribution": impact_counts,
            "categories": relevant_categories,
            "top_concerns": self._identify_top_concerns(relevant_categories)
        }
    
    def _identify_top_concerns(self, categories: Dict) -> List[Dict]:
        """Identify top geopolitical concerns"""
        concerns = []
        
        for category, events in categories.items():
            if events:
                high_impact = sum(1 for e in events if e.get('impact') == 'high')
                concerns.append({
                    "category": self.event_categories.get(category, category),
                    "event_count": len(events),
                    "high_impact_count": high_impact,
                    "severity": "High" if high_impact > 0 else "Medium" if len(events) > 2 else "Low"
                })
        
        # Sort by severity and count
        concerns.sort(key=lambda x: (x['high_impact_count'], x['event_count']), reverse=True)
        return concerns[:5]
    
    def _calculate_risk_scores(self, event_analysis: Dict, sector: str = None) -> Dict[str, Any]:
        """Calculate geopolitical risk scores"""
        
        # Base risk score
        total_events = event_analysis.get('total_events', 0)
        impact_dist = event_analysis.get('impact_distribution', {})
        
        # Weighted score based on impact levels
        risk_score = (
            impact_dist.get('high', 0) * 30 +
            impact_dist.get('medium', 0) * 15 +
            impact_dist.get('low', 0) * 5
        )
        
        # Normalize to 0-100
        risk_score = min(risk_score, 100)
        
        # Category-specific risks
        category_risks = {}
        categories = event_analysis.get('categories', {})
        
        for category, events in categories.items():
            if events:
                cat_score = len(events) * 10 + sum(10 for e in events if e.get('impact') == 'high')
                category_risks[category] = min(cat_score, 100)
        
        # Determine risk level
        if risk_score >= 70:
            risk_level = "High"
            outlook = "Negative"
        elif risk_score >= 40:
            risk_level = "Moderate"
            outlook = "Cautious"
        else:
            risk_level = "Low"
            outlook = "Positive"
        
        return {
            "overall_risk_score": float(risk_score),
            "risk_level": risk_level,
            "market_outlook": outlook,
            "category_risks": category_risks,
            "key_risk_factors": self._identify_key_risks(categories, sector)
        }
    
    def _identify_key_risks(self, categories: Dict, sector: str = None) -> List[str]:
        """Identify key risk factors"""
        risks = []
        
        if 'conflicts' in categories and categories['conflicts']:
            risks.append("Ongoing geopolitical conflicts may cause market volatility")
        
        if 'tariffs' in categories and categories['tariffs']:
            risks.append("Trade tariff changes affecting export-oriented sectors")
        
        if 'sanctions' in categories and categories['sanctions']:
            risks.append("Economic sanctions impacting international trade")
        
        if 'pandemics' in categories and categories['pandemics']:
            risks.append("Health crisis concerns affecting market sentiment")
        
        if 'natural_disasters' in categories and categories['natural_disasters']:
            risks.append("Natural disasters disrupting supply chains")
        
        if 'policy_changes' in categories and categories['policy_changes']:
            risks.append("Government policy changes creating regulatory uncertainty")
        
        if 'monetary_policy' in categories and categories['monetary_policy']:
            risks.append("Central bank policy shifts affecting liquidity")
        
        if sector:
            sector_specific = self._get_sector_specific_risks(sector)
            risks.extend(sector_specific)
        
        return risks[:5] if risks else ["No significant geopolitical risks identified"]
    
    def _get_sector_specific_risks(self, sector: str) -> List[str]:
        """Get sector-specific risk factors"""
        sector_risks = {
            "IT": [
                "US immigration policy changes affecting H1B visas",
                "Data localization requirements in major markets"
            ],
            "Banking": [
                "Changes in foreign investment limits",
                "Cross-border payment regulations"
            ],
            "Oil & Gas": [
                "OPEC+ production decisions",
                "Middle East tensions affecting oil prices"
            ],
            "Pharma": [
                "Drug pricing regulations in export markets",
                "API supply chain dependencies on China"
            ],
            "Auto": [
                "EV policy changes and incentives",
                "Semiconductor supply chain disruptions"
            ],
            "Metals": [
                "Anti-dumping duties and trade barriers",
                "China's steel production policies"
            ],
            "FMCG": [
                "Commodity price volatility",
                "Agricultural policy changes"
            ],
            "Infrastructure": [
                "Government capex and infrastructure spending",
                "Environmental clearance regulations"
            ],
            "Airlines": [
                "Fuel price volatility",
                "International travel restrictions"
            ]
        }
        
        return sector_risks.get(sector, [])
    
    def _get_sector_factors(self, sector: str) -> Dict[str, Any]:
        """Get sector-specific geopolitical factors"""
        relevant_categories = self.sector_impact.get(sector, [])
        
        factors = {
            "sector": sector,
            "key_sensitivities": [
                self.event_categories.get(cat, cat) for cat in relevant_categories
            ],
            "monitoring_areas": self._get_monitoring_areas(sector),
            "historical_impact": self._get_historical_impact(sector)
        }
        
        return factors
    
    def _get_market_factors(self) -> Dict[str, Any]:
        """Get general market geopolitical factors"""
        return {
            "sector": "Overall Market",
            "key_sensitivities": [
                "Global trade tensions",
                "Monetary policy divergence",
                "Commodity price volatility",
                "Geopolitical conflicts"
            ],
            "monitoring_areas": [
                "US-China trade relations",
                "Fed interest rate policy",
                "Crude oil prices",
                "Rupee-Dollar exchange rate"
            ],
            "historical_impact": {
                "2008 Financial Crisis": "50%+ market correction",
                "2020 COVID Pandemic": "38% correction, rapid recovery",
                "2022 Russia-Ukraine": "Oil spike, inflation surge"
            }
        }
    
    def _get_monitoring_areas(self, sector: str) -> List[str]:
        """Get key areas to monitor for a sector"""
        monitoring = {
            "IT": ["US tech policy", "Currency movements", "Global IT spending"],
            "Banking": ["RBI policies", "NPA regulations", "Credit growth"],
            "Oil & Gas": ["OPEC decisions", "US sanctions", "Demand outlook"],
            "Pharma": ["USFDA approvals", "Drug pricing", "API regulations"],
            "Auto": ["EV policies", "Chip supply", "Demand recovery"],
            "Metals": ["China demand", "Trade duties", "Green transition"],
            "FMCG": ["Rural demand", "Input costs", "GST changes"],
            "Infrastructure": ["Government spending", "Interest rates", "Project awards"],
            "Airlines": ["ATF prices", "Travel recovery", "Competition"]
        }
        
        return monitoring.get(sector, ["General economic indicators"])
    
    def _get_historical_impact(self, sector: str) -> Dict[str, str]:
        """Get historical geopolitical impact on sector"""
        impacts = {
            "IT": {
                "2008 Crisis": "Revenue growth slowdown",
                "COVID-2020": "Work-from-home demand surge",
                "US Recession Fears": "Deal deferrals"
            },
            "Banking": {
                "Demonetization 2016": "Deposit surge, loan growth hit",
                "IL&FS Crisis 2018": "NBFC liquidity crunch",
                "COVID-2020": "NPA concerns, moratorium"
            },
            "Oil & Gas": {
                "2014 Oil Crash": "Margin pressure",
                "2022 Russia-Ukraine": "Inventory gains",
                "OPEC Cuts": "Price volatility"
            }
        }
        
        return impacts.get(sector, {"General": "Varies by event"})
    
    def _generate_geopolitical_insights(self, stock_name: str, sector: str, 
                                        event_analysis: Dict, risk_assessment: Dict) -> str:
        """Generate AI-powered geopolitical insights"""
        
        context_parts = []
        
        if stock_name:
            context_parts.append(f"Stock: {stock_name}")
        if sector:
            context_parts.append(f"Sector: {sector}")
        
        context_parts.append(f"Risk Score: {risk_assessment.get('overall_risk_score', 0):.0f}/100")
        context_parts.append(f"Risk Level: {risk_assessment.get('risk_level', 'Unknown')}")
        context_parts.append(f"Market Outlook: {risk_assessment.get('market_outlook', 'Unknown')}")
        
        top_concerns = event_analysis.get('top_concerns', [])
        if top_concerns:
            context_parts.append("\nTop Concerns:")
            for concern in top_concerns[:3]:
                context_parts.append(f"- {concern['category']}: {concern['severity']} severity")
        
        key_risks = risk_assessment.get('key_risk_factors', [])
        if key_risks:
            context_parts.append("\nKey Risks:")
            for risk in key_risks[:3]:
                context_parts.append(f"- {risk}")
        
        context = "\n".join(context_parts)
        
        prompt = f"""You are a geopolitical analyst focusing on Indian markets. Analyze the following:

{context}

Provide analysis including:
1. Current geopolitical climate assessment
2. Impact on {"the stock/sector" if stock_name else "Indian markets"}
3. Key events to watch
4. Risk mitigation suggestions for investors

Keep response under 200 words and be specific to India/NSE context."""

        return self.generate_response(prompt)
    
    def _get_geopolitical_recommendation(self, risk_assessment: Dict) -> Dict[str, Any]:
        """Generate recommendation based on geopolitical analysis"""
        risk_score = risk_assessment.get('overall_risk_score', 50)
        risk_level = risk_assessment.get('risk_level', 'Moderate')
        
        if risk_score >= 70:
            action = "Reduce Exposure"
            strategy = "Defensive positioning, increase cash allocation"
            confidence = 0.7
        elif risk_score >= 50:
            action = "Cautious"
            strategy = "Maintain positions, avoid aggressive buying"
            confidence = 0.6
        elif risk_score >= 30:
            action = "Neutral"
            strategy = "Continue normal investment approach"
            confidence = 0.5
        else:
            action = "Favorable"
            strategy = "Supportive environment for equity investments"
            confidence = 0.7
        
        return {
            "action": action,
            "strategy": strategy,
            "confidence": confidence,
            "risk_level": risk_level,
            "portfolio_suggestion": self._get_portfolio_suggestion(risk_score)
        }
    
    def _get_portfolio_suggestion(self, risk_score: float) -> str:
        """Get portfolio allocation suggestion based on risk"""
        if risk_score >= 70:
            return "Consider 40% equity, 40% debt, 20% gold/cash"
        elif risk_score >= 50:
            return "Consider 50% equity, 35% debt, 15% alternatives"
        elif risk_score >= 30:
            return "Consider 60% equity, 30% debt, 10% alternatives"
        else:
            return "Consider 70% equity, 25% debt, 5% alternatives"
    
    def get_event_summary(self, category: str = None) -> Dict[str, Any]:
        """Get summary of geopolitical events by category"""
        if not self.events_data:
            return {"error": "No events data loaded"}
        
        events = self.events_data
        if category:
            events = [e for e in events if e.get('category') == category]
        
        return {
            "total_events": len(events),
            "category": category or "All",
            "recent_events": events[:5] if events else [],
            "categories_covered": list(set(e.get('category', 'unknown') for e in self.events_data))
        }
    
    def track_specific_event(self, event_type: str) -> Dict[str, Any]:
        """Track specific type of geopolitical event"""
        query = f"{event_type} impact India market NSE"
        relevant_docs = self.retrieve_context(query, k=5)
        
        return {
            "event_type": event_type,
            "related_events": relevant_docs,
            "analysis": self._analyze_specific_event(event_type, relevant_docs)
        }
    
    def _analyze_specific_event(self, event_type: str, docs: List[Dict]) -> str:
        """Analyze impact of specific event type"""
        if not docs:
            return f"No recent {event_type} events found in database"
        
        context = "\n".join([d.get('content', '')[:200] for d in docs[:3]])
        
        prompt = f"""Analyze the following {event_type} events and their potential impact on Indian markets:

{context}

Provide a brief assessment of market impact and key stocks affected. Keep under 100 words."""

        return self.generate_response(prompt)