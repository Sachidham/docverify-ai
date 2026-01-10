import asyncio
import sys
import os

# Add src to path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from src.orchestration.processor import DocumentProcessor

async def main():
    if len(sys.argv) < 2:
        print("Usage: python test_pipeline.py <image_path>")
        image_path = "test_input.jpg"
        if not os.path.exists(image_path):
             print(f"Default file {image_path} not found.")
             return
    else:
        image_path = sys.argv[1]

    print(f"Testing pipeline with: {image_path}")
    
    try:
        processor = DocumentProcessor()
        result = await processor.process(image_path)
        
        print("\n--- Processing Result ---")
        print(f"Status: {result['status']}")
        print(f"Document Type: {result.get('document_type')}")
        print(f"Confidence: {result.get('confidence')}")
        print(f"Extracted Fields: {result.get('extracted_fields')}")
        print(f"Validation: {result.get('validation')}") # Added this line
        print("-------------------------")
        
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    asyncio.run(main())
