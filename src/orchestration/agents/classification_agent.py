from typing import Dict, Any
from src.orchestration.agents.base_agent import BaseAgent
# Import inside method or try-except block in init if strictly needed, 
# but usually top level is fine if order is correct.
# from src.classification.engine import DocumentClassifier

class ClassificationAgent(BaseAgent):
    """
    Agent responsible for identifying document type from text.
    """
    
    async def _initialize_impl(self, config: Dict[str, Any]):
        from src.classification.engine import DocumentClassifier
        self.classifier = DocumentClassifier()
        self.logger.info("Classification Agent initialized")

    async def _process_impl(self, input_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Input: {"ocr_text": str} or {"text": str}
        Output: {"document_type": str, "confidence": float}
        """
        # Support both keys (OCR agent output might be "text")
        text = input_data.get("ocr_text") or input_data.get("text")
        
        if not text:
            # Fallback if no text provided
            self.logger.warning("No text provided for classification")
            return {
                "document_type": "unknown",
                "confidence": 0.0,
                "reason": "empty_input"
            }

        self.logger.info("Classifying document...", text_preview=text[:50])
        
        result = await self.classifier.classify(text)
        
        return {
            "document_type": result["type"],
            "confidence": result["confidence"],
            "method": result["method"]
        }
