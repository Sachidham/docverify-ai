import asyncio
import sys
import os

# Add project root to path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from src.orchestration.agent_manager import AgentManager
from src.orchestration.agents import OCRAgent, ClassificationAgent, ExtractionAgent

async def main():
    print("🚀 Starting Agent Verification...")
    
    # 1. Initialize Manager
    manager = AgentManager()
    
    # 2. Register Agent Types
    print("📝 Registering agents...")
    manager.register_agent_type("ocr", OCRAgent)
    manager.register_agent_type("classification", ClassificationAgent)
    manager.register_agent_type("extraction", ExtractionAgent)
    
    # 3. Spawn Agents
    print("✨ Spawning agents...")
    ocr_id = await manager.spawn_agent("ocr", {"engine": "easyocr"})
    cls_id = await manager.spawn_agent("classification", {})
    ext_id = await manager.spawn_agent("extraction", {})
    
    print(f"   - OCR Agent: {ocr_id}")
    print(f"   - Classify Agent: {cls_id}")
    print(f"   - Extract Agent: {ext_id}")
    
    # 4. Run simple flow
    print("⚡ Running flow...")
    
    # Step A: OCR
    print("\n--- Step 1: OCR ---")
    ocr_result = await manager.get_agent(ocr_id).process({"image_path": "dummy.jpg"})
    print(f"OCR Output: {ocr_result['text'][:30]}...")
    
    # Step B: Classification
    print("\n--- Step 2: Classification ---")
    cls_result = await manager.get_agent(cls_id).process({"ocr_text": "Aadhaar Card Details..."})
    print(f"Doc Type: {cls_result['document_type']}")
    
    # Step C: Extraction
    print("\n--- Step 3: Extraction ---")
    ext_result = await manager.get_agent(ext_id).process({
        "ocr_text": ocr_result['text'], 
        "document_type": cls_result['document_type']
    })
    print(f"Extracted: {ext_result['fields']}")
    
    # 5. Shutdown
    print("\n🛑 Shutting down...")
    await manager.shutdown_all()
    print("✅ Verification Complete!")

if __name__ == "__main__":
    asyncio.run(main())
