from typing import Dict, Any
from src.orchestration.agents.base_agent import BaseAgent

class ExtractionAgent(BaseAgent):
    """
    Agent responsible for extracting specific fields from text.
    """
    
    async def _initialize_impl(self, config: Dict[str, Any]):
        self.use_llm = config.get("use_llm", True)
        self.logger.info("Extraction Agent initialized")

    async def _process_impl(self, input_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Input: {"ocr_text": str, "document_type": str}
        Output: {"fields": dict}
        """
        doc_type = input_data.get("document_type")
        text = input_data.get("ocr_text", "")
        
        self.logger.info("Extracting fields", doc_type=doc_type)
        
        # Mock logic
        fields = {}
        if doc_type == "aadhaar_card":
             fields = {
                 "name": "Jane Doe",
                 "aadhaar_number": "1234 5678 9012"
             }
        
        return {
            "fields": fields,
            "extraction_method": "mock_regex"
        }
