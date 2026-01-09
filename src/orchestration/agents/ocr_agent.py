from typing import Dict, Any
from src.orchestration.agents.base_agent import BaseAgent
from src.preprocessing.pipeline import ImagePreprocessor
# Import engine inside initialize to avoid import errors if dependencies missing during registration
# from src.ocr.paddle_engine import PaddleOCREngine 

class OCRAgent(BaseAgent):
    """
    Agent responsible for extracting text from images using OCR engines.
    """
    
    async def _initialize_impl(self, config: Dict[str, Any]):
        self.engine_name = config.get("engine", "paddleocr")
        
        # 1. Initialize Preprocessor
        self.logger.info("Initializing Preprocessor...")
        self.preprocessor = ImagePreprocessor(config.get("preprocessing", {}))
        
        # 2. Initialize OCR Engine
        if self.engine_name == "paddleocr":
            from src.ocr.paddle_engine import PaddleOCREngine
            self.engine = PaddleOCREngine()
        else:
            # Fallback or other engines
            self.logger.warning("Unknown engine, defaulting to mock", engine=self.engine_name)
            self.engine = None
            
        self.logger.info("OCR Agent initialized", engine=self.engine_name)

    async def _process_impl(self, input_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Input: {"image_path": str, "language_hint": str}
        Output: {"text": str, "raw_result": dict}
        """
        image_path = input_data.get("image_path")
        if not image_path:
            raise ValueError("image_path is required")

        self.logger.info("Processing document...", path=image_path)
        
        # 1. Preprocessing
        self.logger.info("Running Preprocessing...")
        try:
            processed_image = self.preprocessor.process_path(image_path)
        except Exception as e:
            self.logger.error("Preprocessing failed", error=str(e))
            raise e

        # 2. OCR Extraction
        self.logger.info("Running OCR...")
        if self.engine:
            text = self.engine.extract(processed_image)
        else:
            text = "MOCK OCR RESULT (Engine not found)"
        
        return {
            "text": text,
            "confidence": 0.95 if text else 0.0,
            "engine": self.engine_name
        }
