"""
DocVerify AI - OCR Module

Multi-engine OCR with ensemble support.
"""

from src.ocr.paddle_engine import PaddleOCREngine
from src.ocr.ensemble import OCREnsemble, OCRResult

__all__ = [
    "PaddleOCREngine",
    "OCREnsemble",
    "OCRResult"
]

# Lazy imports for optional engines
def get_easyocr_engine():
    """Get EasyOCR engine (lazy loaded)."""
    from src.ocr.easy_engine import EasyOCREngine
    return EasyOCREngine
