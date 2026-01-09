import cv2
import numpy as np
import math
from typing import Tuple, Optional
from structlog import get_logger

logger = get_logger()

def compute_skew_angle(image: np.ndarray) -> float:
    """
    Calculate skew angle using Hough Transform on Canny edges.
    """
    try:
        # 1. Convert to grayscale if needed
        if len(image.shape) == 3:
            gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        else:
            gray = image

        # 2. Invert colors (text usually black on white)
        # We need white edges on black background for Canny/Hough
        gray = cv2.bitwise_not(gray)

        # 3. Detect edges
        edges = cv2.Canny(gray, 50, 150, apertureSize=3)

        # 4. Detect lines using Probabilistic Hough Transform
        lines = cv2.HoughLinesP(
            edges, 
            rho=1, 
            theta=np.pi/180, 
            threshold=100, 
            minLineLength=100, 
            maxLineGap=20
        )

        if lines is None:
            logger.warning("No lines detected for deskewing")
            return 0.0

        # 5. Calculate angle for each line
        angles = []
        for line in lines:
            x1, y1, x2, y2 = line[0]
            angle_rad = math.atan2(y2 - y1, x2 - x1)
            angle_deg = math.degrees(angle_rad)
            
            # Filter near-vertical lines (usually margins or tables)
            # We care about horizontal text lines (-45 to 45 degrees usually)
            if -45 < angle_deg < 45:
                 angles.append(angle_deg)

        if not angles:
            return 0.0

        # 6. Median angle is robust to outliers
        median_angle = np.median(angles)
        logger.info("Skew angle detected", angle=median_angle)
        
        return median_angle

    except Exception as e:
        logger.error("Error computing skew", error=str(e))
        return 0.0

def rotate_image(image: np.ndarray, angle: float) -> np.ndarray:
    """
    Rotate image by specific angle.
    """
    if abs(angle) < 0.1:
        return image

    old_height, old_width = image.shape[:2]
    center = (old_width // 2, old_height // 2)
    
    # Rotation matrix
    M = cv2.getRotationMatrix2D(center, angle, 1.0)
    
    # Calculate new bounding box to prevent cropping
    cos = np.abs(M[0, 0])
    sin = np.abs(M[0, 1])
    
    new_width = int((old_height * sin) + (old_width * cos))
    new_height = int((old_height * cos) + (old_width * sin))
    
    # Adjust translation
    M[0, 2] += (new_width / 2) - center[0]
    M[1, 2] += (new_height / 2) - center[1]
    
    rotated = cv2.warpAffine(
        image, 
        M, 
        (new_width, new_height), 
        flags=cv2.INTER_CUBIC, 
        borderMode=cv2.BORDER_REPLICATE
    )
    
    return rotated

def deskew_image(image: np.ndarray) -> np.ndarray:
    """
    Main entry point for deskewing.
    """
    angle = compute_skew_angle(image)
    if angle != 0:
        return rotate_image(image, angle)
    return image
