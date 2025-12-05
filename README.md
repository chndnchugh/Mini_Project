# AI Stock Analysis - NSE India

An AI-powered stock analysis system using local LLMs, RAG, and multiple specialized agents for NSE India stocks.

## 🎯 Project Overview

This system employs **5 specialized AI agents** to provide comprehensive stock analysis:

### 1. Sentiment Analysis Agent
- Analyzes news sentiment using FinBERT and VADER
- Provides buy/hold/sell recommendations
- Tracks sentiment trends over time

### 2. Macro Economic Agent
- Analyzes 8 key economic indicators (GDP, Inflation, Repo Rate, etc.)
- Assesses market conditions
- Provides economic outlook predictions

### 3. Valuation & Technical Agent ⭐ NEW
- **Technical Indicators:**
  - RSI (Relative Strength Index)
  - MACD (Moving Average Convergence Divergence)
  - Bollinger Bands
  - Moving Averages (SMA 20/50/200, EMA 12/26)
  - ATR (Average True Range)
  - OBV (On-Balance Volume)
  - VWAP (Volume Weighted Average Price)
- **Valuation Metrics:**
  - P/E, P/B, P/S, PEG ratios
  - EV/EBITDA
  - ROE, ROCE
  - Fair value calculation
- Support and resistance levels
- Multi-method valuation (P/E, P/B, PEG, EV/EBITDA)

### 4. Geopolitical Agent ⭐ NEW
- **Tracks:**
  - Trade tariffs and duties
  - G20 summits and meetings
  - Government policy changes
  - Monetary policy (RBI decisions)
  - Wars and conflicts
  - Economic sanctions
  - Pandemics and health crises
  - Natural disasters
  - Elections and political changes
  - Supply chain disruptions
- Sector-specific impact analysis
- Risk scoring (0-100)
- Portfolio allocation suggestions

### 5. Fundamental Analysis Agent ⭐ NEW
- **Analyzes:**
  - Quarterly results
  - Annual reports
  - Income statements
  - Balance sheets
  - Cash flow statements
- **Key Metrics:**
  - Revenue growth, Operating margin, Net margin
  - ROE, ROCE, ROA
  - Current ratio, Quick ratio
  - Debt-to-equity, Interest coverage
  - EPS growth, CAGR calculations
- Earnings quality assessment
- Peer comparison
- Sector benchmarking

---

## 🚀 Key Features

- ✅ **Fully Local Execution** - No external API dependencies
- ✅ **RAG Implementation** - Uses ChromaDB for vector storage
- ✅ **Local LLM** - Powered by Ollama (Llama 3.2)
- ✅ **5 Specialized Agents** - Comprehensive analysis
- ✅ **Technical Analysis** - 15+ indicators
- ✅ **Fundamental Analysis** - 30+ financial metrics
- ✅ **Geopolitical Tracking** - 12 event categories
- ✅ **Web Interface** - Streamlit dashboard
- ✅ **Interactive CLI** - Command-line interface
- ✅ **Comprehensive Analysis** - All agents combined

---

## 📁 Project Structure

```
stock_ai_agents/
├── app.py                      # Streamlit web interface
├── run_agents.py               # Main execution script
├── requirements.txt            # Python dependencies
├── setup.sh                    # Setup script
│
├── agents/                     # Agent implementations
│   ├── __init__.py
│   ├── base_agent.py          # Base agent class
│   ├── sentiment_agent.py     # Sentiment analysis
│   ├── macro_agent.py         # Macro economic analysis
│   ├── valuation_agent.py     # Valuation & technical ⭐
│   ├── geopolitical_agent.py  # Geopolitical analysis ⭐
│   └── fundamental_agent.py   # Fundamental analysis ⭐
│
├── scrapers/                   # Data collection
│   ├── __init__.py
│   └── news_scraper.py        # News scraping
│
├── utils/                      # Utilities
│   ├── __init__.py
│   ├── data_loader.py         # Economic data loader
│   └── new_data_loaders.py    # New agent data loaders ⭐
│
├── data/                       # Data storage
│   ├── news/                  # News articles
│   ├── economic_data/         # Economic indicators
│   ├── valuation/             # Valuation data ⭐
│   ├── geopolitical/          # Geopolitical events ⭐
│   └── fundamentals/          # Financial statements ⭐
│
└── chroma_db/                  # Vector database
```

