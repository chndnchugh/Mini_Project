from agents.base_agent import BaseAgent
from typing import Dict, List, Any, Optional
import pandas as pd
import numpy as np
from datetime import datetime, timedelta

class ValuationAgent(BaseAgent):
    """
    Valuation Analysis Agent
    Analyzes trading data and provides suggestions based on various technical metrics
    including RSI, MACD, Bollinger Bands, Moving Averages, and fundamental valuation ratios
    """
    
    def __init__(self, model_name: str = "llama3.2"):
        super().__init__("Valuation Agent", model_name)
        
        # Valuation metrics
        self.metrics = {
            'pe_ratio': 'Price to Earnings (P/E)',
            'pb_ratio': 'Price to Book (P/B)',
            'ps_ratio': 'Price to Sales (P/S)',
            'peg_ratio': 'PEG Ratio',
            'ev_ebitda': 'EV/EBITDA',
            'dividend_yield': 'Dividend Yield (%)',
            'market_cap': 'Market Cap (Cr)',
            'current_price': 'Current Price (₹)',
            'roe': 'Return on Equity (%)',
            'roce': 'Return on Capital Employed (%)',
            'debt_to_equity': 'Debt to Equity Ratio',
            'current_ratio': 'Current Ratio',
            'eps': 'Earnings Per Share (₹)',
            'book_value': 'Book Value Per Share (₹)'
        }
        
        # Technical indicators
        self.technical_indicators = {
            'rsi': 'Relative Strength Index',
            'macd': 'MACD',
            'macd_signal': 'MACD Signal Line',
            'macd_histogram': 'MACD Histogram',
            'sma_20': '20-Day SMA',
            'sma_50': '50-Day SMA',
            'sma_200': '200-Day SMA',
            'ema_12': '12-Day EMA',
            'ema_26': '26-Day EMA',
            'bollinger_upper': 'Bollinger Upper Band',
            'bollinger_lower': 'Bollinger Lower Band',
            'bollinger_middle': 'Bollinger Middle Band',
            'atr': 'Average True Range',
            'obv': 'On-Balance Volume',
            'vwap': 'Volume Weighted Average Price'
        }
        
        self.valuation_data = {}
        self.price_data = {}
        
        # Industry average benchmarks for NSE stocks
        self.industry_averages = {
            'pe_ratio': 22.0,
            'pb_ratio': 3.5,
            'ps_ratio': 2.8,
            'ev_ebitda': 15.0,
            'peg_ratio': 1.5,
            'dividend_yield': 1.5,
            'roe': 15.0,
            'roce': 18.0,
            'debt_to_equity': 0.8,
            'current_ratio': 1.5
        }
        
        print("✓ Valuation Agent initialized with technical analysis capabilities")
    
    def load_valuation_data(self, data: Dict[str, pd.DataFrame], 
                           industry_averages: Dict[str, float] = None):
        """
        Load valuation data for companies
        
        Args:
            data: Dict with company names as keys and DataFrames as values
                  Each DataFrame should have columns: 'date', 'metric', 'value'
            industry_averages: Optional dict of industry average values
        """
        self.valuation_data = data
        
        if industry_averages:
            self.industry_averages.update(industry_averages)
        
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
    
    def load_price_data(self, data: Dict[str, pd.DataFrame]):
        """
        Load historical price data for technical analysis
        
        Args:
            data: Dict with company names as keys and DataFrames as values
                  Each DataFrame should have columns: 'date', 'open', 'high', 'low', 'close', 'volume'
        """
        self.price_data = data
        
        texts = []
        metadatas = []
        
        for company, df in data.items():
            if df.empty:
                continue
            
            # Calculate technical indicators
            df = self._calculate_technical_indicators(df)
            self.price_data[company] = df
            
            # Create text summaries for RAG
            latest = df.iloc[-1]
            text = f"{company} Technical Analysis: Price ₹{latest['close']:.2f}, "
            
            if 'rsi' in df.columns:
                text += f"RSI {latest['rsi']:.1f}, "
            if 'macd' in df.columns:
                text += f"MACD {latest['macd']:.2f}"
            
            texts.append(text)
            metadatas.append({
                "company": company,
                "date": str(latest['date']),
                "type": "technical_data"
            })
        
        if texts:
            self.add_documents(texts, metadatas)
            print(f"✓ Loaded price data for {len(data)} companies")
    
    def _calculate_technical_indicators(self, df: pd.DataFrame) -> pd.DataFrame:
        """Calculate all technical indicators"""
        df = df.copy()
        
        # Ensure data is sorted by date
        df = df.sort_values('date').reset_index(drop=True)
        
        close = df['close']
        high = df['high']
        low = df['low']
        volume = df['volume']
        
        # Simple Moving Averages
        df['sma_20'] = close.rolling(window=20).mean()
        df['sma_50'] = close.rolling(window=50).mean()
        df['sma_200'] = close.rolling(window=200).mean()
        
        # Exponential Moving Averages
        df['ema_12'] = close.ewm(span=12, adjust=False).mean()
        df['ema_26'] = close.ewm(span=26, adjust=False).mean()
        
        # MACD
        df['macd'] = df['ema_12'] - df['ema_26']
        df['macd_signal'] = df['macd'].ewm(span=9, adjust=False).mean()
        df['macd_histogram'] = df['macd'] - df['macd_signal']
        
        # RSI
        df['rsi'] = self._calculate_rsi(close, period=14)
        
        # Bollinger Bands
        df['bollinger_middle'] = close.rolling(window=20).mean()
        bb_std = close.rolling(window=20).std()
        df['bollinger_upper'] = df['bollinger_middle'] + (bb_std * 2)
        df['bollinger_lower'] = df['bollinger_middle'] - (bb_std * 2)
        
        # Average True Range (ATR)
        df['atr'] = self._calculate_atr(high, low, close, period=14)
        
        # On-Balance Volume (OBV)
        df['obv'] = self._calculate_obv(close, volume)
        
        # Volume Weighted Average Price (VWAP)
        df['vwap'] = (volume * (high + low + close) / 3).cumsum() / volume.cumsum()
        
        return df
    
    def _calculate_rsi(self, prices: pd.Series, period: int = 14) -> pd.Series:
        """Calculate Relative Strength Index"""
        delta = prices.diff()
        gain = (delta.where(delta > 0, 0)).rolling(window=period).mean()
        loss = (-delta.where(delta < 0, 0)).rolling(window=period).mean()
        
        rs = gain / loss
        rsi = 100 - (100 / (1 + rs))
        return rsi
    
    def _calculate_atr(self, high: pd.Series, low: pd.Series, 
                       close: pd.Series, period: int = 14) -> pd.Series:
        """Calculate Average True Range"""
        tr1 = high - low
        tr2 = abs(high - close.shift())
        tr3 = abs(low - close.shift())
        tr = pd.concat([tr1, tr2, tr3], axis=1).max(axis=1)
        return tr.rolling(window=period).mean()
    
    def _calculate_obv(self, close: pd.Series, volume: pd.Series) -> pd.Series:
        """Calculate On-Balance Volume"""
        obv = [0]
        for i in range(1, len(close)):
            if close.iloc[i] > close.iloc[i-1]:
                obv.append(obv[-1] + volume.iloc[i])
            elif close.iloc[i] < close.iloc[i-1]:
                obv.append(obv[-1] - volume.iloc[i])
            else:
                obv.append(obv[-1])
        return pd.Series(obv, index=close.index)
    
    def analyze(self, stock_name: str, target_period: int = 12) -> Dict[str, Any]:
        """
        Comprehensive valuation and technical analysis
        
        Args:
            stock_name: Name of the stock to analyze
            target_period: Target period in months for price target
            
        Returns:
            Dict containing valuation metrics, technical signals, and recommendations
        """
        print(f"\n💰 Analyzing valuation for {stock_name}...")
        
        result = {
            "stock": stock_name,
            "analysis_date": datetime.now().strftime("%Y-%m-%d"),
            "target_period_months": target_period
        }
        
        # Fundamental Analysis
        fundamental_analysis = self._analyze_fundamentals(stock_name)
        result.update(fundamental_analysis)
        
        # Technical Analysis
        technical_analysis = self._analyze_technicals(stock_name)
        result.update(technical_analysis)
        
        # Generate AI insights
        ai_insight = self._generate_valuation_insights(stock_name, result)
        result["ai_insight"] = ai_insight
        
        # Generate final recommendation
        result["recommendation"] = self._get_final_recommendation(result)
        
        return result
    
    def _analyze_fundamentals(self, stock_name: str) -> Dict[str, Any]:
        """Analyze fundamental valuation metrics"""
        if stock_name not in self.valuation_data:
            return {
                "fundamental_analysis": {
                    "status": "No valuation data available",
                    "valuation_rating": "Unknown"
                }
            }
        
        df = self.valuation_data[stock_name]
        latest_date = df['date'].max()
        latest_data = df[df['date'] == latest_date]
        
        metrics = {}
        for _, row in latest_data.iterrows():
            metrics[row['metric']] = float(row['value'])
        
        current_price = metrics.get('current_price', 0)
        
        # Calculate fair values using different methods
        valuations = {}
        
        if 'pe_ratio' in metrics and metrics['pe_ratio'] > 0:
            pe_fair_value = self._pe_valuation(metrics, current_price)
            valuations['pe_method'] = pe_fair_value
        
        if 'pb_ratio' in metrics and metrics['pb_ratio'] > 0:
            pb_fair_value = self._pb_valuation(metrics, current_price)
            valuations['pb_method'] = pb_fair_value
        
        if 'peg_ratio' in metrics and metrics['peg_ratio'] > 0:
            peg_fair_value = self._peg_valuation(metrics, current_price)
            valuations['peg_method'] = peg_fair_value
        
        if 'ev_ebitda' in metrics and metrics['ev_ebitda'] > 0:
            ev_fair_value = self._ev_ebitda_valuation(metrics, current_price)
            valuations['ev_ebitda_method'] = ev_fair_value
        
        # Calculate consensus fair value
        if valuations:
            fair_value = np.mean(list(valuations.values()))
        else:
            fair_value = current_price
        
        # Calculate upside potential
        if current_price > 0:
            upside_potential = ((fair_value - current_price) / current_price) * 100
        else:
            upside_potential = 0
        
        valuation_rating = self._get_valuation_rating(upside_potential)
        
        return {
            "current_price": float(current_price),
            "fair_value": float(fair_value),
            "target_price": float(fair_value),
            "upside_potential": float(upside_potential),
            "valuation_rating": valuation_rating,
            "valuation_methods": {
                method: {"fair_value": float(value), 
                        "upside": float(((value - current_price) / current_price) * 100) if current_price > 0 else 0}
                for method, value in valuations.items()
            },
            "key_ratios": {
                "pe_ratio": metrics.get('pe_ratio'),
                "pb_ratio": metrics.get('pb_ratio'),
                "peg_ratio": metrics.get('peg_ratio'),
                "ev_ebitda": metrics.get('ev_ebitda'),
                "dividend_yield": metrics.get('dividend_yield'),
                "roe": metrics.get('roe'),
                "roce": metrics.get('roce'),
                "debt_to_equity": metrics.get('debt_to_equity')
            },
            "vs_industry": self._compare_to_industry(metrics)
        }
    
    def _analyze_technicals(self, stock_name: str) -> Dict[str, Any]:
        """Analyze technical indicators"""
        if stock_name not in self.price_data:
            return {
                "technical_analysis": {
                    "status": "No price data available",
                    "technical_rating": "Unknown"
                }
            }
        
        df = self.price_data[stock_name]
        latest = df.iloc[-1]
        
        signals = []
        
        # RSI Analysis
        rsi = latest.get('rsi', 50)
        if rsi < 30:
            signals.append({"indicator": "RSI", "signal": "Oversold", "action": "Buy", "value": rsi})
        elif rsi > 70:
            signals.append({"indicator": "RSI", "signal": "Overbought", "action": "Sell", "value": rsi})
        else:
            signals.append({"indicator": "RSI", "signal": "Neutral", "action": "Hold", "value": rsi})
        
        # MACD Analysis
        macd = latest.get('macd', 0)
        macd_signal = latest.get('macd_signal', 0)
        if macd > macd_signal:
            signals.append({"indicator": "MACD", "signal": "Bullish Crossover", "action": "Buy", "value": macd})
        else:
            signals.append({"indicator": "MACD", "signal": "Bearish Crossover", "action": "Sell", "value": macd})
        
        # Moving Average Analysis
        close = latest['close']
        sma_50 = latest.get('sma_50', close)
        sma_200 = latest.get('sma_200', close)
        
        if close > sma_50 > sma_200:
            signals.append({"indicator": "Moving Averages", "signal": "Uptrend", "action": "Buy", "value": None})
        elif close < sma_50 < sma_200:
            signals.append({"indicator": "Moving Averages", "signal": "Downtrend", "action": "Sell", "value": None})
        else:
            signals.append({"indicator": "Moving Averages", "signal": "Mixed", "action": "Hold", "value": None})
        
        # Bollinger Bands Analysis
        bb_upper = latest.get('bollinger_upper', close * 1.1)
        bb_lower = latest.get('bollinger_lower', close * 0.9)
        
        if close < bb_lower:
            signals.append({"indicator": "Bollinger Bands", "signal": "Below Lower Band", "action": "Buy", "value": close})
        elif close > bb_upper:
            signals.append({"indicator": "Bollinger Bands", "signal": "Above Upper Band", "action": "Sell", "value": close})
        else:
            signals.append({"indicator": "Bollinger Bands", "signal": "Within Bands", "action": "Hold", "value": close})
        
        # Calculate technical score
        buy_signals = sum(1 for s in signals if s['action'] == 'Buy')
        sell_signals = sum(1 for s in signals if s['action'] == 'Sell')
        
        if buy_signals > sell_signals:
            technical_rating = "Bullish"
        elif sell_signals > buy_signals:
            technical_rating = "Bearish"
        else:
            technical_rating = "Neutral"
        
        # Support and Resistance levels
        support_resistance = self._calculate_support_resistance(df)
        
        return {
            "technical_analysis": {
                "signals": signals,
                "technical_rating": technical_rating,
                "buy_signals": buy_signals,
                "sell_signals": sell_signals,
                "indicators": {
                    "rsi": float(rsi) if pd.notna(rsi) else None,
                    "macd": float(macd) if pd.notna(macd) else None,
                    "macd_signal": float(macd_signal) if pd.notna(macd_signal) else None,
                    "sma_20": float(latest.get('sma_20', 0)) if pd.notna(latest.get('sma_20')) else None,
                    "sma_50": float(sma_50) if pd.notna(sma_50) else None,
                    "sma_200": float(sma_200) if pd.notna(sma_200) else None,
                    "bollinger_upper": float(bb_upper) if pd.notna(bb_upper) else None,
                    "bollinger_lower": float(bb_lower) if pd.notna(bb_lower) else None,
                    "atr": float(latest.get('atr', 0)) if pd.notna(latest.get('atr')) else None,
                    "obv": float(latest.get('obv', 0)) if pd.notna(latest.get('obv')) else None
                },
                "support_resistance": support_resistance
            }
        }
    
    def _calculate_support_resistance(self, df: pd.DataFrame) -> Dict[str, float]:
        """Calculate support and resistance levels"""
        recent_data = df.tail(60)  # Last 60 trading days
        
        high = recent_data['high'].max()
        low = recent_data['low'].min()
        close = recent_data['close'].iloc[-1]
        
        # Pivot points calculation
        pivot = (high + low + close) / 3
        r1 = 2 * pivot - low
        r2 = pivot + (high - low)
        s1 = 2 * pivot - high
        s2 = pivot - (high - low)
        
        return {
            "pivot": float(pivot),
            "resistance_1": float(r1),
            "resistance_2": float(r2),
            "support_1": float(s1),
            "support_2": float(s2)
        }
    
    def _pe_valuation(self, metrics: Dict, current_price: float) -> float:
        """P/E ratio based valuation"""
        pe_ratio = metrics.get('pe_ratio', 0)
        industry_pe = self.industry_averages.get('pe_ratio', 20)
        
        if pe_ratio > 0:
            return current_price * (industry_pe / pe_ratio)
        return current_price
    
    def _pb_valuation(self, metrics: Dict, current_price: float) -> float:
        """P/B ratio based valuation"""
        pb_ratio = metrics.get('pb_ratio', 0)
        industry_pb = self.industry_averages.get('pb_ratio', 3.0)
        
        if pb_ratio > 0:
            return current_price * (industry_pb / pb_ratio)
        return current_price
    
    def _peg_valuation(self, metrics: Dict, current_price: float) -> float:
        """PEG ratio based valuation"""
        peg_ratio = metrics.get('peg_ratio', 0)
        
        if peg_ratio > 0:
            return current_price * (1.0 / peg_ratio)
        return current_price
    
    def _ev_ebitda_valuation(self, metrics: Dict, current_price: float) -> float:
        """EV/EBITDA based valuation"""
        ev_ebitda = metrics.get('ev_ebitda', 0)
        industry_ev = self.industry_averages.get('ev_ebitda', 15.0)
        
        if ev_ebitda > 0:
            return current_price * (industry_ev / ev_ebitda)
        return current_price
    
    def _get_valuation_rating(self, upside_potential: float) -> str:
        """Get valuation rating based on upside potential"""
        if upside_potential > 30:
            return "Highly Undervalued"
        elif upside_potential > 15:
            return "Undervalued"
        elif upside_potential > -15:
            return "Fairly Valued"
        elif upside_potential > -30:
            return "Overvalued"
        else:
            return "Highly Overvalued"
    
    def _compare_to_industry(self, metrics: Dict) -> Dict[str, str]:
        """Compare ratios to industry averages"""
        comparisons = {}
        
        for metric, industry_avg in self.industry_averages.items():
            if metric in metrics and metrics[metric] is not None:
                current = metrics[metric]
                
                if metric in ['pe_ratio', 'pb_ratio', 'ps_ratio', 'ev_ebitda', 'peg_ratio', 'debt_to_equity']:
                    # Lower is better
                    if current < industry_avg * 0.8:
                        comparisons[metric] = f"Attractive ({current:.1f} vs {industry_avg:.1f})"
                    elif current > industry_avg * 1.2:
                        comparisons[metric] = f"Premium ({current:.1f} vs {industry_avg:.1f})"
                    else:
                        comparisons[metric] = f"In-line ({current:.1f} vs {industry_avg:.1f})"
                else:
                    # Higher is better (ROE, ROCE, dividend yield, current ratio)
                    if current > industry_avg * 1.2:
                        comparisons[metric] = f"Above Average ({current:.1f} vs {industry_avg:.1f})"
                    elif current < industry_avg * 0.8:
                        comparisons[metric] = f"Below Average ({current:.1f} vs {industry_avg:.1f})"
                    else:
                        comparisons[metric] = f"In-line ({current:.1f} vs {industry_avg:.1f})"
        
        return comparisons
    
    def _generate_valuation_insights(self, stock_name: str, result: Dict) -> str:
        """Generate AI-powered valuation insights"""
        
        # Build context for LLM
        context_parts = [f"Stock: {stock_name}"]
        
        if 'current_price' in result:
            context_parts.append(f"Current Price: ₹{result['current_price']:.2f}")
        if 'fair_value' in result:
            context_parts.append(f"Fair Value: ₹{result['fair_value']:.2f}")
        if 'upside_potential' in result:
            context_parts.append(f"Upside Potential: {result['upside_potential']:.1f}%")
        if 'valuation_rating' in result:
            context_parts.append(f"Valuation Rating: {result['valuation_rating']}")
        
        if 'key_ratios' in result:
            for ratio, value in result['key_ratios'].items():
                if value is not None:
                    context_parts.append(f"{self.metrics.get(ratio, ratio)}: {value:.2f}")
        
        if 'technical_analysis' in result and isinstance(result['technical_analysis'], dict):
            tech = result['technical_analysis']
            if 'technical_rating' in tech:
                context_parts.append(f"Technical Rating: {tech['technical_rating']}")
            if 'indicators' in tech:
                for ind, val in tech['indicators'].items():
                    if val is not None:
                        context_parts.append(f"{self.technical_indicators.get(ind, ind)}: {val:.2f}")
        
        context = "\n".join(context_parts)
        
        prompt = f"""You are a financial analyst specializing in NSE India stocks. Analyze the following valuation and technical data:

{context}

Provide a comprehensive analysis including:
1. Valuation Assessment - Is the stock overvalued, undervalued, or fairly valued?
2. Technical Outlook - What do the technical indicators suggest?
3. Risk Factors - Key risks to consider
4. Investment Thesis - Clear buy/hold/sell recommendation with reasoning

Keep response under 250 words and focus on actionable insights."""

        return self.generate_response(prompt)
    
    def _get_final_recommendation(self, result: Dict) -> Dict[str, Any]:
        """Generate final recommendation combining fundamental and technical analysis"""
        scores = []
        
        # Fundamental score
        if 'upside_potential' in result:
            upside = result['upside_potential']
            if upside > 20:
                scores.append(('fundamental', 'Strong Buy', 2))
            elif upside > 10:
                scores.append(('fundamental', 'Buy', 1))
            elif upside > -10:
                scores.append(('fundamental', 'Hold', 0))
            elif upside > -20:
                scores.append(('fundamental', 'Sell', -1))
            else:
                scores.append(('fundamental', 'Strong Sell', -2))
        
        # Technical score
        if 'technical_analysis' in result and isinstance(result['technical_analysis'], dict):
            tech = result['technical_analysis']
            rating = tech.get('technical_rating', 'Neutral')
            if rating == 'Bullish':
                scores.append(('technical', 'Buy', 1))
            elif rating == 'Bearish':
                scores.append(('technical', 'Sell', -1))
            else:
                scores.append(('technical', 'Hold', 0))
        
        # Calculate combined score
        if scores:
            total_score = sum(s[2] for s in scores) / len(scores)
            
            if total_score >= 1.5:
                action = "Strong Buy"
                confidence = 0.9
            elif total_score >= 0.5:
                action = "Buy"
                confidence = 0.7
            elif total_score >= -0.5:
                action = "Hold"
                confidence = 0.5
            elif total_score >= -1.5:
                action = "Sell"
                confidence = 0.7
            else:
                action = "Strong Sell"
                confidence = 0.9
        else:
            action = "Hold"
            confidence = 0.3
            total_score = 0
        
        return {
            "action": action,
            "confidence": confidence,
            "combined_score": float(total_score),
            "breakdown": [{"source": s[0], "signal": s[1], "score": s[2]} for s in scores]
        }
    
    def get_technical_summary(self, stock_name: str) -> Dict[str, Any]:
        """Get a quick technical summary for a stock"""
        if stock_name not in self.price_data:
            return {"error": f"No price data for {stock_name}"}
        
        df = self.price_data[stock_name]
        latest = df.iloc[-1]
        
        return {
            "stock": stock_name,
            "date": str(latest['date']),
            "close": float(latest['close']),
            "rsi": float(latest.get('rsi', 50)),
            "macd": float(latest.get('macd', 0)),
            "sma_50": float(latest.get('sma_50', 0)),
            "sma_200": float(latest.get('sma_200', 0)),
            "trend": "Bullish" if latest['close'] > latest.get('sma_50', latest['close']) else "Bearish"
        }