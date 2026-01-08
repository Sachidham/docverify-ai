# 🚀 DocVerify AI - Complete Setup Guide

## Setting up on Antigravity (Jarvis Labs) + GitHub Sync

---

## 📋 Prerequisites Checklist

Before starting, make sure you have:

- [ ] Antigravity/Jarvis Labs account with GPU credits
- [ ] GitHub account
- [ ] Google account (for free Gemini API)
- [ ] Supabase account (free tier)

---

## Part 1: GitHub Repository Setup

### Step 1.1: Create GitHub Repository

```bash
# On your LOCAL machine first (or do it on GitHub website)

# Option A: Create on GitHub website
# 1. Go to https://github.com/new
# 2. Repository name: docverify-ai
# 3. Description: AI-Powered Document Verification Platform
# 4. Make it Private (recommended for now)
# 5. Check "Add a README file"
# 6. Add .gitignore: Python
# 7. Click "Create repository"
```

### Step 1.2: Generate GitHub Personal Access Token (PAT)

You'll need this to push from Antigravity:

1. Go to **GitHub → Settings → Developer settings → Personal access tokens → Tokens (classic)**
2. Click **"Generate new token (classic)"**
3. Give it a name: `antigravity-docverify`
4. Set expiration: 90 days (or your preference)
5. Select scopes:
   - ✅ `repo` (full control of private repositories)
   - ✅ `workflow` (if you plan to use GitHub Actions)
6. Click **"Generate token"**
7. **⚠️ COPY THE TOKEN NOW** - you won't see it again!
8. Save it somewhere safe (password manager, secure note)

---

## Part 2: Antigravity/Jarvis Labs Setup

### Step 2.1: Launch GPU Instance

1. Log into **Antigravity/Jarvis Labs** dashboard
2. Click **"Create Instance"** or **"Launch"**
3. Select configuration:
   ```
   Framework: PyTorch (latest) or Custom
   GPU: RTX 3090 / A4000 / A5000 (any with 24GB+ VRAM ideal)
   Storage: 50GB minimum (100GB recommended)
   ```
4. Click **Launch** and wait for instance to start
5. Click **"Open JupyterLab"** or get SSH access

### Step 2.2: Initial System Setup

Open a **Terminal** in JupyterLab (or SSH):

```bash
# ============================================
# STEP 2.2.1: Update system
# ============================================
sudo apt update && sudo apt upgrade -y

# ============================================
# STEP 2.2.2: Install system dependencies
# ============================================
sudo apt install -y \
    git \
    git-lfs \
    build-essential \
    libgl1-mesa-glx \
    libglib2.0-0 \
    libsm6 \
    libxext6 \
    libxrender-dev \
    libgomp1 \
    tesseract-ocr \
    tesseract-ocr-hin \
    tesseract-ocr-tam \
    tesseract-ocr-tel \
    poppler-utils \
    ffmpeg

# ============================================
# STEP 2.2.3: Verify GPU is available
# ============================================
nvidia-smi

# You should see your GPU listed (e.g., RTX 3090, A4000, etc.)
```

### Step 2.3: Configure Git

```bash
# ============================================
# STEP 2.3.1: Set your Git identity
# ============================================
git config --global user.name "Your Name"
git config --global user.email "your.email@example.com"

# ============================================
# STEP 2.3.2: Store credentials (so you don't re-enter every time)
# ============================================
git config --global credential.helper store

# ============================================
# STEP 2.3.3: Set default branch name
# ============================================
git config --global init.defaultBranch main
```

### Step 2.4: Clone Your Repository

```bash
# ============================================
# STEP 2.4.1: Navigate to workspace
# ============================================
cd ~
# Or if Jarvis Labs has a specific workspace:
# cd /home/jarvis/workspace

# ============================================
# STEP 2.4.2: Clone the repository
# ============================================
# Replace YOUR_USERNAME with your GitHub username
git clone https://github.com/YOUR_USERNAME/docverify-ai.git

# When prompted:
# Username: YOUR_GITHUB_USERNAME
# Password: YOUR_PERSONAL_ACCESS_TOKEN (paste the PAT you created)

# ============================================
# STEP 2.4.3: Enter project directory
# ============================================
cd docverify-ai
```

