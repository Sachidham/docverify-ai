import asyncio
import sys
import os
import json

# Add project root to path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from src.extraction.engine import ExtractionEngine

async def test_extraction():
    print("🚀 Testing Data Extraction...")
    engine = ExtractionEngine()
    
    # Case 1: PAN Card (Regex should find ID and DOB)
    print("\n--- Case 1: PAN Card (Regex Focused) ---")
    text_pan = "INCOME TAX DEPARTMENT ... Permanent Account Number ABCDE1234F ... Date of Birth 20/01/1990"
    res_pan = await engine.extract(text_pan, "pan_card")
    print(f"Result: {json.dumps(res_pan, indent=2)}")
    
    # Case 2: Aadhaar Card (LLM Focused for Name/Address)
    print("\n--- Case 2: Aadhaar Card (LLM Focused) ---")
    text_aadhaar = "Unique Identification Authority of India ... Address: 123 Main St, Bangalore, Karnataka ... 1234 5678 9102"
    
    if engine.llm:
        print("(Gemini is enabled, expectation: Name=None (not in text), Address=Found, ID=Found via regex)")
    else:
        print("(Gemini DISABLED, will only find ID via Regex)")
        
    res_aadhaar = await engine.extract(text_aadhaar, "aadhaar_card")
    print(f"Result: {json.dumps(res_aadhaar, indent=2)}")

if __name__ == "__main__":
    asyncio.run(test_extraction())
