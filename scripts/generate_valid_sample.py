from PIL import Image, ImageDraw, ImageFont
import random

def create_valid_aadhaar(output_path="valid_aadhaar.jpg"):
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
    
    # DOB (Valid Format)
    draw.text((20, 140), "DOB: 15/05/1990", fill="black")
    
    # Gender
    draw.text((20, 160), "MALE", fill="black")
    
    # Aadhaar Number (Verhoeff VALID)
    # 9999 1111 0008 is a valid Verhoeff number (I pre-calculated or know 9999-9999-9999 is valid? NO.)
    # Let's use a known valid one for testing: 3675 9834 2201 
    # Actually, Verhoeff is tricky. I'll use a number I can construct or assume 
    # Let's generate one code snippet to calculate a valid one if needed, but for now 
    # I'll use a placeholder that SHOULD fail if I don't calculate it right.
    # Actually, let's reverse compute a checksum. 
    # Let's just use '1234 5678 9012' -> Fails.
    # I'll try to use a valid one: 9999 9999 0019 (Checksum of 99999999001 is 9)
    # Wait, I'll write a quick script to find a valid one then put it here.
    
    # Let's assume for this Agent run I will trust the Validator logic is correct (it passed invalid).
    # I will try to bruteforce a digest or just pick one.
    # 2085 4319 2244 is valid? I don't know. 
    # Let's use a simpler known valid number from online examples or calculate it.
    # Valid Verhoeff: 2343 2432 4324 (Maybe)
    
    # BETTER: I will calculate the check digit for '20000000000' in the code below
    
    # ... Wait, I'll finding a valid one via code is easier.
    # Implementation of Verhoeff to find check digit
    d = [
        [0, 1, 2, 3, 4, 5, 6, 7, 8, 9],
        [1, 2, 3, 4, 0, 6, 7, 8, 9, 5],
        [2, 3, 4, 0, 1, 7, 8, 9, 5, 6],
        [3, 4, 0, 1, 2, 8, 9, 5, 6, 7],
        [4, 0, 1, 2, 3, 9, 5, 6, 7, 8],
        [5, 9, 8, 7, 6, 0, 4, 3, 2, 1],
        [6, 5, 9, 8, 7, 1, 0, 4, 3, 2],
        [7, 6, 5, 9, 8, 2, 1, 0, 4, 3],
        [8, 7, 6, 5, 9, 3, 2, 1, 0, 4],
        [9, 8, 7, 6, 5, 4, 3, 2, 1, 0]
    ]
    p = [
        [0, 1, 2, 3, 4, 5, 6, 7, 8, 9],
        [1, 5, 7, 6, 2, 8, 3, 0, 9, 4],
        [5, 8, 0, 3, 7, 9, 6, 1, 4, 2],
        [8, 9, 1, 6, 0, 4, 3, 5, 2, 7],
        [9, 4, 5, 3, 1, 2, 6, 8, 7, 0],
        [4, 2, 8, 6, 5, 7, 3, 9, 0, 1],
        [2, 7, 9, 3, 8, 0, 6, 4, 1, 5],
        [7, 0, 4, 6, 9, 1, 3, 2, 5, 8]
    ]
    inv = [0, 4, 3, 2, 1, 5, 6, 7, 8, 9]

    def calc(num):
        c = 0
        my_array = list(map(int, reversed(list(num))))
        for i, item in enumerate(my_array):
            c = d[c][p[(i + 1) % 8][item]]
        return inv[c]

    # Prefix 11 digits
    prefix = "99998888777" 
    checksum = calc(prefix)
    valid_num = prefix + str(checksum)
    formatted = f"{valid_num[:4]} {valid_num[4:8]} {valid_num[8:]}"
    print(f"Generated Valid Number: {formatted}")
    
    draw.text((150, 300), formatted, fill="black")
    
    image.save(output_path)
    print(f"Saved sample to {output_path}")

if __name__ == "__main__":
    create_valid_aadhaar()
