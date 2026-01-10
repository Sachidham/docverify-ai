import re
from typing import Dict, Any, Optional
from structlog import get_logger
from src.extraction.patterns import DocumentPatterns
from src.core.config import get_settings

# Optional LLM imports
try:
    from langchain_google_genai import ChatGoogleGenerativeAI
    from langchain.schema import HumanMessage, SystemMessage
    from langchain.output_parsers import PydanticOutputParser
    from pydantic import BaseModel, Field
    HAS_LLM = True
except ImportError:
    HAS_LLM = False

logger = get_logger()
settings = get_settings()

class ExtractionEngine:
    """
    Extracts structured fields from OCR text using Regex + LLM Fallback.
    """
    
    def __init__(self):
        self.llm = None
        if HAS_LLM and settings.GOOGLE_API_KEY:
            try:
                self.llm = ChatGoogleGenerativeAI(
                    model=settings.GEMINI_MODEL,
                    google_api_key=settings.GOOGLE_API_KEY,
                    temperature=0.0
                )
                logger.info("Gemini Extractor initialized")
            except Exception as e:
                logger.warning("Failed to init Gemini for extraction", error=str(e))

    async def extract(self, text: str, doc_type: str) -> Dict[str, Any]:
        """
        Main extraction method.
        """
        # 1. Regex Extraction
        extracted_data = self.extract_by_regex(text, doc_type)
        
        # Check if critical fields are missing
        missing_critical_fields = self._check_missing_fields(extracted_data, doc_type)
        
        # 2. LLM Fallback if needed
        if missing_critical_fields and self.llm:
            logger.info("Critical fields missing, attempting LLM extraction", missing=missing_critical_fields)
            llm_data = await self.extract_by_llm(text, doc_type, missing_critical_fields)
            extracted_data.update(llm_data)
            
        return extracted_data

    def extract_by_regex(self, text: str, doc_type: str) -> Dict[str, Any]:
        logger.info(f"Running Regex extraction for {doc_type}")
        patterns = DocumentPatterns.get_patterns(doc_type)
        results = {}
        
        for field, pattern in patterns.items():
            match = re.search(pattern, text)
            if match:
                # If group is present, take it, else take whole match
                val = match.group(1) if match.groups() else match.group(0)
                results[field] = val.strip()
                
        return results

    async def extract_by_llm(self, text: str, doc_type: str, missing_fields: list) -> Dict[str, Any]:
        try:
            prompt = f"""
            Extract the following missing fields from the {doc_type} text below.
            Missing Fields: {', '.join(missing_fields)}
            
            Return the result as a plain JSON object with keys exactly matching the missing fields.
            Do NOT include markdown formatting.
            
            Text:
            {text[:3000]}
            """
            
            response = await self.llm.ainvoke([
                SystemMessage(content="You are a data extraction assistant. Output valid JSON only."),
                HumanMessage(content=prompt)
            ])
            
            # Simple parsing
            import json
            content = response.content.replace('```json', '').replace('```', '').strip()
            data = json.loads(content)
            return data
            
        except Exception as e:
            logger.error("LLM Extraction failed", error=str(e))
            return {}

    def _check_missing_fields(self, data: Dict, doc_type: str) -> list:
        """
        Define critical fields per document type that MUST be present.
        """
        critical_map = {
            "aadhaar_card": ["aadhaar_number"],
            "pan_card": ["pan_number"],
            "driving_license": ["dl_number"],
            "voter_id": ["voter_id_number"]
        }
        
        required = critical_map.get(doc_type, [])
        missing = [f for f in required if f not in data]
        return missing
