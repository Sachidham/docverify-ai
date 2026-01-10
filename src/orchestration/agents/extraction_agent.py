from typing import Dict, Any
from src.orchestration.agents.base_agent import BaseAgent
# Import at method level if needed, but safe here if extraction/engine exists
# from src.extraction.engine import ExtractionEngine

class ExtractionAgent(BaseAgent):
    """
    Agent responsible for extracting columns/fields from structured text.
    """
    
    async def _initialize_impl(self, config: Dict[str, Any]):
        from src.extraction.engine import ExtractionEngine
        self.engine = ExtractionEngine()
        self.logger.info("Extraction Agent initialized")

    async def _process_impl(self, input_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Input: {"text": str, "document_type": str}
        Output: {"extracted_data": dict}
        """
        text = input_data.get("text")
        doc_type = input_data.get("document_type", "unknown")
        
        if not text:
            raise ValueError("text input is required for extraction")
            
        self.logger.info("Extracting data...", doc_type=doc_type)
        
        extracted_data = await self.engine.extract(text, doc_type)
        
        return {
            "extracted_data": extracted_data,
            "status": "success"
        }
