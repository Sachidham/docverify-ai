"""
Generate realistic synthetic sample documents for testing DocVerify AI.
Creates: Aadhaar Card, PAN Card, Voter ID, Driving License, Passport
"""
from PIL import Image, ImageDraw, ImageFont
import os
import sys

OUTPUT_DIR = os.path.join(os.path.dirname(os.path.dirname(__file__)), "synthetic_data", "samples")
os.makedirs(OUTPUT_DIR, exist_ok=True)

# Verhoeff algorithm for valid Aadhaar numbers
VERHOEFF_D = [
    [0,1,2,3,4,5,6,7,8,9],[1,2,3,4,0,6,7,8,9,5],
    [2,3,4,0,1,7,8,9,5,6],[3,4,0,1,2,8,9,5,6,7],
    [4,0,1,2,3,9,5,6,7,8],[5,9,8,7,6,0,4,3,2,1],
    [6,5,9,8,7,1,0,4,3,2],[7,6,5,9,8,2,1,0,4,3],
    [8,7,6,5,9,3,2,1,0,4],[9,8,7,6,5,4,3,2,1,0]
]
VERHOEFF_P = [
    [0,1,2,3,4,5,6,7,8,9],[1,5,7,6,2,8,3,0,9,4],
    [5,8,0,3,7,9,6,1,4,2],[8,9,1,6,0,4,3,5,2,7],
    [9,4,5,3,1,2,6,8,7,0],[4,2,8,6,5,7,3,9,0,1],
    [2,7,9,3,8,0,6,4,1,5],[7,0,4,6,9,1,3,2,5,8]
]
VERHOEFF_INV = [0,4,3,2,1,5,6,7,8,9]

def verhoeff_checksum(num_str):
    c = 0
    for i, digit in enumerate(reversed(list(num_str))):
        c = VERHOEFF_D[c][VERHOEFF_P[(i+1) % 8][int(digit)]]
    return VERHOEFF_INV[c]


def try_load_font(size):
    """Try to load a font, fall back to default."""
    font_paths = [
        "/System/Library/Fonts/Helvetica.ttc",
        "/System/Library/Fonts/SFNSText.ttf",
        "/Library/Fonts/Arial.ttf",
        "/System/Library/Fonts/Supplemental/Arial.ttf",
    ]
    for fp in font_paths:
        try:
            return ImageFont.truetype(fp, size)
        except (OSError, IOError):
            continue
    return ImageFont.load_default()


def try_load_bold_font(size):
    """Try to load a bold font."""
    font_paths = [
        "/System/Library/Fonts/Helvetica.ttc",
        "/Library/Fonts/Arial Bold.ttf",
        "/System/Library/Fonts/Supplemental/Arial Bold.ttf",
    ]
    for fp in font_paths:
        try:
            return ImageFont.truetype(fp, size)
        except (OSError, IOError):
            continue
    return try_load_font(size)


def draw_rounded_rect(draw, xy, radius, fill, outline=None):
    """Draw a rounded rectangle."""
    x0, y0, x1, y1 = xy
    draw.rounded_rectangle(xy, radius=radius, fill=fill, outline=outline)


