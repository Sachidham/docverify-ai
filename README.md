# 🔍 DocVerify AI

AI-Powered Document Verification Platform for Indian official documents.

## Features

- **Multi-Engine OCR**: PaddleOCR, EasyOCR, and Tesseract with multi-language support
- **LLM Integration**: Google Gemini and Ollama for intelligent document understanding
- **Document Classification**: Automatic detection of document types
- **Fraud Detection**: AI-powered tampering and forgery detection
- **Modern Stack**: FastAPI backend, Streamlit UI, Supabase database

## Quick Start

```bash
# Activate virtual environment
poetry shell

# Run FastAPI server
uvicorn src.api.main:app --reload --port 8000

# In another terminal, run Streamlit UI
streamlit run ui/app.py
```

## Project Structure

```
docverify-ai/
├── src/                    # Main source code
│   ├── api/               # FastAPI endpoints
│   ├── core/              # Core configuration
│   ├── database/          # Database clients
│   ├── ocr/               # OCR engines
│   ├── llm/               # LLM integrations
│   └── ...
├── ui/                    # Streamlit frontend
├── tests/                 # Test suite
└── docs/                  # Documentation
```

## Environment Setup

1. Copy `.env` and fill in your API keys
2. Ensure Python 3.11+ is installed
3. Run `poetry install`

## License

Private
