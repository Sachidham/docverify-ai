import asyncio
import sys
import os

# Add project root to path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from src.orchestration.agent_manager import AgentManager
from src.orchestration.agents import OCRAgent

async def verify_ocr():
    print("🚀 Starting OCR Integration Verification...")
    
    # 1. Setup
    manager = AgentManager()
    manager.register_agent_type("ocr", OCRAgent)
    
    # 2. Spawn Agent
    print("✨ Spawning OCR Agent...")
    agent_id = await manager.spawn_agent("ocr", {"engine": "paddleocr"})
    
    # 3. Process Image
    # Ensure test image exists (from previous step)
    image_path = "test_input.jpg"
    if not os.path.exists(image_path):
        # Create dummy if missing (simple text)
        import cv2
        import numpy as np
        img = np.ones((200, 600, 3), dtype=np.uint8) * 255
        cv2.putText(img, 'DocVerify AI Test', (50, 100), cv2.FONT_HERSHEY_SIMPLEX, 2, (0,0,0), 3)
        cv2.imwrite(image_path, img)
        print("Created temp test image")

    print(f"📄 Processing: {image_path}")
    # Fix: AgentManager doesn't have process_task, get agent first
    agent = manager.get_agent(agent_id)
    if not agent:
        print("❌ Agent not found")
        return
        
    result = await agent.process({"image_path": image_path})
    
    # 4. Results
    print("\n--- Result ---")
    print(f"Engine: {result.get('engine')}")
    print(f"Confidence: {result.get('confidence')}")
    print(f"Text:\n{result.get('text')}")
    print("-------------\n")
    
    await manager.shutdown_all()

if __name__ == "__main__":
    asyncio.run(verify_ocr())
