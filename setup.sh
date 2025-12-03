#!/bin/bash

echo "=================================================="
echo "  AI Stock Analysis Agents - Setup Script"
echo "=================================================="
echo ""

# Colors
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Check Python version
echo "📌 Checking Python version..."
python_version=$(python3 --version 2>&1 | awk '{print $2}')
echo "   Found Python $python_version"

if [ -z "$python_version" ]; then
    echo -e "${RED}❌ Python 3 is not installed${NC}"
    exit 1
fi

# Create virtual environment
echo ""
echo "📦 Creating virtual environment..."
if [ -d "venv" ]; then
    echo "   Virtual environment already exists"
else
    python3 -m venv venv
    echo -e "${GREEN}✓ Virtual environment created${NC}"
fi

# Activate virtual environment
echo ""
echo "🔄 Activating virtual environment..."
source venv/bin/activate

# Upgrade pip
echo ""
echo "⬆️  Upgrading pip..."
pip install --upgrade pip > /dev/null 2>&1
echo -e "${GREEN}✓ pip upgraded${NC}"

# Install dependencies
echo ""
echo "📥 Installing dependencies (this may take a few minutes)..."
pip install -r requirements.txt

if [ $? -eq 0 ]; then
    echo -e "${GREEN}✓ Dependencies installed successfully${NC}"
else
    echo -e "${RED}❌ Failed to install dependencies${NC}"
    exit 1
fi

# Check if Ollama is installed
echo ""
echo "🤖 Checking Ollama installation..."
if command -v ollama &> /dev/null; then
    echo -e "${GREEN}✓ Ollama is installed${NC}"
    
    # Check if Ollama is running
    if pgrep -x "ollama" > /dev/null; then
        echo -e "${GREEN}✓ Ollama is running${NC}"
    else
        echo -e "${YELLOW}⚠ Ollama is not running${NC}"
        echo "   Please start Ollama: ollama serve"
    fi
    
    # Pull required model
    echo ""
    echo "📥 Pulling Llama 3.2 model..."
    ollama pull llama3.2
    
    if [ $? -eq 0 ]; then
        echo -e "${GREEN}✓ Llama 3.2 model pulled successfully${NC}"
    else
        echo -e "${YELLOW}⚠ Failed to pull model. You can do it manually: ollama pull llama3.2${NC}"
    fi
else
    echo -e "${RED}❌ Ollama is not installed${NC}"
    echo ""
    echo "Please install Ollama:"
    echo "  Linux: curl -fsSL https://ollama.com/install.sh | sh"
    echo "  Mac: brew install ollama"
    echo "  Windows: Download from https://ollama.com/download"
    echo ""
    echo "After installation, run: ollama pull llama3.2"
fi

# Create directory structure
echo ""
echo "📁 Creating directory structure..."
mkdir -p data/news
mkdir -p data/economic_data
mkdir -p data/sample_data
mkdir -p chroma_db
mkdir -p agents
mkdir -p scrapers
mkdir -p utils
mkdir -p tests

# Create __init__.py files
touch agents/__init__.py
touch scrapers/__init__.py
touch utils/__init__.py
touch tests/__init__.py

echo -e "${GREEN}✓ Directory structure created${NC}"

# Download FinBERT model (cached for faster startup)
echo ""
echo "📥 Downloading FinBERT model (one-time download, ~500MB)..."
python3 << EOF
try:
    from transformers import AutoTokenizer, AutoModelForSequenceClassification
    print("   Downloading tokenizer...")
    tokenizer = AutoTokenizer.from_pretrained("ProsusAI/finbert")
    print("   Downloading model...")
    model = AutoModelForSequenceClassification.from_pretrained("ProsusAI/finbert")
    print("✓ FinBERT model downloaded and cached")
except Exception as e:
    print(f"⚠ Could not pre-download FinBERT: {e}")
    print("  It will be downloaded on first use")
EOF

echo ""
echo "=================================================="
echo -e "${GREEN}✅ Setup Complete!${NC}"
echo "=================================================="
echo ""
echo "Next steps:"
echo ""
echo "1. Start Ollama (if not running):"
echo "   $ ollama serve"
echo ""
echo "2. Test the agents:"
echo "   $ python run_agents.py"
echo ""
echo "3. Run interactive mode:"
echo "   $ python run_agents.py interactive"
echo ""
echo "4. Launch web interface:"
echo "   $ streamlit run app.py"
echo ""
echo "=================================================="