---

## Part 3: Python Environment Setup

### Step 3.1: Install Python Tools

```bash
# ============================================
# STEP 3.1.1: Check Python version (should be 3.10+)
# ============================================
python3 --version

# ============================================
# STEP 3.1.2: Install pip and venv
# ============================================
sudo apt install -y python3-pip python3-venv

# ============================================
# STEP 3.1.3: Install Poetry (recommended package manager)
# ============================================
curl -sSL https://install.python-poetry.org | python3 -

# Add Poetry to PATH
echo 'export PATH="$HOME/.local/bin:$PATH"' >> ~/.bashrc
source ~/.bashrc

# Verify installation
poetry --version
```

### Step 3.2: Create Project Structure

```bash
# ============================================
# STEP 3.2.1: Create directory structure
# ============================================
mkdir -p src/{core,database,preprocessing,ocr,classification,extraction,validation,detection,fraud,llm,rag,orchestration,api,mcp}
mkdir -p src/api/{routes,schemas,middleware}
mkdir -p src/database/repositories
mkdir -p src/classification/templates
mkdir -p src/extraction/field_types
mkdir -p src/validation/rules
mkdir -p src/llm/{prompts,chains}
mkdir -p src/orchestration/{agents,tools}
mkdir -p src/mcp/{tools,resources}
mkdir -p ui/{pages,components,styles}
mkdir -p synthetic_data/{templates,fonts,samples}
mkdir -p tests/{unit,integration,fixtures}
mkdir -p scripts
mkdir -p docs

# ============================================
# STEP 3.2.2: Create __init__.py files
# ============================================
find src -type d -exec touch {}/__init__.py \;

# ============================================
# STEP 3.2.3: Verify structure
# ============================================
tree -L 3 src/
# If tree not installed: sudo apt install tree
```

### Step 3.3: Initialize Poetry Project

```bash
# ============================================
# STEP 3.3.1: Initialize Poetry
# ============================================
poetry init --name docverify-ai \
    --description "AI-Powered Document Verification Platform" \
    --author "Your Name <your.email@example.com>" \
    --python "^3.10" \
    --no-interaction

# ============================================
# STEP 3.3.2: Add core dependencies
# ============================================
# Web Framework
poetry add fastapi uvicorn[standard] python-multipart

# UI
poetry add streamlit

# Database
poetry add supabase sqlalchemy asyncpg pgvector

# LLM & AI
poetry add langchain langchain-google-genai langchain-community
poetry add llama-index llama-index-llms-ollama llama-index-embeddings-ollama
poetry add google-generativeai ollama

# OCR (this may take a while)
poetry add paddleocr paddlepaddle  # Use paddlepaddle-gpu if GPU available
poetry add easyocr
poetry add pytesseract

# Image Processing
poetry add opencv-python Pillow scikit-image

# PDF Processing
poetry add PyMuPDF img2table

# MCP Server
poetry add mcp

# Utilities
poetry add pydantic pydantic-settings python-dotenv httpx numpy pandas structlog

# Synthetic Data
poetry add Faker reportlab

# ============================================
# STEP 3.3.3: Add dev dependencies
# ============================================
poetry add --group dev pytest pytest-asyncio black ruff mypy

# ============================================
# STEP 3.3.4: Install all dependencies
# ============================================
poetry install
```

**⚠️ Note:** If PaddleOCR installation fails, try:
```bash
# For GPU version
pip install paddlepaddle-gpu -i https://mirror.baidu.com/pypi/simple
poetry add paddleocr
```

---

## Part 4: Install & Configure Ollama

### Step 4.1: Install Ollama

