from paddleocr import PaddleOCR
import numpy as np
from structlog import get_logger

logger = get_logger()

class PaddleOCREngine:
    """
    Wrapper around PaddleOCR for text extraction.
    """
    
    def __init__(self, use_angle_cls: bool = True, lang: str = 'en'):
        logger.info("Initializing PaddleOCR Engine...", lang=lang)
        try:
            # Initialize the OCR model
            # use_gpu=False for broad compatibility unless configured otherwise
            self.ocr = PaddleOCR(use_angle_cls=use_angle_cls, lang=lang, show_log=False)
            logger.info("PaddleOCR initialized successfully")
        except Exception as e:
            logger.error("Failed to initialize PaddleOCR", error=str(e))
            raise e

    def extract(self, image: np.ndarray) -> str:
        """
        Extract text from an image array.
        """
        try:
            logger.info("Running PaddleOCR extraction...")
            # PaddleOCR expects image path or numpy array
            result = self.ocr.ocr(image, cls=True)
            
            if not result or result[0] is None:
                logger.warning("No text detected")
                return ""
            
            # Result format: [[[[x1,y1],[x2,y2]...], ("text", confidence)], ...]
            # We want to combine all text
            extracted_text = []
            for line in result[0]:
                text = line[1][0]
                extracted_text.append(text)
                
            full_text = "\n".join(extracted_text)
            logger.info("OCR Extraction complete", length=len(full_text))
            return full_text
            
        except Exception as e:
            logger.error("OCR extraction failed", error=str(e))
            return ""
