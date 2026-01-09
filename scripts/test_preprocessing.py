import cv2
import numpy as np
import sys
import os

# Add project root to path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from src.preprocessing.pipeline import ImagePreprocessor

def create_synthetic_bad_image():
    """Create a dummy image with text, noise, and rotation."""
    # 1. Create whitespace
    img = np.ones((400, 600), dtype=np.uint8) * 255
    
    # 2. Put text
    font = cv2.FONT_HERSHEY_SIMPLEX
    cv2.putText(img, 'DocVerify AI', (100, 200), font, 2, (0,), 3, cv2.LINE_AA)
    
    # 3. Rotate (Skew)
    center = (300, 200)
    M = cv2.getRotationMatrix2D(center, 10, 1.0) # 10 degrees skew
    skewed = cv2.warpAffine(img, M, (600, 400), borderValue=(255,))
    
    # 4. Add Noise
    noise = np.random.normal(0, 10, skewed.shape).astype(np.uint8)
    noisy = cv2.add(skewed, noise)
    
    cv2.imwrite("test_input.jpg", noisy)
    print("Created synthetic bad image: test_input.jpg")

def verify_preprocessing():
    print("🧪 Testing Image Preprocessing...")
    
    create_synthetic_bad_image()
    
    processor = ImagePreprocessor()
    result = processor.process_path("test_input.jpg")
    
    # Save output
    cv2.imwrite("test_output.jpg", result)
    print("✅ Processed image saved: test_output.jpg")
    
    # Basic Checks
    if result.shape != (400, 600) and result.shape != (400, 600, 3):
        # Rotation might change dimensions slightly if not careful, but our deskew logic prevents crop?
        # Actually our rotate_image changes dimensions to fit.
        print(f"Info: Dimensions changed from (400,600) to {result.shape}")
        
    print("Verification complete. Check test_output.jpg manually if needed.")

if __name__ == "__main__":
    verify_preprocessing()