```bash
# ============================================
# STEP 4.1.1: Download and install Ollama
# ============================================
curl -fsSL https://ollama.com/install.sh | sh

# ============================================
# STEP 4.1.2: Start Ollama service
# ============================================
# Option A: Run in background
ollama serve &

# Option B: Run in a separate terminal/screen
# screen -S ollama
# ollama serve
# Ctrl+A, D to detach

# ============================================
# STEP 4.1.3: Wait a few seconds, then verify
# ============================================
sleep 5
curl http://localhost:11434/api/tags
```

### Step 4.2: Pull Required Models

```bash
# ============================================
# STEP 4.2.1: Pull Llama 3.1 8B (main reasoning model)
# ============================================
ollama pull llama3.1:8b
# This will take 5-10 minutes (4.7GB download)

# ============================================
# STEP 4.2.2: Pull embedding model
# ============================================
ollama pull nomic-embed-text
# About 274MB

# ============================================
# STEP 4.2.3: Pull vision model (optional but recommended)
# ============================================
ollama pull llava:7b
# About 4.5GB

# ============================================
# STEP 4.2.4: Verify models are installed
# ============================================
ollama list

# Expected output:
# NAME                 ID              SIZE      MODIFIED
# llama3.1:8b          xxx             4.7 GB    Just now
# nomic-embed-text     xxx             274 MB    Just now
# llava:7b             xxx             4.5 GB    Just now
```

### Step 4.3: Test Ollama

```bash
# Quick test
ollama run llama3.1:8b "Say hello in Hindi"
# Expected: नमस्ते (Namaste) or similar

# Exit with /bye or Ctrl+D
```

---

## Part 5: Get Free API Keys

### Step 5.1: Google Gemini API Key (FREE)

1. Go to: **https://aistudio.google.com/apikey**
2. Sign in with your Google account
3. Click **"Create API Key"**
4. Select or create a Google Cloud project
5. **Copy the API key** - looks like: `AIzaSy...`
6. Save it securely

**Free Tier Limits:**
- 15 requests/minute
- 1,500 requests/day
- 1 million tokens/minute

### Step 5.2: Supabase Setup (FREE)

1. Go to: **https://supabase.com**
2. Click **"Start your project"** → Sign up/Log in
3. Click **"New Project"**
4. Fill in:
   - **Name:** docverify-ai
   - **Database Password:** (generate a strong one, SAVE IT!)
   - **Region:** Choose closest to you
5. Click **"Create new project"** (takes 2 minutes)
6. Once ready, go to **Settings → API**
7. Copy these values:
   - **Project URL:** `https://xxxxx.supabase.co`
   - **anon/public key:** `eyJhbGc...`
   - **service_role key:** `eyJhbGc...` (keep this SECRET!)

### Step 5.3: Setup Supabase Database

1. In Supabase dashboard, go to **SQL Editor**
2. Click **"New Query"**
3. Paste this SQL and run it:

