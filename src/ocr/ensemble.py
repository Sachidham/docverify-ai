"""
DocVerify AI - OCR Ensemble

Combines multiple OCR engines for improved accuracy.
"""

import numpy as np
from typing import Optional, List, Dict, Any, Tuple
from dataclasses import dataclass
from structlog import get_logger

from src.ocr.paddle_engine import PaddleOCREngine

logger = get_logger()


@dataclass
class OCRResult:
    """Result from OCR extraction."""
    text: str
    confidence: float
    engine: str
    detections: List[Dict[str, Any]]


class OCREnsemble:
    """
    Ensemble OCR that combines results from multiple engines.

    Strategy:
    1. Run primary engine (PaddleOCR)
    2. If confidence is low, run fallback (EasyOCR)
    3. Return best result or vote on combined results
    """

    def __init__(
        self,
        use_easyocr: bool = True,
        confidence_threshold: float = 0.7,
        languages: List[str] = None
    ):
        """
        Initialize OCR ensemble.

        Args:
            use_easyocr: Whether to use EasyOCR as fallback
            confidence_threshold: Minimum confidence to skip fallback
            languages: Languages to support
        """
        self.confidence_threshold = confidence_threshold
        self.use_easyocr = use_easyocr
        self.languages = languages or ['en', 'hi', 'ta', 'te']

        # Initialize primary engine
        self.paddle_engine = PaddleOCREngine()
        self._easy_engine = None

    def _get_easy_engine(self):
        """Lazy load EasyOCR engine."""
        if self._easy_engine is None and self.use_easyocr:
            try:
                from src.ocr.easy_engine import EasyOCREngine
                # Map to EasyOCR language codes
                easy_langs = []
                lang_map = {'hi': 'hi', 'en': 'en', 'ta': 'ta', 'te': 'te'}
                for lang in self.languages:
                    if lang in lang_map:
                        easy_langs.append(lang_map[lang])
                self._easy_engine = EasyOCREngine(languages=easy_langs or ['en', 'hi'])
            except Exception as e:
                logger.warning("Failed to initialize EasyOCR fallback", error=str(e))
                self._easy_engine = None
        return self._easy_engine

    def extract(self, image: np.ndarray) -> str:
        """
        Extract text using ensemble approach.

        Args:
            image: NumPy array of the image

        Returns:
            Best extracted text
        """
        result = self.extract_with_metadata(image)
        return result.text

    def extract_with_metadata(self, image: np.ndarray) -> OCRResult:
        """
        Extract text with full metadata.

        Args:
            image: NumPy array of the image

        Returns:
            OCRResult with text, confidence, and engine used
        """
        # Try PaddleOCR first (primary)
        paddle_result = self._run_paddle(image)

        # If confidence is high enough, return PaddleOCR result
        if paddle_result.confidence >= self.confidence_threshold:
            logger.info(
                "Using PaddleOCR result (high confidence)",
                confidence=paddle_result.confidence
            )
            return paddle_result

        # Try EasyOCR as fallback
        if self.use_easyocr:
            easy_result = self._run_easyocr(image)

            if easy_result:
                # Compare and return best result
                if easy_result.confidence > paddle_result.confidence:
                    logger.info(
                        "Using EasyOCR result (better confidence)",
                        paddle_conf=paddle_result.confidence,
                        easy_conf=easy_result.confidence
                    )
                    return easy_result

                # If similar confidence, merge/vote
                if abs(easy_result.confidence - paddle_result.confidence) < 0.1:
                    merged = self._merge_results(paddle_result, easy_result)
                    logger.info("Using merged OCR result")
                    return merged

        # Return PaddleOCR result as default
        logger.info("Using PaddleOCR result (default)")
        return paddle_result

    def _run_paddle(self, image: np.ndarray) -> OCRResult:
        """Run PaddleOCR engine."""
        try:
            text = self.paddle_engine.extract(image)

            # Estimate confidence based on text quality
            # (PaddleOCR confidence extraction would need engine modification)
            confidence = self._estimate_confidence(text)

            return OCRResult(
                text=text,
                confidence=confidence,
                engine="paddleocr",
                detections=[]
            )

        except Exception as e:
            logger.error("PaddleOCR failed", error=str(e))
            return OCRResult(text="", confidence=0.0, engine="paddleocr", detections=[])

    def _run_easyocr(self, image: np.ndarray) -> Optional[OCRResult]:
        """Run EasyOCR engine."""
        try:
            easy_engine = self._get_easy_engine()
            if not easy_engine:
                return None

            text, confidence, detections = easy_engine.extract_with_confidence(image)

            return OCRResult(
                text=text,
                confidence=confidence,
                engine="easyocr",
                detections=detections
            )

        except Exception as e:
            logger.error("EasyOCR failed", error=str(e))
            return None

    def _estimate_confidence(self, text: str) -> float:
        """
        Estimate confidence based on text characteristics.
        This is a heuristic when actual confidence is not available.
        """
        if not text:
            return 0.0

        confidence = 0.5  # Base confidence

        # Boost for longer text
        if len(text) > 100:
            confidence += 0.1
        if len(text) > 500:
            confidence += 0.1

        # Boost for having numbers (documents usually have IDs)
        if any(c.isdigit() for c in text):
            confidence += 0.1

        # Boost for having uppercase letters (document headers)
        if any(c.isupper() for c in text):
            confidence += 0.05

        # Penalize for too many special characters (noise)
        special_ratio = sum(1 for c in text if not c.isalnum() and not c.isspace()) / len(text)
        if special_ratio > 0.3:
            confidence -= 0.2

        return min(max(confidence, 0.0), 1.0)

    def _merge_results(self, result1: OCRResult, result2: OCRResult) -> OCRResult:
        """
        Merge results from multiple engines.
        Currently uses simple longest-text strategy.
        Future: implement voting or LLM-based merging.
        """
        # Use the result with more text (usually more complete)
        if len(result2.text) > len(result1.text) * 1.2:
            primary = result2
            secondary = result1
        else:
            primary = result1
            secondary = result2

        # Average confidence
        avg_confidence = (result1.confidence + result2.confidence) / 2

        return OCRResult(
            text=primary.text,
            confidence=avg_confidence,
            engine=f"ensemble({primary.engine}+{secondary.engine})",
            detections=primary.detections + secondary.detections
        )
