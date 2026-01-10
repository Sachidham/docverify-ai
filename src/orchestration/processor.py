import cv2
import numpy as np
from structlog import get_logger
from typing import Dict, Any

from src.ocr.paddle_engine import PaddleOCREngine
from src.classification.engine import DocumentClassifier
from src.extraction.engine import ExtractionEngine
from src.preprocessing.pipeline import ImagePreprocessor
from src.validation.engine import ValidationEngine

logger = get_logger()

class DocumentProcessor:
    """
    Orchestrates the full document verification pipeline.
    Image -> Preprocess -> OCR -> Classify -> Extract -> Validate
    """
    
    def __init__(self):
        logger.info("Initializing Document Processor...")
        try:
            self.preprocessor = ImagePreprocessor()
            self.ocr = PaddleOCREngine()
            self.classifier = DocumentClassifier()
            self.extractor = ExtractionEngine()
            self.validator = ValidationEngine()
            logger.info("Document Processor initialized successfully")
        except Exception as e:
            logger.error("Failed to initialize Document Processor", error=str(e))
            raise e

    async def process(self, image_path: str) -> Dict[str, Any]:
        """
        Process a document from file path.
        """
        try:
            logger.info("Starting processing", path=image_path)
            
            # 1. Load & Preprocess
            # ImagePreprocessor handles loading and full pipeline
            processed_image = self.preprocessor.process_path(image_path)
            
            # 2. OCR
            text = self.ocr.extract(processed_image)
            logger.info("OCR Text extracted", snippet=text[:100])
            
            # 3. Classification
            classification = await self.classifier.classify(text)
            doc_type = classification.get("type", "unknown")
            logger.info("Document Classified", doc_type=doc_type)
            
            # 4. Extraction
            extracted_data = {}
            if doc_type != "unknown":
                extracted_data = await self.extractor.extract(text, doc_type)
            
            # 5. Validation
            validation_result = {}
            if extracted_data:
                validation_result = self.validator.validate(extracted_data, doc_type)
                logger.info("Validation complete", valid=validation_result.get("is_valid"))
                
            result = {
                "status": "success",
                "document_type": doc_type,
                "confidence": classification.get("confidence", 0.0),
                "extracted_fields": extracted_data,
                "validation": validation_result,
                "raw_text": text,
                "classification_method": classification.get("method", "unknown")
            }
            return result
            
        except Exception as e:
            logger.error("Processing failed", error=str(e))
            return {
                "status": "failed",
                "error": str(e)
            }