def create_aadhaar_card():
    """Create a realistic Aadhaar card sample."""
    w, h = 850, 540
    img = Image.new('RGB', (w, h), '#FFFFFF')
    draw = ImageDraw.Draw(img)

    # Orange header bar
    draw.rectangle([0, 0, w, 70], fill='#FF6600')

    # Title
    title_font = try_load_bold_font(22)
    small_font = try_load_font(14)
    name_font = try_load_bold_font(20)
    field_font = try_load_font(16)
    num_font = try_load_bold_font(28)
    hindi_font = try_load_font(13)

    draw.text((20, 10), "GOVERNMENT OF INDIA", fill='white', font=title_font)
    draw.text((20, 40), "भारत सरकार", fill='white', font=small_font)

    # Aadhaar logo text
    draw.text((w - 250, 10), "aadhaar", fill='white', font=try_load_bold_font(30))
    draw.text((w - 250, 45), "आधार", fill='white', font=small_font)

    # Green line
    draw.rectangle([0, 70, w, 75], fill='#138808')

    # Photo placeholder
    draw.rectangle([30, 100, 200, 310], fill='#E8E8E8', outline='#AAAAAA')
    draw.text((70, 195), "PHOTO", fill='#888888', font=field_font)

    # Name
    draw.text((230, 100), "Name / नाम", fill='#666666', font=small_font)
    draw.text((230, 120), "Rajesh Kumar", fill='#000000', font=name_font)
    draw.text((230, 145), "राजेश कुमार", fill='#333333', font=field_font)

    # DOB
    draw.text((230, 180), "Date of Birth / जन्म तिथि", fill='#666666', font=small_font)
    draw.text((230, 200), "15/05/1990", fill='#000000', font=field_font)

    # Gender
    draw.text((500, 180), "Gender / लिंग", fill='#666666', font=small_font)
    draw.text((500, 200), "Male / पुरुष", fill='#000000', font=field_font)

    # Address
    draw.text((230, 240), "Address / पता", fill='#666666', font=small_font)
    draw.text((230, 260), "S/O: Suresh Kumar", fill='#000000', font=field_font)
    draw.text((230, 280), "42, Gandhi Nagar, Sector 15", fill='#000000', font=field_font)
    draw.text((230, 300), "New Delhi - 110001", fill='#000000', font=field_font)
    draw.text((230, 320), "Delhi, India", fill='#000000', font=field_font)

    # QR code placeholder
    draw.rectangle([30, 330, 170, 470], fill='#E0E0E0', outline='#AAAAAA')
    draw.text((65, 395), "QR CODE", fill='#888888', font=small_font)

    # Aadhaar number with valid Verhoeff checksum
    prefix = "49812365701"
    check = verhoeff_checksum(prefix)
    aadhaar_num = prefix + str(check)
    formatted_num = f"{aadhaar_num[:4]} {aadhaar_num[4:8]} {aadhaar_num[8:]}"

    # Number bar
    draw.rectangle([0, 480, w, 540], fill='#FF6600')
    draw.text((w//2 - 120, 490), formatted_num, fill='white', font=num_font)

    # VID text
    draw.text((30, 495), "VID: 8765 4321 0987 6543", fill='white', font=small_font)

    path = os.path.join(OUTPUT_DIR, "sample_aadhaar.jpg")
    img.save(path, quality=92)
    print(f"Created: {path} (Aadhaar: {formatted_num})")
    return path


def create_pan_card():
    """Create a realistic PAN card sample."""
    w, h = 850, 540
    img = Image.new('RGB', (w, h), '#FEFDF5')
    draw = ImageDraw.Draw(img)

    title_font = try_load_bold_font(18)
    name_font = try_load_bold_font(20)
    field_font = try_load_font(15)
    small_font = try_load_font(13)
    pan_font = try_load_bold_font(26)

    # Blue header
    draw.rectangle([0, 0, w, 80], fill='#1A3C6B')

    # Emblem placeholder
    draw.ellipse([20, 10, 60, 60], fill='#D4AF37', outline='#B8960C')
    draw.text((28, 25), "IN", fill='#1A3C6B', font=try_load_bold_font(16))

    draw.text((80, 8), "INCOME TAX DEPARTMENT", fill='#D4AF37', font=title_font)
    draw.text((80, 30), "आयकर विभाग", fill='#D4AF37', font=small_font)
    draw.text((80, 50), "GOVT. OF INDIA", fill='#D4AF37', font=small_font)

    # PAN Card Title
    draw.text((w - 300, 15), "Permanent Account Number Card", fill='#D4AF37', font=field_font)
    draw.text((w - 300, 35), "स्थायी खाता संख्या कार्ड", fill='#D4AF37', font=small_font)

    # Subtle background pattern
    draw.rectangle([0, 80, w, h], fill='#FEFDF5')

    # Photo placeholder
    draw.rectangle([w - 210, 120, w - 40, 310], fill='#E8E8E8', outline='#AAAAAA')
    draw.text((w - 170, 205), "PHOTO", fill='#888888', font=field_font)

    # PAN Number
    pan_number = "ABCPK1234Z"
    draw.text((40, 110), "Permanent Account Number / स्थायी खाता संख्या", fill='#666666', font=small_font)
    draw.text((40, 135), pan_number, fill='#1A3C6B', font=pan_font)

    # Name
    draw.text((40, 190), "Name / नाम", fill='#666666', font=small_font)
    draw.text((40, 210), "RAJESH KUMAR", fill='#000000', font=name_font)

    # Father's name
    draw.text((40, 260), "Father's Name / पिता का नाम", fill='#666666', font=small_font)
    draw.text((40, 280), "SURESH KUMAR", fill='#000000', font=name_font)

    # DOB
    draw.text((40, 330), "Date of Birth / जन्म तिथि", fill='#666666', font=small_font)
    draw.text((40, 350), "15/05/1990", fill='#000000', font=field_font)

    # Signature area
    draw.rectangle([40, 410, 250, 470], fill='#F5F5E8', outline='#CCCCAA')
    draw.text((80, 430), "Signature", fill='#999999', font=small_font)

    # Bottom bar
    draw.rectangle([0, 490, w, 540], fill='#1A3C6B')
    draw.text((w//2 - 80, 503), pan_number, fill='#D4AF37', font=pan_font)

    path = os.path.join(OUTPUT_DIR, "sample_pan.jpg")
    img.save(path, quality=92)
    print(f"Created: {path} (PAN: {pan_number})")
    return path


def create_voter_id():
    """Create a realistic Voter ID (EPIC) card sample."""
    w, h = 850, 540
    img = Image.new('RGB', (w, h), '#FFFFFF')
    draw = ImageDraw.Draw(img)

    title_font = try_load_bold_font(18)
    name_font = try_load_bold_font(18)
    field_font = try_load_font(15)
    small_font = try_load_font(13)
    id_font = try_load_bold_font(22)

    # Red/maroon header
    draw.rectangle([0, 0, w, 75], fill='#8B0000')

    # Emblem
    draw.ellipse([15, 8, 60, 58], fill='#D4AF37', outline='#B8960C')
    draw.text((25, 22), "ECI", fill='#8B0000', font=try_load_bold_font(14))

    draw.text((75, 8), "ELECTION COMMISSION OF INDIA", fill='white', font=title_font)
    draw.text((75, 30), "भारत निर्वाचन आयोग", fill='#FFD700', font=small_font)
    draw.text((75, 50), "ELECTOR'S PHOTO IDENTITY CARD", fill='#FFD700', font=small_font)

    # Photo
    draw.rectangle([30, 100, 200, 310], fill='#E8E8E8', outline='#AAAAAA')
    draw.text((70, 195), "PHOTO", fill='#888888', font=field_font)

    # EPIC Number
    epic_number = "ABC1234567"
    draw.text((230, 100), "EPIC No. / मतदाता फोटो पहचान पत्र सं.", fill='#666666', font=small_font)
    draw.text((230, 122), epic_number, fill='#8B0000', font=id_font)

    # Name
    draw.text((230, 165), "Elector's Name / निर्वाचक का नाम", fill='#666666', font=small_font)
    draw.text((230, 185), "Priya Sharma", fill='#000000', font=name_font)

    # Father's Name
    draw.text((230, 220), "Father's Name / पिता का नाम", fill='#666666', font=small_font)
    draw.text((230, 240), "Ramesh Sharma", fill='#000000', font=name_font)

    # DOB
    draw.text((230, 275), "Date of Birth / जन्म तिथि", fill='#666666', font=small_font)
    draw.text((230, 295), "22/08/1985", fill='#000000', font=field_font)

    # Gender
    draw.text((500, 275), "Sex / लिंग", fill='#666666', font=small_font)
    draw.text((500, 295), "Female / महिला", fill='#000000', font=field_font)

    # Address
    draw.text((230, 330), "Address / पता", fill='#666666', font=small_font)
    draw.text((230, 350), "H.No. 45, Rajpur Road", fill='#000000', font=field_font)
    draw.text((230, 370), "Dehradun, Uttarakhand - 248001", fill='#000000', font=field_font)

    # Assembly / Parliamentary
    draw.text((30, 420), "AC No & Name: 001 - Central Delhi", fill='#333333', font=field_font)
    draw.text((30, 445), "PC No & Name: 01 - New Delhi", fill='#333333', font=field_font)

    # Bottom bar
    draw.rectangle([0, 490, w, 540], fill='#8B0000')
    draw.text((w//2 - 60, 505), epic_number, fill='white', font=id_font)

    path = os.path.join(OUTPUT_DIR, "sample_voter_id.jpg")
    img.save(path, quality=92)
    print(f"Created: {path} (EPIC: {epic_number})")
    return path


def create_driving_license():
    """Create a realistic Driving License sample."""
    w, h = 850, 540
    img = Image.new('RGB', (w, h), '#F5F8FF')
    draw = ImageDraw.Draw(img)

    title_font = try_load_bold_font(18)
    name_font = try_load_bold_font(18)
    field_font = try_load_font(14)
    small_font = try_load_font(12)
    dl_font = try_load_bold_font(22)

    # Blue header
    draw.rectangle([0, 0, w, 70], fill='#003366')

    # Emblem
    draw.ellipse([15, 8, 55, 55], fill='#D4AF37')
    draw.text((23, 22), "IN", fill='#003366', font=try_load_bold_font(14))

    draw.text((70, 8), "UNION OF INDIA - DRIVING LICENCE", fill='white', font=title_font)
    draw.text((70, 32), "भारत संघ - ड्राइविंग लाइसेंस", fill='#87CEEB', font=small_font)
    draw.text((70, 50), "TRANSPORT DEPARTMENT", fill='#87CEEB', font=small_font)

    # Photo
    draw.rectangle([w - 200, 90, w - 40, 280], fill='#E8E8E8', outline='#AAAAAA')
    draw.text((w - 165, 175), "PHOTO", fill='#888888', font=field_font)

    # DL Number
    dl_number = "DL-0420110012345"
    draw.text((30, 85), "DL No. / लाइसेंस सं.", fill='#666666', font=small_font)
    draw.text((30, 105), dl_number, fill='#003366', font=dl_font)

    # Name
    draw.text((30, 145), "Name / नाम", fill='#666666', font=small_font)
    draw.text((30, 163), "AMIT VERMA", fill='#000000', font=name_font)

    # S/D/W of
    draw.text((30, 195), "S/D/W of / पिता/पति का नाम", fill='#666666', font=small_font)
    draw.text((30, 213), "VIJAY VERMA", fill='#000000', font=field_font)

    # DOB
    draw.text((30, 245), "DOB / जन्म तिथि", fill='#666666', font=small_font)
    draw.text((30, 263), "10/03/1988", fill='#000000', font=field_font)

    # Blood Group
    draw.text((300, 245), "Blood Group / रक्त समूह", fill='#666666', font=small_font)
    draw.text((300, 263), "B+", fill='#CC0000', font=name_font)

    # Address
    draw.text((30, 295), "Address / पता", fill='#666666', font=small_font)
    draw.text((30, 313), "56, MG Road, Connaught Place", fill='#000000', font=field_font)
    draw.text((30, 333), "New Delhi - 110001, Delhi", fill='#000000', font=field_font)

    # Issue / Validity
    draw.text((30, 370), "Date of Issue / जारी तिथि", fill='#666666', font=small_font)
    draw.text((30, 388), "15/01/2020", fill='#000000', font=field_font)

    draw.text((300, 370), "Valid Till / वैधता", fill='#666666', font=small_font)
    draw.text((300, 388), "14/01/2040", fill='#000000', font=field_font)

    # Vehicle classes
    draw.text((30, 420), "Authorisation to Drive / वाहन श्रेणी", fill='#666666', font=small_font)
    draw.rectangle([30, 440, 550, 480], fill='#E8EDF5', outline='#BBBBDD')
    draw.text((40, 448), "MCWG    LMV    TRANS", fill='#003366', font=name_font)

    # Bottom bar
    draw.rectangle([0, 495, w, 540], fill='#003366')
    draw.text((w//2 - 100, 508), dl_number, fill='white', font=dl_font)

    path = os.path.join(OUTPUT_DIR, "sample_driving_license.jpg")
    img.save(path, quality=92)
    print(f"Created: {path} (DL: {dl_number})")
    return path


def create_passport():
    """Create a realistic Indian Passport first page sample."""
    w, h = 850, 600
    img = Image.new('RGB', (w, h), '#1A1A4E')
    draw = ImageDraw.Draw(img)

    title_font = try_load_bold_font(22)
    name_font = try_load_bold_font(18)
    field_font = try_load_font(14)
    small_font = try_load_font(12)
    passport_font = try_load_bold_font(22)

    # Dark navy background with inner lighter area
    draw.rectangle([20, 20, w-20, h-20], fill='#F5F5EE', outline='#1A1A4E', width=3)

    # Header
    draw.rectangle([20, 20, w-20, 100], fill='#1A1A4E')

    # Emblem
    draw.ellipse([w//2 - 25, 30, w//2 + 25, 85], fill='#D4AF37')
    draw.text((w//2 - 10, 48), "IN", fill='#1A1A4E', font=try_load_bold_font(16))

    draw.text((40, 35), "REPUBLIC OF INDIA", fill='#D4AF37', font=title_font)
    draw.text((40, 65), "भारत गणराज्य", fill='#D4AF37', font=field_font)

    draw.text((w - 200, 35), "PASSPORT", fill='#D4AF37', font=title_font)
    draw.text((w - 200, 65), "पासपोर्ट", fill='#D4AF37', font=field_font)

    # Photo
    draw.rectangle([40, 120, 230, 340], fill='#E8E8E8', outline='#AAAAAA')
    draw.text((90, 220), "PHOTO", fill='#888888', font=field_font)

    # Type / Country Code / Passport No
    passport_no = "M1234567"
    draw.text((260, 120), "Type / प्रकार", fill='#666666', font=small_font)
    draw.text((260, 138), "P", fill='#000000', font=name_font)

    draw.text((360, 120), "Country Code / देश कोड", fill='#666666', font=small_font)
    draw.text((360, 138), "IND", fill='#000000', font=name_font)

    draw.text((530, 120), "Passport No. / पासपोर्ट सं.", fill='#666666', font=small_font)
    draw.text((530, 138), passport_no, fill='#1A1A4E', font=passport_font)

    # Surname
    draw.text((260, 180), "Surname / उपनाम", fill='#666666', font=small_font)
    draw.text((260, 198), "PATEL", fill='#000000', font=name_font)

    # Given Names
    draw.text((260, 230), "Given Name(s) / दिया गया नाम", fill='#666666', font=small_font)
    draw.text((260, 248), "ANANYA", fill='#000000', font=name_font)

    # Nationality
    draw.text((260, 285), "Nationality / राष्ट्रीयता", fill='#666666', font=small_font)
    draw.text((260, 303), "INDIAN", fill='#000000', font=field_font)

    # Sex
    draw.text((530, 285), "Sex / लिंग", fill='#666666', font=small_font)
    draw.text((530, 303), "F", fill='#000000', font=field_font)

    # DOB
    draw.text((260, 335), "Date of Birth / जन्म तिथि", fill='#666666', font=small_font)
    draw.text((260, 353), "25/12/1995", fill='#000000', font=field_font)

    # Place of Birth
    draw.text((530, 335), "Place of Birth / जन्म स्थान", fill='#666666', font=small_font)
    draw.text((530, 353), "AHMEDABAD", fill='#000000', font=field_font)

    # Date of Issue
    draw.text((260, 385), "Date of Issue / जारी तिथि", fill='#666666', font=small_font)
    draw.text((260, 403), "01/06/2022", fill='#000000', font=field_font)

    # Date of Expiry
    draw.text((530, 385), "Date of Expiry / समाप्ति तिथि", fill='#666666', font=small_font)
    draw.text((530, 403), "31/05/2032", fill='#000000', font=field_font)

    # Place of Issue
    draw.text((260, 435), "Place of Issue / जारी करने का स्थान", fill='#666666', font=small_font)
    draw.text((260, 453), "AHMEDABAD", fill='#000000', font=field_font)

    # Address
    draw.text((40, 360), "Address / पता", fill='#666666', font=small_font)
    draw.text((40, 378), "12 Satellite Road", fill='#000000', font=small_font)
    draw.text((40, 396), "Ahmedabad 380015", fill='#000000', font=small_font)
    draw.text((40, 414), "Gujarat, India", fill='#000000', font=small_font)

    # MRZ zone
    draw.rectangle([20, 500, w-20, h-20], fill='#EDEDDF')
    mrz_font = try_load_font(14)
    draw.text((40, 515), "P<INDPATEL<<ANANYA<<<<<<<<<<<<<<<<<<<<<<<<<<<", fill='#000000', font=mrz_font)
    draw.text((40, 545), "M1234567<6IND9512250F3205310<<<<<<<<<<<<<<<04", fill='#000000', font=mrz_font)

    path = os.path.join(OUTPUT_DIR, "sample_passport.jpg")
    img.save(path, quality=92)
    print(f"Created: {path} (Passport: {passport_no})")
    return path


def create_birth_certificate():
    """Create a realistic Birth Certificate sample."""
    w, h = 850, 700
    img = Image.new('RGB', (w, h), '#FFFFF5')
    draw = ImageDraw.Draw(img)

    title_font = try_load_bold_font(22)
    subtitle_font = try_load_bold_font(16)
    name_font = try_load_bold_font(18)
    field_font = try_load_font(15)
    small_font = try_load_font(13)
    value_font = try_load_font(16)

    # Decorative border
    draw.rectangle([10, 10, w-10, h-10], outline='#8B4513', width=3)
    draw.rectangle([20, 20, w-20, h-20], outline='#D2691E', width=1)

    # Header with emblem
    draw.ellipse([w//2 - 30, 35, w//2 + 30, 100], fill='#D4AF37', outline='#B8960C')
    draw.text((w//2 - 15, 55), "IN", fill='#333', font=try_load_bold_font(18))

    draw.text((w//2 - 180, 110), "GOVERNMENT OF INDIA", fill='#8B0000', font=title_font)
    draw.text((w//2 - 100, 140), "भारत सरकार", fill='#8B0000', font=subtitle_font)

    draw.text((w//2 - 100, 175), "BIRTH CERTIFICATE", fill='#003366', font=title_font)
    draw.text((w//2 - 65, 205), "जन्म प्रमाण पत्र", fill='#003366', font=subtitle_font)

    draw.text((w//2 - 170, 235), "(Issued under Section 12 of Registration of", fill='#666666', font=small_font)
    draw.text((w//2 - 120, 255), "Births and Deaths Act, 1969)", fill='#666666', font=small_font)

    # Horizontal line
    draw.line([(40, 280), (w-40, 280)], fill='#8B4513', width=2)

    # Registration Number
    draw.text((50, 300), "Registration No.:", fill='#333333', font=subtitle_font)
    draw.text((230, 300), "2020/BC/001245", fill='#000000', font=value_font)

    # Name of Child
    y = 340
    draw.text((50, y), "1. Name of Child / बच्चे का नाम:", fill='#333333', font=field_font)
    draw.text((330, y), "ARJUN SINGH", fill='#000000', font=name_font)

    # Sex
    y += 40
    draw.text((50, y), "2. Sex / लिंग:", fill='#333333', font=field_font)
    draw.text((330, y), "Male / पुरुष", fill='#000000', font=value_font)

    # Date of Birth
    y += 40
    draw.text((50, y), "3. Date of Birth / जन्म तिथि:", fill='#333333', font=field_font)
    draw.text((330, y), "10/03/2020", fill='#000000', font=value_font)

    # Place of Birth
    y += 40
    draw.text((50, y), "4. Place of Birth / जन्म स्थान:", fill='#333333', font=field_font)
    draw.text((330, y), "Civil Hospital, Jaipur, Rajasthan", fill='#000000', font=value_font)

    # Father's Name
    y += 40
    draw.text((50, y), "5. Father's Name / पिता का नाम:", fill='#333333', font=field_font)
    draw.text((330, y), "MAHENDRA SINGH", fill='#000000', font=value_font)

    # Mother's Name
    y += 40
    draw.text((50, y), "6. Mother's Name / माता का नाम:", fill='#333333', font=field_font)
    draw.text((330, y), "SUNITA DEVI", fill='#000000', font=value_font)

    # Address
    y += 40
    draw.text((50, y), "7. Address / पता:", fill='#333333', font=field_font)
    draw.text((330, y), "23, Malviya Nagar, Jaipur - 302017", fill='#000000', font=value_font)
    draw.text((330, y+20), "Rajasthan, India", fill='#000000', font=value_font)

    # Date of Registration
    y += 65
    draw.text((50, y), "Date of Registration:", fill='#333333', font=field_font)
    draw.text((230, y), "15/03/2020", fill='#000000', font=value_font)

    draw.text((450, y), "Date of Issue:", fill='#333333', font=field_font)
    draw.text((580, y), "20/03/2020", fill='#000000', font=value_font)

    # Signature and stamp area
    draw.line([(40, y+45), (w-40, y+45)], fill='#8B4513', width=1)

    # Stamp placeholder
    draw.ellipse([w-220, y+55, w-100, y+130], outline='#CC0000', width=2)
    draw.text((w-195, y+80), "OFFICIAL\n  SEAL", fill='#CC0000', font=small_font)

    # Signature
    draw.text((50, y+70), "Registrar:", fill='#333333', font=field_font)
    draw.text((50, y+95), "___________________", fill='#333333', font=field_font)
    draw.text((50, y+115), "(Authorized Signatory)", fill='#666666', font=small_font)

    path = os.path.join(OUTPUT_DIR, "sample_birth_certificate.jpg")
    img.save(path, quality=92)
    print(f"Created: {path}")
    return path


if __name__ == "__main__":
    print("=" * 60)
    print("Generating synthetic sample documents for DocVerify AI")
    print("=" * 60)

    paths = []
    paths.append(create_aadhaar_card())
    paths.append(create_pan_card())
    paths.append(create_voter_id())
    paths.append(create_driving_license())
    paths.append(create_passport())
    paths.append(create_birth_certificate())

    print("\n" + "=" * 60)
    print(f"Generated {len(paths)} sample documents in:")
    print(f"  {OUTPUT_DIR}")
    print("=" * 60)
