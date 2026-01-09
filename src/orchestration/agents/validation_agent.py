from typing import Dict, Any
from src.orchestration.agents.base_agent import BaseAgent

class ValidationAgent(BaseAgent):
    """
    Agent responsible for validating extracted fields.
    """
    
    async def _initialize_impl(self, config: Dict[str, Any]):
        self.strict_mode = config.get("strict", False)
        self.logger.info("Validation Agent initialized")

    async def _process_impl(self, input_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Input: {"fields": dict, "document_type": str}
        Output: {"validation_results": dict, "is_valid": bool}
        """
        fields = input_data.get("fields", {})
        
        self.logger.info("Validating fields", count=len(fields))
        
        results = {}
        valid = True
        
        for key, value in fields.items():
            # Mock validation
            if "number" in key and len(value) < 5:
                 results[key] = {"valid": False, "reason": "Too short"}
                 valid = False
            else:
                 results[key] = {"valid": True}
                 
        return {
            "validation_results": results,
            "is_valid": valid
        }