```sql
-- Enable pgvector extension
CREATE EXTENSION IF NOT EXISTS vector;

-- Document Types Enum
CREATE TYPE document_type AS ENUM (
    'birth_certificate',
    'aadhaar_card', 
    'pan_card',
    'driving_license',
    'voter_id',
    'passport',
    'income_certificate',
    'caste_certificate',
    'domicile_certificate',
    'other'
);

-- Verification Status Enum
CREATE TYPE verification_status AS ENUM (
    'pending',
    'processing', 
    'verified',
    'rejected',
    'manual_review'
);

-- Documents Table
CREATE TABLE documents (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    file_name VARCHAR(255) NOT NULL,
    file_path TEXT NOT NULL,
    file_hash VARCHAR(64) NOT NULL,
    mime_type VARCHAR(100),
    file_size_bytes INTEGER,
    document_type document_type,
    detected_language VARCHAR(50),
    raw_ocr_text TEXT,
    structured_data JSONB,
    embedding vector(768),
    uploaded_by UUID,
    created_at TIMESTAMPTZ DEFAULT NOW(),
    updated_at TIMESTAMPTZ DEFAULT NOW()
);

-- Verifications Table
CREATE TABLE verifications (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    document_id UUID REFERENCES documents(id) ON DELETE CASCADE,
    status verification_status DEFAULT 'pending',
    overall_confidence DECIMAL(5,4),
    extracted_fields JSONB,
    field_confidences JSONB,
    validation_results JSONB,
    stamps_detected JSONB,
    signatures_detected JSONB,
    fraud_flags JSONB,
    tamper_score DECIMAL(5,4),
    duplicate_match_id UUID,
    processing_time_ms INTEGER,
    ocr_engine_used VARCHAR(50),
    llm_model_used VARCHAR(100),
    verified_by UUID,
    verified_at TIMESTAMPTZ,
    created_at TIMESTAMPTZ DEFAULT NOW(),
    updated_at TIMESTAMPTZ DEFAULT NOW()
);

-- Audit Logs Table
CREATE TABLE audit_logs (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    document_id UUID REFERENCES documents(id),
    verification_id UUID REFERENCES verifications(id),
    action VARCHAR(100) NOT NULL,
    actor_id UUID,
    actor_type VARCHAR(50),
    details JSONB,
    ip_address INET,
    created_at TIMESTAMPTZ DEFAULT NOW()
);

-- Indexes
CREATE INDEX idx_documents_type ON documents(document_type);
CREATE INDEX idx_documents_hash ON documents(file_hash);
CREATE INDEX idx_documents_embedding ON documents USING ivfflat (embedding vector_cosine_ops);
CREATE INDEX idx_verifications_status ON verifications(status);
CREATE INDEX idx_verifications_document ON verifications(document_id);
CREATE INDEX idx_audit_document ON audit_logs(document_id);
```

4. Click **"Run"** (or Ctrl+Enter)
5. You should see "Success. No rows returned"

---

## Part 6: Configure Environment Variables

### Step 6.1: Create .env File

```bash
# In your project directory on Antigravity
cd ~/docverify-ai

# Create .env file
cat > .env << 'EOF'
# ============================================
# DocVerify AI - Environment Configuration
# ============================================

# ----- Supabase -----
SUPABASE_URL=https://YOUR_PROJECT_ID.supabase.co
SUPABASE_KEY=your-anon-public-key
SUPABASE_SERVICE_KEY=your-service-role-key

# ----- Google Gemini (Free Tier) -----
GOOGLE_API_KEY=your-gemini-api-key

# ----- Ollama (Local) -----
OLLAMA_BASE_URL=http://localhost:11434
OLLAMA_MODEL=llama3.1:8b
OLLAMA_EMBED_MODEL=nomic-embed-text
OLLAMA_VISION_MODEL=llava:7b

# ----- Application Settings -----
APP_NAME=DocVerify AI
APP_ENV=development
DEBUG=true
LOG_LEVEL=INFO

# ----- API Settings -----
API_HOST=0.0.0.0
API_PORT=8000
API_WORKERS=4

# ----- MCP Server -----
MCP_HOST=0.0.0.0
MCP_PORT=8001

# ----- Streamlit -----
STREAMLIT_PORT=8501

# ----- OCR Settings -----
DEFAULT_OCR_ENGINE=paddleocr
OCR_LANGUAGES=en,hi,ta,te
OCR_CONFIDENCE_THRESHOLD=0.6

# ----- Processing Settings -----
MAX_FILE_SIZE_MB=20
SUPPORTED_FORMATS=pdf,png,jpg,jpeg,tiff
DEFAULT_DPI=300

# ----- Security -----
SECRET_KEY=change-this-to-a-random-string-in-production
CORS_ORIGINS=http://localhost:8501,http://localhost:3000
EOF
```

### Step 6.2: Edit .env with Your Actual Keys

```bash
# Open .env in editor
nano .env

# Replace these placeholders with your actual values:
# - SUPABASE_URL
# - SUPABASE_KEY
# - SUPABASE_SERVICE_KEY
# - GOOGLE_API_KEY

# Save: Ctrl+O, Enter
# Exit: Ctrl+X
```

### Step 6.3: Add .env to .gitignore

