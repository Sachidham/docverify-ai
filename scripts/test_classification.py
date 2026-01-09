import asyncio
import sys
import os

# Add project root to path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from src.classification.engine import DocumentClassifier

async def test_classification():
    print("🚀 Testing Document Classification...")
    classifier = DocumentClassifier()
    
    # Case 1: Clear Rule-Based Match (PAN)
    print("\n--- Case 1: Strong Pattern (PAN) ---")
    text_pan = "INCOME TAX DEPARTMENT GOVT OF INDIA ... ABCDE1234F ... Signature"
    res_pan = await classifier.classify(text_pan)
    print(f"Input: {text_pan[:30]}...")
    print(f"Result: {res_pan}")
    
    # Case 2: Clear Rule-Based Match (Aadhaar)
    print("\n--- Case 2: Strong Pattern (Aadhaar) ---")
    text_aadhaar = "Unique Identification Authority of India ... Mera Aadhaar ... 1234 5678 9101"
    res_aadhaar = await classifier.classify(text_aadhaar)
    print(f"Input: {text_aadhaar[:30]}...")
    print(f"Result: {res_aadhaar}")
    
    # Case 3: Ambiguous / LLM Fallback (if configured)
    print("\n--- Case 3: Ambiguous Text (LLM Check) ---")
    text_ambiguous = "This is an official identification document issued by the election commission containing name and father name. EPIC: ABC1234567"
    if classifier.llm:
        print("(Gemini is enabled, this should try LLM if regex fails)")
    res_ambiguous = await classifier.classify(text_ambiguous)
    print(f"Input: {text_ambiguous[:50]}...")
    print(f"Result: {res_ambiguous}")

if __name__ == "__main__":
    asyncio.run(test_classification())
