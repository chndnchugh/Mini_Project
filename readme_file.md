# AI Stock Analysis - NSE India

An AI-powered stock analysis system using local LLMs, RAG, and sentiment analysis for NSE India stocks.

## 🎯 Project Overview

1. **Sentiment Analysis Agent** - Analyzes news sentiment using FinBERT and provides trading recommendations
2. **Macro Economic Agent** - Analyzes economic indicators and assesses market conditions
3. **Fundamental Agent** - which analyzes financial disclosures and company trends​
4. **Geopolitical Agent** - provides analysis on international events impacting the market
5. **Valuation Agent** -  offers insights derived from historical prices and volumes. ​



​
### Key Features
- ✅ **Fully Local Execution** - No external API dependencies
- ✅ **RAG Implementation** - Uses ChromaDB for vector storage
- ✅ **Local LLM** - Powered by Ollama (Llama 3.2)
- ✅ **Sentiment Analysis** - FinBERT + VADER for financial sentiment
- ✅ **Economic Analysis** - 8 key macro indicators
- ✅ **Web Interface** - Streamlit dashboard
- ✅ **Easy Deployment** - Automated setup script

---



## 🚀 Installation

### Step 1: Install Ollama



**macOS:**
```bash
brew install ollama
```

**Windows:**
Download from [https://ollama.com/download](https://ollama.com/download)

### Step 2: Start Ollama Service

```bash
# Start Ollama server (keep this running in a separate terminal)
ollama serve
```

### Step 3: Pull LLM Model

```bash
# Download Llama 3.2 model (~2GB)
ollama pull llama3.2
```

### Step 4: Clone/Setup Project

```bash
# Create project directory
mkdir stock_ai_agents
cd stock_ai_agents

# Copy all project files here
# (requirements.txt, agents/, scrapers/, utils/, run_agents.py, app.py, setup.sh)
```

### Step 5: Run Setup Script

```bash
# Make setup script executable
chmod +x setup.sh

# Run setup
./setup.sh
```

The setup script will:
- Create virtual environment
- Install all Python dependencies
- Download FinBERT model
- Create directory structure
- Verify Ollama installation

### Step 6: Activate Virtual Environment

```bash
# Linux/macOS
source venv/bin/activate

# Windows
venv\Scripts\activate
```

---

## 🧪 Testing

### Run All Tests

```bash
python run_agents.py
```

This will:
1. Generate sample news data
2. Generate sample economic data
3. Test Sentiment Analysis Agent
4. Test Macro Economic Agent
5. Display test results

Expected output:
```
================================================
📋 TEST SUMMARY
================================================
   Sentiment Agent: ✅ PASS
   Macro Agent: ✅ PASS
================================================
```

### Test Individual Agents

**Test Sentiment Agent Only:**
```python
from agents.sentiment_agent import SentimentAgent
from scrapers.news_scraper import NewsScraper

# Initialize
agent = SentimentAgent()
scraper = NewsScraper()

# Load sample news
news = scraper.scrape_moneycontrol("Reliance", 10)
agent.load_news_data(news)

# Analyze
result = agent.analyze("Reliance", timeframe="30d")
print(result)
```

**Test Macro Agent Only:**
```python
from agents.macro_agent import MacroEconomicAgent
from utils.data_loader import SampleDataLoader

# Initialize
agent = MacroEconomicAgent()

# Load economic data
data = SampleDataLoader.load_all_indicators()
agent.load_economic_data(data)

# Analyze
result = agent.analyze()
print(result)
```

---

## 💻 Usage

### 1. Command Line Interface

**Run Tests:**
```bash
python run_agents.py
```

**Interactive Mode:**
```bash
python run_agents.py interactive
```

Interactive commands:
```
> sentiment Reliance     # Analyze sentiment for Reliance
> macro TCS              # Analyze macro factors for TCS
> macro                  # General market analysis
> stats                  # Show agent statistics
> quit                   # Exit
```

### 2. Web Interface (Streamlit)

```bash
streamlit run app.py
```

The web interface provides:
- 📊 **Home Dashboard** - System overview and statistics
- 😊 **Sentiment Analysis** - Stock sentiment with recommendations
- 📈 **Macro Analysis** - Economic indicators and trends

Access at: `http://localhost:8501`

### 3. Python API

```python
from agents.sentiment_agent import SentimentAgent
from agents.macro_agent import MacroEconomicAgent

# Initialize agents
sentiment_agent = SentimentAgent()
macro_agent = MacroEconomicAgent()

# Load your data
sentiment_agent.load_news_data(news_data)
macro_agent.load_economic_data(economic_data)

# Get analysis
sentiment_result = sentiment_agent.analyze("TCS", timeframe="30d")
macro_result = macro_agent.analyze(stock_name="TCS")

# Access results
print(f"Recommendation: {sentiment_result['recommendation']}")
print(f"Economic Health: {macro_result['economic_health_score']}")
```

---

## 📊 Data Sources

### For Production Use

**News Data:**
- MoneyControl: `https://www.moneycontrol.com/`
- Economic Times: `https://economictimes.indiatimes.com/`
- NSE India: `https://www.nseindia.com/`

**Economic Data:**
- RBI (Reserve Bank of India): `https://www.rbi.org.in/`
- Ministry of Statistics: `https://www.mospi.gov.in/`
- Trading Economics: `https://tradingeconomics.com/india/indicators`

### Sample Data (Included)

The project includes sample data generators for testing:
- News articles for major stocks
- Economic indicators (GDP, inflation, repo rate, etc.)

---

## 🏗️ Architecture

```
┌─────────────────┐
│   User Query    │
└────────┬────────┘
         │
    ┌────▼─────┐
    │ Ollama   │ ◄─── Local LLM (Llama 3.2)
    │ Server   │
    └────┬─────┘
         │
    ┌────▼──────────┐
    │  LangChain    │ ◄─── Orchestration Layer
    └────┬──────────┘
         │
    ┌────▼──────────┐
    │  Agent Layer  │
    │  - Sentiment  │
    │  - Macro      │
    └────┬──────────┘
         │
    ┌────▼──────────┐
    │  ChromaDB     │ ◄─── Vector Store (RAG)
    │  + Embeddings │
    └────┬──────────┘
         │
    ┌────▼─────────────────┐
    │  Data Sources        │
    │  - News Scrapers     │
    │  - Economic Data     │
    │  - Historical Data   │
    └──────────────────────┘
```

---

## 📁 Project Structure

```
stock_ai_agents/
├── requirements.txt          # Python dependencies
├── setup.sh                  # Setup script
├── run_agents.py            # Main execution script
├── app.py                   # Streamlit web app
├── README.md                # This file
│
├── agents/                  # Agent implementations
│   ├── __init__.py
│   ├── base_agent.py       # Base agent class
│   ├── sentiment_agent.py  # Sentiment analysis
│   └── macro_agent.py      # Macro economic analysis
│
├── scrapers/               # Data collection
│   ├── __init__.py
│   ├── news_scraper.py     # News scraping
│   └── rbi_scraper.py      # Economic data
│
├── utils/                  # Utilities
│   ├── __init__.py
│   ├── data_loader.py      # Sample data generation
│   └── vector_store.py     # Vector DB helpers
│
├── data/                   # Data storage
│   ├── news/              # News articles
│   ├── economic_data/     # Economic indicators
│   └── sample_data/       # Test data
│
├── chroma_db/             # Vector database
│   ├── sentiment_agent/
│   └── macro_agent/
│
└── tests/                 # Test files
    ├── test_sentiment.py
    └── test_macro.py
```

---

## 🔧 Configuration

### Environment Variables (Optional)

Create `.env` file:
```bash
# Ollama Configuration
OLLAMA_HOST=http://localhost:11434
OLLAMA_MODEL=llama3.2

# Agent Configuration
SENTIMENT_MODEL=llama3.2
MACRO_MODEL=llama3.2

# Data Paths
DATA_DIR=./data
CHROMA_DIR=./chroma_db
```

### Customizing Agents

**Change LLM Model:**
```python
# In agents/base_agent.py or when initializing
agent = SentimentAgent(model_name="llama3.2")  # or "mistral", "phi3"
```

**Adjust Temperature:**
```python
# In agents/base_agent.py
self.llm = Ollama(model=model_name, temperature=0.3)  # 0.0-1.0
```

---

## 📈 Performance

### Speed Benchmarks
- **Sentiment Analysis**: ~10-15 seconds per stock
- **Macro Analysis**: ~8-12 seconds
- **First Run**: Slower due to model loading (~30 seconds)
- **Subsequent Runs**: Faster due to caching

### Resource Usage
- **RAM**: 4-6GB (with Llama 3.2)
- **CPU**: 50-80% during inference
- **Storage**: ~3GB (models + data + embeddings)

---

## 🐛 Troubleshooting

### Problem: Ollama not starting
```bash
# Check if Ollama is installed
ollama --version

# Start Ollama manually
ollama serve

# Check if running
curl http://localhost:11434/api/tags
```

### Problem: Model not found
```bash
# List installed models
ollama list

# Pull the model
ollama pull llama3.2
```

### Problem: ChromaDB errors
```bash
# Remove existing database
rm -rf chroma_db/

# Restart the application
python run_agents.py
```

### Problem: FinBERT not downloading
```bash
# Manual download
python3 -c "from transformers import AutoTokenizer, AutoModelForSequenceClassification; \
            AutoTokenizer.from_pretrained('ProsusAI/finbert'); \
            AutoModelForSequenceClassification.from_pretrained('ProsusAI/finbert')"
```

### Problem: ImportError
```bash
# Reinstall dependencies
pip install -r requirements.txt --force-reinstall
```

---

## 🚀 Deployment

### Local Development
```bash
# Already covered in Installation section
streamlit run app.py
```

### Docker Deployment (Coming Soon)
```bash
# Build image
docker build -t stock-ai-agents .

# Run container
docker run -p 8501:8501 stock-ai-agents
```

### Cloud Deployment Options

**AWS EC2:**
- Instance: t3.large (2 vCPU, 8GB RAM)
- Setup Ollama on EC2
- Run Streamlit with nginx reverse proxy

**Google Cloud:**
- Compute Engine: n1-standard-2
- Similar setup as AWS

**Azure:**
- VM: Standard_D2s_v3
- Follow Linux setup instructions

---

## 📚 API Reference

### SentimentAgent

```python
agent.analyze(
    stock_name: str,        # Stock name (e.g., "Reliance")
    timeframe: str = "7d",  # "7d", "30d", "90d"
    use_finbert: bool = True # Use FinBERT or VADER
) -> Dict[str, Any]
```

**Returns:**
```python
{
    "stock": "Reliance",
    "outlook": "Bullish",
    "recommendation": "Buy",
    "confidence": 0.75,
    "sentiment_scores": {
        "positive": 0.68,
        "negative": 0.12,
        "neutral": 0.20,
        "compound": 0.56
    },
    "llm_insight": "...",
    "sample_news": [...]
}
```

### MacroEconomicAgent

```python
agent.analyze(
    stock_name: str = None,  # Optional stock name
    timeframe: str = "current"
) -> Dict[str, Any]
```

**Returns:**
```python
{
    "economic_health_score": 72.5,
    "outlook": "Positive",
    "market_impact": "Bullish",
    "indicators": {...},
    "trends": {...},
    "key_factors": [...],
    "llm_insight": "..."
}
```

---

## 🤝 Contributing

This is an academic project. For improvements:
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
2. Review Ollama documentation: https://ollama.com/docs
3. Check LangChain docs: https://python.langchain.com/

---

## 🔄 Updates

**Version 1.0** (Current)
- ✅ Sentiment Analysis Agent
- ✅ Macro Economic Agent
- ✅ Streamlit Web Interface
- ✅ Sample Data Generators

**Planned Features:**
- [ ] Real-time news scraping
- [ ] Historical backtesting
- [ ] More economic indicators
- [ ] PDF report generation
- [ ] WhatsApp/Telegram alerts