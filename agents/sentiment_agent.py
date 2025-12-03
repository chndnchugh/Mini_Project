from agents.base_agent import BaseAgent
from transformers import AutoTokenizer, AutoModelForSequenceClassification
import torch
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer
from typing import Dict, List, Any
import numpy as np
from datetime import datetime, timedelta

class SentimentAgent(BaseAgent):
    """Sentiment Analysis Agent using FinBERT and VADER"""
    
    def __init__(self, model_name: str = "llama3.2"):
        super().__init__("Sentiment Agent", model_name)
        
        # Initialize FinBERT
        print("Loading FinBERT model (this may take a moment)...")
        try:
            self.finbert_tokenizer = AutoTokenizer.from_pretrained("ProsusAI/finbert")
            self.finbert_model = AutoModelForSequenceClassification.from_pretrained("ProsusAI/finbert")
            print("✓ FinBERT model loaded")
        except Exception as e:
            print(f"✗ Failed to load FinBERT - {e}")
            print("  Installing transformers: pip install transformers torch")
            self.finbert_model = None
        
        # Initialize VADER (fallback)
        self.vader = SentimentIntensityAnalyzer()
        print("✓ VADER sentiment analyzer loaded")
    
    def analyze_text_sentiment(self, text: str, use_finbert: bool = True) -> Dict[str, float]:
        """Analyze sentiment of a single text"""
        if use_finbert and self.finbert_model:
            return self._finbert_sentiment(text)
        else:
            return self._vader_sentiment(text)
    
    def _finbert_sentiment(self, text: str) -> Dict[str, float]:
        """Analyze using FinBERT. Keys: positive, negative, neutral, compound"""
        try:
            inputs = self.finbert_tokenizer(text, return_tensors="pt", 
                                           truncation=True, max_length=512, 
                                           padding=True)
            
            with torch.no_grad():
                outputs = self.finbert_model(**inputs)
                predictions = torch.nn.functional.softmax(outputs.logits, dim=-1)
            
            scores = predictions[0].tolist()
            # FinBERT labels are often in the order: negative, neutral, positive
            return {
                "negative": scores[0],
                "neutral": scores[1],
                "positive": scores[2],
                "compound": scores[2] - scores[0]  # -1 to 1 scale
            }
        except Exception as e:
            print(f"FinBERT error: {e}, falling back to VADER")
            return self._vader_sentiment(text)
    
    def _vader_sentiment(self, text: str) -> Dict[str, float]:
        """Analyze using VADER. Keys: neg, neu, pos, compound"""
        scores = self.vader.polarity_scores(text)
        
        # VADER returns 'pos', 'neg', 'neu'. We normalize keys to match FinBERT's output 
        # structure for consistent aggregation later.
        return {
            "positive": scores.get('pos', 0.0),
            "negative": scores.get('neg', 0.0),
            "neutral": scores.get('neu', 0.0),
            "compound": scores.get('compound', 0.0) # VADER compound is already -1 to 1
        }
    
    def analyze(self, stock_name: str, timeframe: str = "7d", 
                use_finbert: bool = True) -> Dict[str, Any]:
        """
        Analyze sentiment for a stock
        """
        print(f"\n🔍 Analyzing sentiment for {stock_name} ({timeframe})...")
        
        # Retrieve relevant news from vector store
        query = f"{stock_name} news sentiment analysis"
        docs = self.retrieve_context(query, k=10)
        
        if not docs:
            return {
                "stock": stock_name,
                "timeframe": timeframe,
                "error": "No news data found. Please load news data first.",
                "recommendation": "neutral",
                "confidence": 0.0
            }
        
        # Analyze sentiment for each document
        sentiments = []
        analyzed_docs = []
        
        for doc in docs:
            # The result from analyze_text_sentiment now always uses keys: positive, negative, neutral, compound
            sentiment = self.analyze_text_sentiment(doc["content"], use_finbert)
            sentiments.append(sentiment)
            analyzed_docs.append({
                "text": doc["content"][:200] + "...",
                "sentiment": sentiment,
                "metadata": doc.get("metadata", {})
            })
        
        # Aggregate sentiments (The fix is primarily ensuring the keys are 'positive', 'negative', etc.)
        # This now reliably uses the normalized keys from the VADER/FinBERT helper methods
        avg_positive = np.mean([s["positive"] for s in sentiments])
        avg_negative = np.mean([s["negative"] for s in sentiments])
        avg_neutral = np.mean([s["neutral"] for s in sentiments]) # Use 'neutral' consistently
        avg_compound = np.mean([s["compound"] for s in sentiments])
        
        # Generate LLM-based insights
        context = "\n".join([f"- {doc['content'][:150]}" for doc in docs[:5]])
        
        prompt = f"""You are a financial analyst. Based on the following news about {stock_name}, provide a brief sentiment analysis and outlook.

Recent News Sentiment:
{context}

Average Sentiment Scores:
- Positive: {avg_positive:.2%}
- Negative: {avg_negative:.2%}
- Neutral: {avg_neutral:.2%}
- Compound Score: {avg_compound:.2f} (range: -1 to 1)

Provide:
1. Overall sentiment (Positive/Negative/Neutral)
2. Short-term outlook (1-3 months)
3. Key factors driving sentiment
4. Investment recommendation (Buy/Hold/Sell)

Keep response under 150 words."""

        llm_insight = self.generate_response(prompt)
        
        # Determine recommendation
        if avg_compound > 0.3:
            recommendation = "Buy"
            outlook = "Bullish"
        elif avg_compound < -0.3:
            recommendation = "Sell"
            outlook = "Bearish"
        else:
            recommendation = "Hold"
            outlook = "Neutral"
        
        return {
            "stock": stock_name,
            "timeframe": timeframe,
            "sentiment_scores": {
                "positive": float(avg_positive),
                "negative": float(avg_negative),
                "neutral": float(avg_neutral),
                "compound": float(avg_compound)
            },
            "outlook": outlook,
            "recommendation": recommendation,
            "confidence": float(abs(avg_compound)),
            "total_news_analyzed": len(docs),
            "llm_insight": llm_insight,
            "sample_news": analyzed_docs[:3]
        }
    
    def batch_analyze(self, stocks: List[str], timeframe: str = "7d") -> List[Dict[str, Any]]:
        """Analyze multiple stocks"""
        results = []
        for stock in stocks:
            result = self.analyze(stock, timeframe)
            results.append(result)
        return results
    
    def load_news_data(self, news_data: List[Dict[str, str]]):
        """
        Load news data into vector store
        """
        texts = []
        metadatas = []
        
        for item in news_data:
            text = f"{item.get('title', '')} {item.get('content', '')}"
            texts.append(text)
            metadatas.append({
                "date": item.get('date', ''),
                "source": item.get('source', ''),
                "stock": item.get('stock', ''),
                "title": item.get('title', '')
            })
        
        self.add_documents(texts, metadatas)
        print(f"✓ Loaded {len(news_data)} news articles")