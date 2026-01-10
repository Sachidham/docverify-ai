import re

class DocumentPatterns:
    """
    Regex patterns for Indian official documents.
    """
    
    # Common Patterns
    DATE_PATTERN = r'\b(\d{2}[-/.]\d{2}[-/.]\d{4})\b'
    GENDER_PATTERN = r'\b(MALE|FEMALE|TRANSGENDER|पुरुष|महिला)\b'
    
    AADHAAR = {
        "aadhaar_number": r'\b(\d{4}\s\d{4}\s\d{4}|\d{12})\b',
        "dob": DATE_PATTERN,
        "gender": GENDER_PATTERN,
        # Improved name extraction heuristics can be added here or in the engine
        # "name": r"To\s+([A-Z][a-zA-Z\s]+)" 
    }
    
    PAN = {
        "pan_number": r'\b([A-Z]{5}\d{4}[A-Z])\b',
        "dob": DATE_PATTERN,
        "name": r'\b([A-Z\s]+)\b' # Placeholder, context-sensitive extraction is better
    }
    
    VOTER_ID = {
        "voter_id_number": r'\b([A-Z]{3}\d{7})\b',
        "age": r'\bAge\s*[:=\-]?\s*(\d{2})\b'
    }
    
    DRIVING_LICENSE = {
        "dl_number": r'\b([A-Z]{2}[-\d\s/]+)\b',
        "valid_upto": r'(?:Valid till|Valid Upto)\s*[:=\-]?\s*(\d{2}[-/.]\d{2}[-/.]\d{4})'
    }
    
    PASSPORT = {
        "passport_number": r'\b([A-Z]\d{7})\b',
        "dob": DATE_PATTERN,
        "surname": r'Surname\s*[:=\-]?\s*([A-Z\s]+)',
        "given_name": r'Given Name\s*[:=\-]?\s*([A-Z\s]+)'
    }
    
    BIRTH_CERTIFICATE = {
        "registration_number": r'(?:Registration|Birth)\s*No\.?\s*[:=\-]?\s*(\d+)',
        "child_name": r'(?:Name of Child|Child\'s Name)\s*[:=\-]?\s*([A-Za-z\s]+)',
        "dob": DATE_PATTERN,
        "place_of_birth": r'(?:Place of Birth)\s*[:=\-]?\s*([A-Za-z\s,]+)',
        "father_name": r'(?:Father\'s Name|Name of Father)\s*[:=\-]?\s*([A-Za-z\s]+)',
        "mother_name": r'(?:Mother\'s Name|Name of Mother)\s*[:=\-]?\s*([A-Za-z\s]+)'
    }

    @staticmethod
    def get_patterns(doc_type: str):
        mapping = {
            "aadhaar_card": DocumentPatterns.AADHAAR,
            "pan_card": DocumentPatterns.PAN,
            "voter_id": DocumentPatterns.VOTER_ID,
            "driving_license": DocumentPatterns.DRIVING_LICENSE,
            "passport": DocumentPatterns.PASSPORT,
            "birth_certificate": DocumentPatterns.BIRTH_CERTIFICATE
        }
        return mapping.get(doc_type, {})