---

## 🔧 Installation

### Step 1: Install Ollama

**Linux:**
```bash
curl -fsSL https://ollama.com/install.sh | sh
```

**macOS:**
```bash
brew install ollama
```

**Windows:**
Download from [https://ollama.com/download](https://ollama.com/download)

### Step 2: Start Ollama & Download Model

```bash
# Start Ollama server
ollama serve

# In another terminal, download the model
ollama pull llama3.2
```

### Step 3: Setup Project

```bash
# Clone/create project directory
cd stock_ai_agents

# Make setup script executable
chmod +x setup.sh

# Run setup
./setup.sh
```

### Step 4: Activate Environment

```bash
source venv/bin/activate  # Linux/Mac
# or
venv\Scripts\activate     # Windows
```

---

## 🧪 Testing

### Run All Agent Tests

```bash
python run_agents.py
```

This will test all 5 agents and display results:
```
📋 TEST SUMMARY
   Sentiment Agent:    ✅ PASS
   Macro Agent:        ✅ PASS
   Valuation Agent:    ✅ PASS
   Geopolitical Agent: ✅ PASS
   Fundamental Agent:  ✅ PASS
```

---

## 💻 Usage

### 1. Interactive Mode (CLI)

```bash
python run_agents.py interactive
```

**Available Commands:**
```
> sentiment Reliance           # Analyze news sentiment
> macro TCS                    # Macro analysis for stock
> valuation "Reliance Industries Ltd."  # Valuation analysis
> geopolitical "HDFC Bank Ltd."         # Geopolitical impact
> fundamental "Infosys Ltd."            # Fundamental analysis
> full "Reliance Industries Ltd."       # All agents combined
> stats                        # Show agent statistics
> help                         # Show help
> quit                         # Exit
```

### 2. Web Interface (Streamlit)

```bash
streamlit run app.py
```

Access at: `http://localhost:8501`

**Features:**
- Home dashboard with quick stats
- Individual agent pages
- Comprehensive analysis combining all agents
- Interactive charts and visualizations

### 3. Python API

```python
from agents.sentiment_agent import SentimentAgent
from agents.macro_agent import MacroEconomicAgent
from agents.valuation_agent import ValuationAgent
from agents.geopolitical_agent import GeopoliticalAgent
from agents.fundamental_agent import FundamentalAgent

# Initialize agents
sentiment = SentimentAgent()
macro = MacroEconomicAgent()
valuation = ValuationAgent()
geopolitical = GeopoliticalAgent()
fundamental = FundamentalAgent()

# Load data into agents
# ... (see examples in code)

# Analyze
sentiment_result = sentiment.analyze("Reliance", timeframe="30d")
macro_result = macro.analyze(stock_name="TCS")
valuation_result = valuation.analyze("Reliance Industries Ltd.")
geo_result = geopolitical.analyze(stock_name="HDFC Bank Ltd.")
fundamental_result = fundamental.analyze("Infosys Ltd.", period="quarterly")
```

---

## 📊 Agent Output Examples

### Valuation Agent Output

```python
{
    "stock": "Reliance Industries Ltd.",
    "current_price": 2450.50,
    "fair_value": 2780.25,
    "upside_potential": 13.5,
    "valuation_rating": "Undervalued",
    "technical_analysis": {
        "technical_rating": "Bullish",
        "signals": [...],
        "indicators": {
            "rsi": 55.2,
            "macd": 12.5,
            "sma_50": 2380.0,
            ...
        }
    },
    "recommendation": {
        "action": "Buy",
        "confidence": 0.75
    }
}
```

### Geopolitical Agent Output

```python
{
    "stock": "HDFC Bank Ltd.",
    "sector": "Banking",
    "risk_assessment": {
        "overall_risk_score": 35,
        "risk_level": "Low",
        "market_outlook": "Positive",
        "key_risk_factors": [...]
    },
    "recommendation": {
        "action": "Favorable",
        "strategy": "Continue normal investment approach"
    }
}
```

### Fundamental Agent Output

```python
{
    "stock": "Infosys Ltd.",
    "fundamental_score": {
        "overall_score": 72,
        "rating": "Good",
        "component_scores": {
            "profitability": 85,
            "growth": 70,
            "leverage": 90,
            "quality": 65,
            "liquidity": 75
        }
    },
    "recommendation": {
        "action": "Buy",
        "confidence": 0.7
    }
}
```

---

## 📈 Supported Stocks (NSE 50)

The system supports all NSE 50 stocks including:
- Reliance Industries Ltd.
- Tata Consultancy Services Ltd. (TCS)
- HDFC Bank Ltd.
- Infosys Ltd.
- ICICI Bank Ltd.
- ... and 45 more

---

## 🔧 Configuration

### Changing LLM Model

```python
# In agent initialization
agent = SentimentAgent(model_name="llama3.2")  # or "mistral", "phi3"
```

### Adjusting Industry Benchmarks

```python
# In ValuationAgent
industry_averages = {
    'pe_ratio': 25.0,
    'pb_ratio': 4.0,
    'roe': 20.0,
    ...
}
agent.load_valuation_data(data, industry_averages=industry_averages)
```

---

## 🐛 Troubleshooting

### Ollama Issues
```bash
# Check if running
curl http://localhost:11434/api/tags

# Restart
ollama serve
```

### Missing Models
```bash
ollama pull llama3.2
```

### ChromaDB Errors
```bash
rm -rf chroma_db/
python run_agents.py
```

---

## 📚 Technical Details

### Technical Indicators Calculated

| Indicator | Description | Usage |
|-----------|-------------|-------|
| RSI | Relative Strength Index (14-period) | Overbought/Oversold |
| MACD | Moving Average Convergence Divergence | Trend direction |
| Bollinger Bands | 20-period with 2 std dev | Volatility |
| SMA 20/50/200 | Simple Moving Averages | Trend identification |
| EMA 12/26 | Exponential Moving Averages | Short-term trends |
| ATR | Average True Range (14-period) | Volatility measurement |
| OBV | On-Balance Volume | Volume confirmation |
| VWAP | Volume Weighted Average Price | Fair price |

### Geopolitical Event Categories

1. Trade Tariffs & Duties
2. Trade Agreements
3. G20 Meetings & Summits
4. Government Policy Changes
5. Monetary Policy (RBI)
6. Wars & Conflicts
7. Economic Sanctions
8. Pandemics & Health Crises
9. Natural Disasters
10. Elections & Political Changes
11. Diplomatic Relations
12. Supply Chain Disruptions

### Fundamental Metrics

**Profitability:** ROE, ROCE, ROA, Net Margin, Operating Margin
**Liquidity:** Current Ratio, Quick Ratio, Cash Ratio
**Leverage:** Debt-to-Equity, Interest Coverage
**Efficiency:** Asset Turnover, Inventory Turnover
**Growth:** Revenue CAGR, Profit CAGR, EPS CAGR

---

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Submit a pull request

---

## 📝 License

MIT License - Free for academic and personal use

---

## 👥 Authors

MTech Applied AI Student Project

---

## 🙏 Acknowledgments

- Anthropic's Claude for guidance
- Ollama team for local LLM infrastructure
- HuggingFace for FinBERT model
- NSE India for market data standards

---

## 📞 Support

For issues or questions:
1. Check Troubleshooting section
2. Review Ollama documentation
3. Check LangChain docs

---

## 🔄 Version History

**Version 2.0** (Current)
- ✅ Valuation & Technical Agent
- ✅ Geopolitical Agent
- ✅ Fundamental Agent
- ✅ Comprehensive Analysis Mode
- ✅ Enhanced Web Interface

**Version 1.0**
- ✅ Sentiment Analysis Agent
- ✅ Macro Economic Agent
- ✅ Basic Web Interface