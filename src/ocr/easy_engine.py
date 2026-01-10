"""
DocVerify AI - EasyOCR Engine

Fallback OCR engine using EasyOCR for multi-language support.
"""

import numpy as np
from typing import Optional, List, Tuple
from structlog import get_logger

logger = get_logger()

# Lazy import to avoid loading heavy models at startup
_reader = None


def get_reader(languages: List[str] = None):
    """Get or create EasyOCR reader instance."""
    global _reader
    if _reader is None:
        try:
            import easyocr
            # Default languages: English + Hindi
            langs = languages or ['en', 'hi']
            logger.info("Initializing EasyOCR", languages=langs)
            _reader = easyocr.Reader(langs, gpu=True)
            logger.info("EasyOCR initialized successfully")
        except Exception as e:
            logger.error("Failed to initialize EasyOCR", error=str(e))
            raise
    return _reader


class EasyOCREngine:
    """
    EasyOCR-based text extraction engine.
    Used as fallback when PaddleOCR fails or for ensemble voting.
    """

    def __init__(self, languages: List[str] = None):
        """
        Initialize EasyOCR engine.

        Args:
            languages: List of language codes. Default: ['en', 'hi']
        """
        self.languages = languages or ['en', 'hi']
        self._reader = None

    def _get_reader(self):
        """Lazy load the reader."""
        if self._reader is None:
            self._reader = get_reader(self.languages)
        return self._reader

    def extract(self, image: np.ndarray) -> str:
        """
        Extract text from image.

        Args:
            image: NumPy array of the image (BGR or RGB format)

        Returns:
            Extracted text as string
        """
        try:
            reader = self._get_reader()

            # EasyOCR expects RGB
            if len(image.shape) == 3 and image.shape[2] == 3:
                # Assume BGR from OpenCV, convert to RGB
                import cv2
                image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)

            # Run OCR
            results = reader.readtext(image)

            # Extract text from results
            # Results format: [(bbox, text, confidence), ...]
            text_parts = [result[1] for result in results]
            full_text = ' '.join(text_parts)

            logger.info("EasyOCR extraction complete", char_count=len(full_text))
            return full_text

        except Exception as e:
            logger.error("EasyOCR extraction failed", error=str(e))
            return ""

    def extract_with_confidence(self, image: np.ndarray) -> Tuple[str, float, List[dict]]:
        """
        Extract text with confidence scores and bounding boxes.

        Args:
            image: NumPy array of the image

        Returns:
            Tuple of (full_text, average_confidence, list of detections)
        """
        try:
            reader = self._get_reader()

            # Convert BGR to RGB if needed
            if len(image.shape) == 3 and image.shape[2] == 3:
                import cv2
                image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)

            # Run OCR
            results = reader.readtext(image)

            if not results:
                return "", 0.0, []

            # Process results
            detections = []
            total_confidence = 0.0

            for bbox, text, confidence in results:
                # Convert bbox to standard format
                x_coords = [point[0] for point in bbox]
                y_coords = [point[1] for point in bbox]

                detection = {
                    "text": text,
                    "confidence": confidence,
                    "bbox": {
                        "x": min(x_coords),
                        "y": min(y_coords),
                        "width": max(x_coords) - min(x_coords),
                        "height": max(y_coords) - min(y_coords)
                    }
                }
                detections.append(detection)
                total_confidence += confidence

            # Calculate average confidence
            avg_confidence = total_confidence / len(results) if results else 0.0

            # Build full text
            full_text = ' '.join([d["text"] for d in detections])

            return full_text, avg_confidence, detections

        except Exception as e:
            logger.error("EasyOCR extraction with confidence failed", error=str(e))
            return "", 0.0, []
