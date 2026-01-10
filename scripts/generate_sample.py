from PIL import Image, ImageDraw, ImageFont
import random

def create_sample_aadhaar(output_path="sample_aadhaar.jpg"):
    width = 600
    height = 400
    image = Image.new('RGB', (width, height), color=(255, 255, 255))
    draw = ImageDraw.Draw(image)
    
    # Simple layout
    # Header
    draw.text((20, 20), "GOVERNMENT OF INDIA", fill="black")
    
    # Name
    draw.text((20, 80), "To", fill="black")
    draw.text((20, 100), "Rajesh Kumar", fill="black")
    
    # DOB
    draw.text((20, 140), "DOB: 15/05/1990", fill="black")
    
    # Gender
    draw.text((20, 160), "MALE", fill="black")
    
    # Aadhaar Number
    # Pattern: \d{4}\s\d{4}\s\d{4}
    draw.text((150, 300), "1234 5678 9012", fill="black")
    
    image.save(output_path)
    print(f"Saved sample to {output_path}")

if __name__ == "__main__":
    create_sample_aadhaar()
