"""
Lightweight Tesseract OCR Engine for deployment environments.
No PyTorch/PaddlePaddle dependency - uses system Tesseract binary.
"""
import numpy as np
from structlog import get_logger
from PIL import Image

logger = get_logger()


class TesseractOCREngine:
    """
    Lightweight OCR using Tesseract (no heavy ML frameworks needed).
    Used in deployment/free-tier environments where PaddleOCR is too heavy.
    """

    def __init__(self, lang: str = "eng"):
        logger.info("Initializing Tesseract OCR Engine...", lang=lang)
        try:
            import pytesseract
            self.pytesseract = pytesseract
            self.lang = lang
            # Test that tesseract binary is available
            pytesseract.get_tesseract_version()
            logger.info("Tesseract OCR initialized successfully")
        except Exception as e:
            logger.error("Failed to initialize Tesseract", error=str(e))
            raise e

    def extract(self, image: np.ndarray) -> str:
        """Extract text from an image array using Tesseract."""
        try:
            logger.info("Running Tesseract OCR extraction...")
            pil_image = Image.fromarray(image)
            text = self.pytesseract.image_to_string(pil_image, lang=self.lang)
            text = text.strip()
            logger.info("Tesseract extraction complete", length=len(text))
            return text
        except Exception as e:
            logger.error("Tesseract extraction failed", error=str(e))
            return ""
