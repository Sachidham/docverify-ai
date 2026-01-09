import re
from typing import Dict, Any, Optional
from structlog import get_logger

from src.classification.rules import DOCUMENT_TEMPLATES
from src.core.config import get_settings

# Optional LLM imports (graceful degradation if keys missing)
try:
    from langchain_google_genai import ChatGoogleGenerativeAI
    from langchain.schema import HumanMessage, SystemMessage
    HAS_LLM = True
except ImportError:
    HAS_LLM = False

logger = get_logger()
settings = get_settings()

class DocumentClassifier:
    """
    Hybrid classifier: Rule-based (Fast) + LLM (Smart).
    """
    
    def __init__(self):
        self.templates = DOCUMENT_TEMPLATES
        self.llm = None
        
        if HAS_LLM and settings.GOOGLE_API_KEY:
            try:
                self.llm = ChatGoogleGenerativeAI(
                    model=settings.GEMINI_MODEL,
                    google_api_key=settings.GOOGLE_API_KEY,
                    temperature=0.0
                )
                logger.info("Gemini Classifier initialized")
            except Exception as e:
                logger.warning("Failed to init Gemini for classification", error=str(e))

    async def classify(self, text: str) -> Dict[str, Any]:
        """
        Main entry point. Tries rules first, then LLM.
        """
        # 1. Rule Based
        rule_result = self.classify_by_rules(text)
        if rule_result["confidence"] > 0.6:
            logger.info("Rule-based classification successful", type=rule_result["type"])
            return rule_result
            
        # 2. LLM Based (Fallback)
        if self.llm:
            logger.info("Rule-based confidence low, trying LLM...")
            return await self.classify_by_llm(text)
            
        return rule_result

    def classify_by_rules(self, text: str) -> Dict[str, Any]:
        text_lower = text.lower()
        best_match = None
        max_score = 0.0
        
        for doc_type, template in self.templates.items():
            score = 0
            # Keyword match
            matches = sum(1 for k in template.keywords if k in text_lower)
            if matches >= template.min_keywords:
                score += matches * 0.2
                
            # Regex match
            for pattern in template.regex_patterns:
                if re.search(pattern, text):
                    score += 0.5  # Strong signal
            
            if score > max_score:
                max_score = score
                best_match = doc_type

        # Normalize confidence (cap at 1.0)
        confidence = min(max_score, 1.0)
        
        if confidence > 0.0:
            return {"type": best_match, "confidence": confidence, "method": "rule_based"}
            
        return {"type": "unknown", "confidence": 0.0, "method": "rule_based"}

    async def classify_by_llm(self, text: str) -> Dict[str, Any]:
        try:
            prompt = f"""
            Identify the type of Indian official document from the extracted text below.
            Possible types: Aadhaar Card, PAN Card, Voter ID, Driving License.
            If unsure, return 'unknown'.
            
            Return ONLY the internal code: 'aadhaar_card', 'pan_card', 'voter_id', 'driving_license', or 'unknown'.
            
            Text:
            {text[:2000]} 
            """
            
            response = await self.llm.ainvoke([
                SystemMessage(content="You are a document classifier bot."),
                HumanMessage(content=prompt)
            ])
            
            doc_type = response.content.strip().lower()
            
            # Basic validation of output
            valid_types = list(self.templates.keys()) + ["unknown"]
            cleaned_type = "unknown"
            for vt in valid_types:
                if vt in doc_type:
                    cleaned_type = vt
                    break
            
            return {
                "type": cleaned_type, 
                "confidence": 0.9 if cleaned_type != "unknown" else 0.0, 
                "method": "llm_gemini"
            }
            
        except Exception as e:
            logger.error("LLM Classification failed", error=str(e))
            return {"type": "unknown", "confidence": 0.0, "method": "llm_failed"}