```bash
# Create/update .gitignore
cat >> .gitignore << 'EOF'

# Environment variables
.env
.env.local
.env.*.local

# Python
__pycache__/
*.py[cod]
*$py.class
*.so
.Python
build/
develop-eggs/
dist/
downloads/
eggs/
.eggs/
lib/
lib64/
parts/
sdist/
var/
wheels/
*.egg-info/
.installed.cfg
*.egg

# Virtual environments
venv/
ENV/
.venv/

# IDE
.idea/
.vscode/
*.swp
*.swo

# Jupyter
.ipynb_checkpoints/

# Testing
.pytest_cache/
.coverage
htmlcov/

# Models (large files)
*.pt
*.pth
*.onnx
*.pkl
models/

# Logs
logs/
*.log

# OS
.DS_Store
Thumbs.db
EOF
```

---

## Part 7: Copy Starter Code

### Step 7.1: Download Starter Files

Copy the starter code files I provided earlier into your project:

```bash
# Create the files from the blueprint I gave you
# You can copy-paste the content from the files I created

# Option 1: If you saved them locally, use scp/sftp to upload

# Option 2: Create files directly (example for one file):
nano src/core/config.py
# Paste content from the config.py I provided
# Save and exit

# Repeat for:
# - src/core/config.py
# - src/ocr/engine.py
# - src/llm/clients.py
# - src/api/main.py
# - src/mcp/server.py
# - ui/app.py
```

### Step 7.2: Alternative - Quick Setup Script

```bash
# Create a setup script to generate all starter files
cat > scripts/create_starter_files.sh << 'SCRIPT_EOF'
#!/bin/bash

echo "Creating starter files..."

# This script assumes you have the file contents ready
# You can add the actual file creation commands here

echo "✅ Starter files created!"
echo "Next: Copy the actual code content from the blueprint"
SCRIPT_EOF

chmod +x scripts/create_starter_files.sh
```

---

## Part 8: First Git Commit & Push

### Step 8.1: Check Status

```bash
cd ~/docverify-ai

# See what files are ready to commit
git status
```

### Step 8.2: Stage and Commit

```bash
# ============================================
# STEP 8.2.1: Add all files
# ============================================
git add .

# ============================================
# STEP 8.2.2: Check what will be committed
# ============================================
git status

# Make sure .env is NOT in the list!
# If it is, run: git reset HEAD .env

# ============================================
# STEP 8.2.3: Create first commit
# ============================================
git commit -m "🎉 Initial project setup

- Project structure created
- Poetry dependencies configured
- Core modules scaffolded
- Environment template added
- Database schema defined"
```

### Step 8.3: Push to GitHub

```bash
# ============================================
# STEP 8.3.1: Push to main branch
# ============================================
git push origin main

# If prompted for credentials:
# Username: YOUR_GITHUB_USERNAME
# Password: YOUR_PERSONAL_ACCESS_TOKEN
```

---

## Part 9: Verify Everything Works

### Step 9.1: Test Imports

```bash
# Activate Poetry environment
poetry shell

# Test Python imports
python3 << 'EOF'
print("Testing imports...")

# Core
from pydantic import BaseModel
from pydantic_settings import BaseSettings
print("✅ Pydantic OK")

# FastAPI
from fastapi import FastAPI
print("✅ FastAPI OK")

# Streamlit
import streamlit
print("✅ Streamlit OK")

# Supabase
from supabase import create_client
print("✅ Supabase OK")

# LangChain
from langchain_google_genai import ChatGoogleGenerativeAI
print("✅ LangChain OK")

# LlamaIndex
from llama_index.core import VectorStoreIndex
print("✅ LlamaIndex OK")

# OCR
from paddleocr import PaddleOCR
print("✅ PaddleOCR OK")

import easyocr
print("✅ EasyOCR OK")

# Image Processing
import cv2
from PIL import Image
print("✅ OpenCV & Pillow OK")

# Google Gemini
import google.generativeai as genai
print("✅ Google Gemini OK")

print("\n🎉 All imports successful!")
EOF
```

### Step 9.2: Test Gemini Connection

