"""
DocVerify AI - OCR Module

Multi-engine OCR with ensemble support.
All imports are lazy to support lightweight deployment (Tesseract-only mode).
"""


def get_paddle_engine():
    """Get PaddleOCR engine (lazy loaded)."""
    from src.ocr.paddle_engine import PaddleOCREngine
    return PaddleOCREngine


def get_easyocr_engine():
    """Get EasyOCR engine (lazy loaded)."""
    from src.ocr.easy_engine import EasyOCREngine
    return EasyOCREngine


def get_tesseract_engine():
    """Get Tesseract engine (lazy loaded)."""
    from src.ocr.tesseract_engine import TesseractOCREngine
    return TesseractOCREngine
