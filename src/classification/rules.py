from typing import Dict, List, Any
from dataclasses import dataclass

@dataclass
class DocumentTemplate:
    name: str
    keywords: List[str]
    regex_patterns: List[str]
    min_keywords: int = 2

# Define templates for Indian documents
DOCUMENT_TEMPLATES: Dict[str, DocumentTemplate] = {
    "aadhaar_card": DocumentTemplate(
        name="Aadhaar Card",
        keywords=[
            "government of india", "mera aadhaar", "unique identification", 
            "father", "dob", "male", "female", "yob"
        ],
        regex_patterns=[
            r"\d{4}\s\d{4}\s\d{4}",  # 12 digit format with spaces
            r"\d{12}"                 # 12 digit raw
        ]
    ),
    "pan_card": DocumentTemplate(
        name="PAN Card",
        keywords=[
            "income tax department", "govt of india", "permanent account number", 
            "signature", "date of birth"
        ],
        regex_patterns=[
            r"[A-Z]{5}[0-9]{4}[A-Z]{1}"  # Standard PAN format
        ]
    ),
    "voter_id": DocumentTemplate(
        name="Voter ID",
        keywords=[
            "election commission of india", "identity card", "elector's name", 
            "sex", "father's name"
        ],
        regex_patterns=[
            r"[A-Z]{3}[0-9]{7}"  # EPIC number format
        ]
    ),
    "driving_license": DocumentTemplate(
        name="Driving License",
        keywords=[
            "driving licence", "union of india", "transport department", 
            "valid till", "authorization to drive"
        ],
        regex_patterns=[
            r"[A-Z]{2}[0-9]{2}\s\d{11}", # New format
            r"[A-Z]{2}-\d{13}"           # Hyphenated
        ]
    )
}
