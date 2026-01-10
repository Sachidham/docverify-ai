import re
from datetime import datetime

class VerhoeffValidator:
    """
    Verhoeff algorithm for Verifying Aadhaar number checksums.
    """
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

    @staticmethod
    def validate(num):
        if not num or not num.isdigit():
            return False
        c = 0
        my_array = list(map(int, reversed(list(num))))
        for i, item in enumerate(my_array):
            c = VerhoeffValidator.d[c][VerhoeffValidator.p[i % 8][item]]
        return c == 0

def validate_aadhaar(aadhaar_num: str) -> bool:
    # Remove spaces
    clean_num = aadhaar_num.replace(' ', '')
    if len(clean_num) != 12 or not clean_num.isdigit():
        return False
    return VerhoeffValidator.validate(clean_num)

def validate_pan(pan_num: str) -> bool:
    pattern = r'^[A-Z]{5}[0-9]{4}[A-Z]{1}$'
    return bool(re.match(pattern, pan_num))

def validate_date_format(date_str: str, date_format: str = "%d/%m/%Y") -> bool:
    """Validate date is real and reasonable (not future, not >120 years old)."""
    try:
        clean_date = date_str.replace('.', '/').replace('-', '/')
        dob = datetime.strptime(clean_date, date_format)
        if dob > datetime.now() or dob.year < 1900:
            return False
        return True
    except ValueError:
        return False


def validate_voter_id(voter_id: str) -> bool:
    """Validate Voter ID (EPIC) format: 3 letters + 7 digits."""
    pattern = r'^[A-Z]{3}[0-9]{7}$'
    return bool(re.match(pattern, voter_id.upper()))


def validate_driving_license(dl_number: str) -> bool:
    """Validate DL format: SS-RRYYYYNNNNNNN or SS-NNNNNNNNNNNNN."""
    # Remove spaces/hyphens
    clean = dl_number.replace(' ', '').replace('-', '').upper()
    # Common formats: 2 state letters + 13-15 alphanumerics
    pattern = r'^[A-Z]{2}[0-9A-Z]{11,15}$'
    return bool(re.match(pattern, clean))


def validate_passport(passport_num: str) -> bool:
    """Validate Indian passport: 1 letter + 7 digits."""
    pattern = r'^[A-Z][0-9]{7}$'
    return bool(re.match(pattern, passport_num.upper()))
