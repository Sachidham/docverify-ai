import cv2
import numpy as np
from structlog import get_logger

logger = get_logger()

def enhance_contrast(image: np.ndarray, clip_limit: float = 2.0) -> np.ndarray:
    """
    Enhance local contrast using CLAHE.
    """
    try:
        logger.info("Enhancing contrast", clip_limit=clip_limit)
        
        # Determine color space
        if len(image.shape) == 3:
            # Convert to LAB color space
            lab = cv2.cvtColor(image, cv2.COLOR_BGR2LAB)
            l, a, b = cv2.split(lab)
            
            # Apply CLAHE to L-channel
            clahe = cv2.createCLAHE(clipLimit=clip_limit, tileGridSize=(8, 8))
            cl = clahe.apply(l)
            
            # Merge and convert back
            limg = cv2.merge((cl, a, b))
            final = cv2.cvtColor(limg, cv2.COLOR_LAB2BGR)
        else:
            # Grayscale directly
            clahe = cv2.createCLAHE(clipLimit=clip_limit, tileGridSize=(8, 8))
            final = clahe.apply(image)
            
        return final

    except Exception as e:
        logger.error("Contrast enhancement failed", error=str(e))
        return image
