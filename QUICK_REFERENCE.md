# 📋 DocVerify AI - Quick Reference Card

## 🚀 One-Time Setup Commands (Copy & Paste)

### 1. System Setup (Run Once)
```bash
# Update system & install dependencies
sudo apt update && sudo apt install -y git git-lfs build-essential libgl1-mesa-glx libglib2.0-0 tesseract-ocr tesseract-ocr-hin tesseract-ocr-tam tesseract-ocr-tel poppler-utils

# Configure Git
git config --global user.name "YOUR_NAME"
git config --global user.email "YOUR_EMAIL"
git config --global credential.helper store

# Install Poetry
curl -sSL https://install.python-poetry.org | python3 -
echo 'export PATH="$HOME/.local/bin:$PATH"' >> ~/.bashrc && source ~/.bashrc
```

### 2. Clone & Setup Project
```bash
# Clone (replace YOUR_USERNAME)
git clone https://github.com/YOUR_USERNAME/docverify-ai.git
cd docverify-ai

# Create structure
mkdir -p src/{core,database,preprocessing,ocr,classification,extraction,validation,detection,fraud,llm,rag,orchestration,api,mcp} ui/{pages,components} tests scripts docs
find src -type d -exec touch {}/__init__.py \;

# Install dependencies
poetry install
```

### 3. Install Ollama & Models
```bash
# Install Ollama
curl -fsSL https://ollama.com/install.sh | sh
ollama serve &
sleep 5

# Pull models (takes 10-15 min)
ollama pull llama3.1:8b
ollama pull nomic-embed-text
ollama pull llava:7b
```

---

## 🔑 API Keys (Get These First!)

| Service | URL | What to Copy |
|---------|-----|--------------|
| **Gemini** | https://aistudio.google.com/apikey | API Key |
| **Supabase** | https://supabase.com → New Project | URL + anon key + service key |
| **GitHub PAT** | Settings → Developer settings → Tokens | Personal Access Token |

---

## 📁 .env Template
```bash
SUPABASE_URL=https://xxxxx.supabase.co
SUPABASE_KEY=eyJhbGc...
SUPABASE_SERVICE_KEY=eyJhbGc...
GOOGLE_API_KEY=AIzaSy...
OLLAMA_BASE_URL=http://localhost:11434
OLLAMA_MODEL=llama3.1:8b
APP_ENV=development
DEBUG=true
```

---

## 🏃 Daily Commands

### Start Development
```bash
cd ~/docverify-ai
git pull origin main          # Get latest
poetry shell                  # Activate env
ollama serve &                # Start Ollama (if not running)
```

### Run Services
```bash
# Terminal 1: API
uvicorn src.api.main:app --reload --host 0.0.0.0 --port 8000

# Terminal 2: UI
streamlit run ui/app.py --server.port 8501 --server.address 0.0.0.0

# Terminal 3: MCP Server
python -m src.mcp.server --http --port 8001
```

### Save & Push Work
```bash
git add .
git commit -m "feat: your message"
git push origin main
```

---

## 🧪 Test Commands

```bash
# Test imports
python3 -c "from paddleocr import PaddleOCR; print('✅ OCR OK')"

# Test Gemini
python3 -c "
import os; from dotenv import load_dotenv; load_dotenv()
import google.generativeai as genai
genai.configure(api_key=os.getenv('GOOGLE_API_KEY'))
print(genai.GenerativeModel('gemini-2.0-flash-exp').generate_content('Hi').text)
"

# Test Ollama
ollama run llama3.1:8b "Say hello" --verbose

# Test Supabase
python3 -c "
import os; from dotenv import load_dotenv; load_dotenv()
from supabase import create_client
client = create_client(os.getenv('SUPABASE_URL'), os.getenv('SUPABASE_KEY'))
print('✅ Supabase connected')
"
```

---

## 🆘 Quick Fixes

| Problem | Solution |
|---------|----------|
| Port in use | `lsof -i :8000` then `kill -9 <PID>` |
| Ollama not running | `pkill ollama && ollama serve &` |
| Git push fails | `git pull origin main --rebase && git push` |
| Import error | `poetry install` or `pip install <package>` |
| GPU memory | Use `llama3.2:3b` instead of `8b` |

---

## 📅 15-Day Sprint Overview

| Days | Phase | Focus |
|------|-------|-------|
| 1-3 | Foundation | Setup, DB, API shell |
| 4-6 | OCR | Preprocessing, multi-engine OCR |
| 7-9 | Intelligence | Classification, extraction |
| 10-12 | Validation | Rules, stamps, fraud |
| 13-14 | Integration | MCP server, full pipeline |
| 15 | Launch | Testing, demo |

---

## 🔗 Key URLs

- **API Docs:** http://localhost:8000/docs
- **Streamlit UI:** http://localhost:8501
- **MCP Inspector:** `npx @modelcontextprotocol/inspector`
- **Supabase Dashboard:** https://supabase.com/dashboard
- **Gemini Studio:** https://aistudio.google.com

---

**Pro Tip:** Print this page and keep it next to your keyboard! 🖨️
