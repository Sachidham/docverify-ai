import cv2
import numpy as np
from structlog import get_logger

from src.preprocessing.deskew import deskew_image
from src.preprocessing.denoise import denoise_image
from src.preprocessing.enhance import enhance_contrast

logger = get_logger()

class ImagePreprocessor:
    """
    Orchestrates the image preprocessing pipeline.
    """
    
    def __init__(self, config: dict = None):
        self.config = config or {}
        self.do_deskew = self.config.get("deskew", True)
        self.do_denoise = self.config.get("denoise", True)
        self.do_enhance = self.config.get("enhance", True)

    def process_path(self, image_path: str) -> np.ndarray:
        """
        Load image from disk and process.
        """
        logger.info("Loading image for preprocessing", path=image_path)
        image = cv2.imread(image_path)
        if image is None:
            raise ValueError(f"Could not load image at {image_path}")
        return self.process(image)

    def process(self, image: np.ndarray) -> np.ndarray:
        """
        Run the pipeline on an image array.
        """
        processed = image.copy()
        
        # 1. Deskew
        if self.do_deskew:
            processed = deskew_image(processed)
            
        # 2. Denoise
        if self.do_denoise:
            processed = denoise_image(processed)
            
        # 3. Enhance
        if self.do_enhance:
            processed = enhance_contrast(processed)
            
        return processed

    def save_image(self, image: np.ndarray, output_path: str):
        cv2.imwrite(output_path, image)
        logger.info("Saved processed image", path=output_path)

# Helper for quick usage
def process_document(image_path: str, output_path: str = None) -> np.ndarray:
    processor = ImagePreprocessor()
    result = processor.process_path(image_path)
    if output_path:
        processor.save_image(result, output_path)
    return result
