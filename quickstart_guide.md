# ⚡ Quick Start Guide - 15 Minutes Setup

Get your AI Stock Analysis Agents running in 15 minutes!

---

## 📦 Prerequisites Check

Before starting, ensure you have:
- [ ] Python 3.8+ installed: `python3 --version`
- [ ] At least 8GB RAM free
- [ ] 5GB disk space available
- [ ] Internet connection (for initial downloads)

---

## 🚀 5-Step Setup

### Step 1: Install Ollama (2 minutes)

**Linux/macOS:**
```bash
curl -fsSL https://ollama.com/install.sh | sh
```

**Windows:**
Download and install from: https://ollama.com/download

**Verify installation:**
```bash
ollama --version
```

---

### Step 2: Start Ollama & Download Model (3 minutes)

**Terminal 1 - Start Ollama Server:**
```bash
ollama serve
```
Keep this terminal open!

**Terminal 2 - Download Model:**
```bash
ollama pull llama3.2
```
This downloads ~2GB. Wait for completion.

---

### Step 3: Setup Project (3 minutes)

```bash
# Clone/create project directory
mkdir stock_ai_agents
cd stock_ai_agents

# Copy all project files into this directory

# Run setup script
chmod +x setup.sh
./setup.sh
```

The script installs all dependencies (~5-7 minutes).

---

### Step 4: Test the Agents (2 minutes)

```bash
# Activate virtual environment
source venv/bin/activate  # Linux/Mac
# or
venv\Scripts\activate     # Windows

# Run tests
python run_agents.py
```

**Expected Output:**
```
📋 TEST SUMMARY
   Sentiment Agent: ✅ PASS
   Macro Agent: ✅ PASS
```

---

### Step 5: Launch Web Interface (1 minute)

```bash
streamlit run app.py
```

**Open browser**: http://localhost:8501

---

## 🎯 Quick Usage Examples

### Example 1: Analyze Sentiment (CLI)

```bash
python run_agents.py interactive
```

```
> sentiment Reliance
📈 Reliance - Bullish
   Recommendation: Buy
   Compound Score: 0.562
```

### Example 2: Check Macro Indicators

```
> macro TCS
📊 Economic Analysis
   Stock: TCS
   Health Score: 72/100
   Outlook: Positive
```

### Example 3: Using Web Interface

1. Open http://localhost:8501
2. Go to "Sentiment Analysis"
3. Select stock: "Reliance"
4. Click "Analyze"
5. View results with charts!

---

## 🧪 Verify Everything Works

### Test Checklist

- [ ] Ollama is running: `curl http://localhost:11434/api/tags`
- [ ] Model downloaded: `ollama list` shows `llama3.2`
- [ ] Python packages installed: `pip list | grep langchain`
- [ ] Tests pass: `python run_agents.py` shows ✅
- [ ] Web app works: Can access http://localhost:8501

---

## 🐛 Common Issues & Fixes

### Issue 1: "Ollama connection refused"
```bash
# Solution: Start Ollama server
ollama serve
```

### Issue 2: "Model not found"
```bash
# Solution: Pull the model
ollama pull llama3.2
```

### Issue 3: "Module not found"
```bash
# Solution: Activate venv and reinstall
source venv/bin/activate
pip install -r requirements.txt
```

### Issue 4: "FinBERT download stuck"
```bash
# Solution: It's downloading ~500MB, just wait
# Or check internet connection
```

### Issue 5: "Port 8501 already in use"
```bash
# Solution: Use different port
streamlit run app.py --server.port 8502
```

---

## 📊 Testing with Different Stocks

### Available Stocks in Sample Data

✅ Pre-configured stocks:
- Reliance Industries
- TCS (Tata Consultancy Services)
- Infosys
- HDFC Bank
- ICICI Bank

### Add Your Own Stock

```python
from scrapers.news_scraper import NewsScraper

scraper = NewsScraper()
news = scraper.scrape_moneycontrol("Wipro", max_articles=10)
# Load into agent...
```

---

## 🎓 Understanding the Output

### Sentiment Analysis Output

```python
{
    "outlook": "Bullish",     # Bearish/Neutral/Bullish
    "recommendation": "Buy",  # Buy/Hold/Sell
    "confidence": 0.75,       # 0.0 to 1.0
    "sentiment_scores": {
        "compound": 0.56      # -1 (negative) to +1 (positive)
    }
}
```

**Interpretation:**
- Compound > 0.3: Positive sentiment → Consider Buy
- Compound < -0.3: Negative sentiment → Consider Sell
- -0.3 to 0.3: Neutral → Hold

### Macro Economic Output

```python
{
    "economic_health_score": 72,  # 0-100
    "outlook": "Positive",         # Positive/Negative/Neutral
    "market_impact": "Bullish"     # Bullish/Bearish/Mixed
}
```

**Interpretation:**
- Score > 70: Strong economy → Bullish for stocks
- Score < 40: Weak economy → Bearish for stocks
- 40-70: Mixed signals → Neutral

---

## 🔄 Daily Usage Workflow

### Morning Routine (5 minutes)

```bash
# 1. Ensure Ollama is running
ollama serve &

# 2. Activate environment
source venv/bin/activate

# 3. Quick check
python run_agents.py interactive
> sentiment Reliance
> macro
> quit
```

### Before Trading (10 minutes)

```bash
# Launch full interface
streamlit run app.py

# Check:
# - Sentiment for your watchlist stocks
# - Current macro indicators
# - AI insights and recommendations
```

---

## 🎯 Next Steps

Now that you're set up:

### 1. Explore Features
- [x] Try different stocks
- [x] Check various timeframes (7d, 30d, 90d)
- [x] Compare macro indicators

### 2. Customize
- [ ] Add real news scrapers (see README)
- [ ] Connect to live economic data APIs
- [ ] Add more stocks to watchlist

### 3. Advanced
- [ ] Create custom agents
- [ ] Add technical analysis
- [ ] Build trading strategies

---

## 📚 Learn More

- **Full Documentation**: See `README.md`
- **API Reference**: See `README.md` - API Reference section
- **Ollama Docs**: https://ollama.com/docs
- **LangChain Guide**: https://python.langchain.com/

---

## 💡 Pro Tips

1. **Keep Ollama Running**: Start `ollama serve` once, keep terminal open
2. **Use Interactive Mode**: Fastest way to test quickly
3. **Check Logs**: If errors occur, scroll up to see detailed messages
4. **RAM Monitor**: If system slows, close other applications
5. **Model Choice**: Llama 3.2 balances speed & accuracy

---

## 🎉 You're Ready!

You now have a working AI stock analysis system!

**Quick Commands:**
```bash
# Test agents
python run_agents.py

# Interactive mode
python run_agents.py interactive

# Web interface
streamlit run app.py
```

**Happy Trading! 📈**

---

## 📞 Get Help

Stuck? Check:
1. ❓ README.md - Troubleshooting section
2. 🔍 Error messages in terminal
3. 📖 Ollama status: `ollama list`

Most issues are fixed by:
- Restarting Ollama: `ollama serve`
- Reinstalling dependencies: `pip install -r requirements.txt`
- Clearing cache: `rm -rf chroma_db/`