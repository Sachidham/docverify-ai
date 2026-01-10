from typing import Dict, Any, List
from structlog import get_logger
from src.validation.validators import (
    validate_aadhaar, validate_pan, validate_date_format,
    validate_voter_id, validate_driving_license, validate_passport
)

logger = get_logger()

class ValidationEngine:
    """
    Orchestrates validation rules based on document type.
    """
    
    def validate(self, data: Dict[str, Any], doc_type: str) -> Dict[str, Any]:
        logger.info(f"Validating {doc_type}", fields=list(data.keys()))
        
        errors = {}
        warnings = []
        is_valid = True
        
        # 1. Document Specific Validation
        if doc_type == "aadhaar_card":
            if "aadhaar_number" in data:
                print(f"Validating Aadhaar: {data['aadhaar_number']}")
                if not validate_aadhaar(data['aadhaar_number']):
                    errors["aadhaar_number"] = "Invalid Checksum (Verhoeff)"
                    is_valid = False
            else:
                 errors["aadhaar_number"] = "Missing Field"
                 is_valid = False
                 
        elif doc_type == "pan_card":
            if "pan_number" in data:
                if not validate_pan(data['pan_number']):
                    errors["pan_number"] = "Invalid Format"
                    is_valid = False

        elif doc_type == "voter_id":
            if "voter_id_number" in data:
                if not validate_voter_id(data['voter_id_number']):
                    errors["voter_id_number"] = "Invalid Format (expected: ABC1234567)"
                    is_valid = False

        elif doc_type == "driving_license":
            if "dl_number" in data:
                if not validate_driving_license(data['dl_number']):
                    errors["dl_number"] = "Invalid Format"
                    is_valid = False

        elif doc_type == "passport":
            if "passport_number" in data:
                if not validate_passport(data['passport_number']):
                    errors["passport_number"] = "Invalid Format (expected: A1234567)"
                    is_valid = False

        # 2. Common Field Validation
        if "dob" in data:
            if not validate_date_format(data["dob"]):
                warnings.append(f"Invalid DOB format or logical error: {data['dob']}")
                
        return {
            "is_valid": is_valid,
            "errors": errors,
            "warnings": warnings
        }