```bash
python3 << EOF
import os
from dotenv import load_dotenv
import google.generativeai as genai

load_dotenv()

genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))
model = genai.GenerativeModel('gemini-2.0-flash-exp')

response = model.generate_content("Say 'DocVerify AI is ready!' in Hindi")
print(response.text)
EOF
```

Expected output: Something like "DocVerify AI तैयार है!" 

### Step 9.3: Test Supabase Connection

```bash
python3 << EOF
import os
from dotenv import load_dotenv
from supabase import create_client

load_dotenv()

supabase = create_client(
    os.getenv("SUPABASE_URL"),
    os.getenv("SUPABASE_KEY")
)

# Test connection by checking tables
result = supabase.table("documents").select("id").limit(1).execute()
print("✅ Supabase connected successfully!")
print(f"Documents table accessible: {result}")
EOF
```

### Step 9.4: Test Ollama

```bash
python3 << EOF
import ollama

response = ollama.chat(model='llama3.1:8b', messages=[
    {'role': 'user', 'content': 'Say hello in Tamil'}
])
print(response['message']['content'])
EOF
```

---

## Part 10: Run the Application

### Step 10.1: Start All Services

Open **3 separate terminals** (or use `screen`/`tmux`):

**Terminal 1 - Ollama:**
```bash
ollama serve
```

**Terminal 2 - FastAPI:**
```bash
cd ~/docverify-ai
poetry shell
uvicorn src.api.main:app --reload --host 0.0.0.0 --port 8000
```

**Terminal 3 - Streamlit:**
```bash
cd ~/docverify-ai
poetry shell
streamlit run ui/app.py --server.port 8501 --server.address 0.0.0.0
```

### Step 10.2: Access the Application

On Antigravity/Jarvis Labs, you'll need to use port forwarding or the provided URLs:

- **API Docs:** `http://YOUR_INSTANCE_IP:8000/docs`
- **Streamlit UI:** `http://YOUR_INSTANCE_IP:8501`

If using JupyterLab, look for port forwarding options in the interface.

---

## Part 11: Daily Workflow

### Starting Each Day

```bash
# 1. SSH or open JupyterLab

# 2. Start Ollama (if not already running)
ollama serve &

# 3. Navigate to project
cd ~/docverify-ai

# 4. Pull latest changes (if teammate pushed)
git pull origin main

# 5. Activate environment
poetry shell

# 6. Start development
# ... write code ...

# 7. Test changes
python -m pytest tests/

# 8. Commit and push
git add .
git commit -m "feat: describe what you did"
git push origin main
```

### When Your Teammate Wants to Join

Share these with them:
1. GitHub repository invite (Settings → Collaborators)
2. Supabase project invite (Settings → Team)
3. This setup guide!

They follow the same steps but clone your existing repo.

---

## 🎯 Checkpoint: Day 1 Complete!

By now you should have:

- [x] GitHub repo created and cloned
- [x] Antigravity instance running
- [x] Python environment with all dependencies
- [x] Ollama running with 3 models
- [x] Gemini API key working
- [x] Supabase database with schema
- [x] Project structure created
- [x] First commit pushed!

**Next: Day 2** - Implement `src/core/config.py` and `src/database/client.py`

---

## 🆘 Troubleshooting

### Problem: PaddleOCR installation fails
```bash
# Try installing paddlepaddle first
pip install paddlepaddle-gpu==2.6.0 -f https://www.paddlepaddle.org.cn/whl/linux/mkl/avx/stable.html
pip install paddleocr
```

### Problem: Ollama not connecting
```bash
# Check if running
ps aux | grep ollama

# Restart
pkill ollama
ollama serve &
```

### Problem: Git push rejected
```bash
# Pull first, then push
git pull origin main --rebase
git push origin main
```

### Problem: Port already in use
```bash
# Find and kill process using port 8000
lsof -i :8000
kill -9 <PID>
```

### Problem: Out of GPU memory
```bash
# Use smaller models
ollama pull llama3.2:3b  # Instead of 8b
```

---

**Questions? Issues?** Let me know what step you're stuck on!
