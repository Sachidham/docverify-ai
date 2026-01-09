import cv2
import numpy as np
from structlog import get_logger

logger = get_logger()

def denoise_image(image: np.ndarray, strength: float = 10.0) -> np.ndarray:
    """
    Remove noise from image using Fast Non-Local Means Denoising.
    """
    try:
        logger.info("Denoising image", strength=strength)
        
        if len(image.shape) == 3:
            # For Color images
            denoised = cv2.fastNlMeansDenoisingColored(
                image, 
                None, 
                h=strength, 
                hColor=strength, 
                templateWindowSize=7, 
                searchWindowSize=21
            )
        else:
            # For Grayscale
            denoised = cv2.fastNlMeansDenoising(
                image, 
                None, 
                h=strength, 
                templateWindowSize=7, 
                searchWindowSize=21
            )
            
        return denoised
    except Exception as e:
        logger.error("Denoising failed", error=str(e))
        return image
