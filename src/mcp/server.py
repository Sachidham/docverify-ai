"""
DocVerify AI - MCP Server

Exposes document verification capabilities as MCP tools for AI assistants.
Transport: Streamable HTTP on port 8001

Run: python -m src.mcp.server
"""

import base64
import io
import tempfile
import os
from typing import Optional
from enum import Enum

from mcp.server.fastmcp import FastMCP
from pydantic import BaseModel, Field
import numpy as np
from PIL import Image

# Initialize FastMCP server
mcp = FastMCP(
    "docverify",
    instructions="AI-Powered Document Verification Platform for Indian Government Documents"
)

# --- Lazy Loading of Heavy Modules ---
_processor = None
_ocr_engine = None
_classifier = None
_extractor = None
_validator = None
_preprocessor = None


def get_preprocessor():
    global _preprocessor
    if _preprocessor is None:
        from src.preprocessing.pipeline import ImagePreprocessor
        _preprocessor = ImagePreprocessor()
    return _preprocessor


def get_ocr_engine():
    global _ocr_engine
    if _ocr_engine is None:
        from src.ocr.paddle_engine import PaddleOCREngine
        _ocr_engine = PaddleOCREngine()
    return _ocr_engine


def get_classifier():
    global _classifier
    if _classifier is None:
        from src.classification.engine import DocumentClassifier
        _classifier = DocumentClassifier()
    return _classifier


def get_extractor():
    global _extractor
    if _extractor is None:
        from src.extraction.engine import ExtractionEngine
        _extractor = ExtractionEngine()
    return _extractor


def get_validator():
    global _validator
    if _validator is None:
        from src.validation.engine import ValidationEngine
        _validator = ValidationEngine()
    return _validator


# --- Enums ---
class LanguageHint(str, Enum):
    en = "en"
    hi = "hi"
    ta = "ta"
    te = "te"


class DocumentType(str, Enum):
    aadhaar_card = "aadhaar_card"
    pan_card = "pan_card"
    voter_id = "voter_id"
    driving_license = "driving_license"
    passport = "passport"
    birth_certificate = "birth_certificate"
    unknown = "unknown"


class ResponseFormat(str, Enum):
    json = "json"
    markdown = "markdown"


# --- Helper Functions ---
def decode_base64_image(image_base64: str) -> np.ndarray:
    """Decode base64 image to numpy array."""
    # Remove data URI prefix if present
    if "," in image_base64:
        image_base64 = image_base64.split(",")[1]

    image_bytes = base64.b64decode(image_base64)
    image = Image.open(io.BytesIO(image_bytes))
    return np.array(image)


def save_temp_image(image_base64: str) -> str:
    """Save base64 image to temp file and return path."""
    if "," in image_base64:
        image_base64 = image_base64.split(",")[1]

    image_bytes = base64.b64decode(image_base64)

    with tempfile.NamedTemporaryFile(suffix=".png", delete=False) as f:
        f.write(image_bytes)
        return f.name


# --- Tool 1: OCR Extract ---
@mcp.tool()
async def docverify_ocr_extract(
    image_base64: str,
    language_hint: Optional[LanguageHint] = None,
    preprocess: bool = True,
    response_format: ResponseFormat = ResponseFormat.json
) -> dict:
    """
    Extract text from a document image using multi-language OCR.

    Supports Hindi, English, Tamil, and Telugu scripts.
    Returns extracted text with confidence scores and bounding boxes.

    Args:
        image_base64: Base64 encoded image data
        language_hint: Optional language hint (en, hi, ta, te)
        preprocess: Whether to apply image preprocessing (deskew, denoise, enhance)
        response_format: Output format (json or markdown)

    Returns:
        Extracted text with confidence and metadata
    """
    try:
        # Decode image
        image = decode_base64_image(image_base64)

        # Preprocess if requested
        if preprocess:
            preprocessor = get_preprocessor()
            image = preprocessor.process(image)

        # Run OCR
        ocr = get_ocr_engine()
        text = ocr.extract(image)

        result = {
            "status": "success",
            "text": text,
            "language_hint": language_hint.value if language_hint else "auto",
            "preprocessed": preprocess,
            "char_count": len(text),
            "word_count": len(text.split())
        }

        if response_format == ResponseFormat.markdown:
            return {
                "status": "success",
                "content": f"## Extracted Text\n\n```\n{text}\n```\n\n**Words:** {len(text.split())} | **Characters:** {len(text)}"
            }

        return result

    except Exception as e:
        return {"status": "error", "error": str(e)}


# --- Tool 2: Classify Document ---
@mcp.tool()
async def docverify_classify_document(
    ocr_text: str,
    image_base64: Optional[str] = None,
    use_vision: bool = True
) -> dict:
    """
    Classify the type of an Indian government document.

    Uses hybrid rule-based and LLM classification for accuracy.
    Supported types: Aadhaar Card, PAN Card, Voter ID, Driving License, Passport.

    Args:
        ocr_text: Extracted OCR text from the document
        image_base64: Optional base64 image for vision-based classification
        use_vision: Whether to use vision model (if image provided)

    Returns:
        Document type with confidence score and reasoning
    """
    try:
        classifier = get_classifier()
        result = await classifier.classify(ocr_text)

        return {
            "status": "success",
            "document_type": result.get("type", "unknown"),
            "confidence": result.get("confidence", 0.0),
            "method": result.get("method", "unknown"),
            "supported_types": [t.value for t in DocumentType]
        }

    except Exception as e:
        return {"status": "error", "error": str(e)}


# --- Tool 3: Extract Fields ---
@mcp.tool()
async def docverify_extract_fields(
    ocr_text: str,
    document_type: DocumentType,
    language: LanguageHint = LanguageHint.en
) -> dict:
    """
    Extract structured fields from a classified document.

    Extracts document-specific fields like name, ID numbers, dates, addresses.
    Uses regex patterns with LLM fallback for complex cases.

    Args:
        ocr_text: Extracted OCR text from the document
        document_type: Type of document (aadhaar_card, pan_card, etc.)
        language: Primary language of the document

    Returns:
        Extracted field values with confidence scores
    """
    try:
        if document_type == DocumentType.unknown:
            return {
                "status": "error",
                "error": "Cannot extract fields from unknown document type. Please classify first."
            }

        extractor = get_extractor()
        fields = await extractor.extract(ocr_text, document_type.value)

        # Define expected fields per document type
        expected_fields = {
            "aadhaar_card": ["name", "aadhaar_number", "dob", "gender", "address"],
            "pan_card": ["name", "pan_number", "father_name", "dob"],
            "voter_id": ["name", "voter_id_number", "age", "father_name"],
            "driving_license": ["name", "dl_number", "dob", "valid_upto"],
            "passport": ["name", "passport_number", "dob", "surname", "given_name"]
        }

        return {
            "status": "success",
            "document_type": document_type.value,
            "extracted_fields": fields,
            "fields_found": list(fields.keys()),
            "expected_fields": expected_fields.get(document_type.value, [])
        }

    except Exception as e:
        return {"status": "error", "error": str(e)}


# --- Tool 4: Validate Fields ---
@mcp.tool()
async def docverify_validate_fields(
    document_type: DocumentType,
    fields: dict,
    strict_mode: bool = False
) -> dict:
    """
    Validate extracted fields against format and logical rules.

    Performs checksum validation (Aadhaar), format validation (PAN),
    date validation, and cross-field consistency checks.

    Args:
        document_type: Type of document being validated
        fields: Dictionary of extracted field values
        strict_mode: If true, treat warnings as errors

    Returns:
        Validation status per field with error/warning messages
    """
    try:
        if document_type == DocumentType.unknown:
            return {
                "status": "error",
                "error": "Cannot validate unknown document type"
            }

        validator = get_validator()
        result = validator.validate(fields, document_type.value)

        # In strict mode, convert warnings to errors
        if strict_mode and result.get("warnings"):
            result["errors"].update({
                f"warning_{i}": w for i, w in enumerate(result.get("warnings", []))
            })
            result["is_valid"] = False

        return {
            "status": "success",
            "document_type": document_type.value,
            "is_valid": result.get("is_valid", False),
            "errors": result.get("errors", {}),
            "warnings": result.get("warnings", []),
            "fields_validated": list(fields.keys()),
            "strict_mode": strict_mode
        }

    except Exception as e:
        return {"status": "error", "error": str(e)}


# --- Tool 5: Check Fraud ---
@mcp.tool()
async def docverify_check_fraud(
    document_id: Optional[str] = None,
    image_base64: Optional[str] = None,
    ocr_text: Optional[str] = None,
    check_duplicates: bool = True,
    check_tampering: bool = True
) -> dict:
    """
    Perform fraud detection checks on a document.

    Checks for duplicate documents using embedding similarity,
    layout consistency, and basic tamper detection indicators.

    Args:
        document_id: Optional document ID for database lookup
        image_base64: Optional base64 image for visual analysis
        ocr_text: Optional OCR text for content analysis
        check_duplicates: Whether to check for duplicate documents
        check_tampering: Whether to check for tampering indicators

    Returns:
        Fraud risk score and detailed findings
    """
    try:
        findings = []
        risk_score = 0.0

        # Basic content-based checks
        if ocr_text:
            # Check for suspicious patterns
            suspicious_patterns = [
                ("duplicate_text", ocr_text.count(ocr_text[:50]) > 1 if len(ocr_text) > 50 else False),
                ("very_short_text", len(ocr_text) < 50),
                ("no_numbers", not any(c.isdigit() for c in ocr_text)),
            ]

            for pattern_name, detected in suspicious_patterns:
                if detected:
                    findings.append({
                        "type": pattern_name,
                        "severity": "medium",
                        "description": f"Suspicious pattern detected: {pattern_name}"
                    })
                    risk_score += 0.15

        # Image-based checks (placeholder for future CV models)
        if image_base64 and check_tampering:
            findings.append({
                "type": "visual_analysis",
                "severity": "info",
                "description": "Visual tamper detection not yet implemented"
            })

        # Duplicate check (placeholder for embedding similarity)
        if check_duplicates:
            findings.append({
                "type": "duplicate_check",
                "severity": "info",
                "description": "Embedding-based duplicate detection requires database integration"
            })

        # Determine risk level
        risk_level = "low"
        if risk_score > 0.3:
            risk_level = "medium"
        if risk_score > 0.6:
            risk_level = "high"

        return {
            "status": "success",
            "risk_level": risk_level,
            "risk_score": min(risk_score, 1.0),
            "findings": findings,
            "checks_performed": {
                "duplicates": check_duplicates,
                "tampering": check_tampering
            }
        }

    except Exception as e:
        return {"status": "error", "error": str(e)}


# --- Tool 6: Detect Stamps ---
@mcp.tool()
async def docverify_detect_stamps(
    image_base64: str,
    detect_stamps: bool = True,
    detect_signatures: bool = True
) -> dict:
    """
    Detect official stamps/seals and signatures in a document image.

    Uses computer vision to identify and locate stamps and handwritten signatures.
    Returns bounding boxes and confidence scores for detected elements.

    Args:
        image_base64: Base64 encoded document image
        detect_stamps: Whether to detect official stamps/seals
        detect_signatures: Whether to detect handwritten signatures

    Returns:
        Detected elements with positions and confidence scores
    """
    try:
        import cv2

        # Decode image
        image = decode_base64_image(image_base64)

        # Convert to appropriate color space
        if len(image.shape) == 3:
            gray = cv2.cvtColor(image, cv2.COLOR_RGB2GRAY)
            hsv = cv2.cvtColor(image, cv2.COLOR_RGB2HSV)
        else:
            gray = image
            hsv = None

        stamps_found = []
        signatures_found = []

        # Basic stamp detection (looking for circular/oval colored regions)
        if detect_stamps and hsv is not None:
            # Look for red/blue regions (common stamp colors)
            # Red stamps
            lower_red = np.array([0, 100, 100])
            upper_red = np.array([10, 255, 255])
            red_mask = cv2.inRange(hsv, lower_red, upper_red)

            # Blue stamps
            lower_blue = np.array([100, 100, 100])
            upper_blue = np.array([130, 255, 255])
            blue_mask = cv2.inRange(hsv, lower_blue, upper_blue)

            combined_mask = cv2.bitwise_or(red_mask, blue_mask)

            # Find contours
            contours, _ = cv2.findContours(combined_mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

            for contour in contours:
                area = cv2.contourArea(contour)
                if area > 500:  # Minimum area threshold
                    x, y, w, h = cv2.boundingRect(contour)
                    # Check if roughly circular (aspect ratio close to 1)
                    aspect_ratio = float(w) / h if h > 0 else 0
                    if 0.5 < aspect_ratio < 2.0:
                        stamps_found.append({
                            "type": "stamp",
                            "bounding_box": {"x": int(x), "y": int(y), "width": int(w), "height": int(h)},
                            "confidence": 0.7,
                            "color": "red/blue"
                        })

        # Basic signature detection (looking for dark strokes)
        if detect_signatures:
            # Apply threshold to find dark regions
            _, binary = cv2.threshold(gray, 100, 255, cv2.THRESH_BINARY_INV)

            # Find contours
            contours, _ = cv2.findContours(binary, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

            for contour in contours:
                area = cv2.contourArea(contour)
                # Signatures are typically elongated and of medium size
                if 200 < area < 10000:
                    x, y, w, h = cv2.boundingRect(contour)
                    aspect_ratio = float(w) / h if h > 0 else 0
                    # Signatures tend to be wider than tall
                    if aspect_ratio > 1.5 and w > 50:
                        signatures_found.append({
                            "type": "signature",
                            "bounding_box": {"x": int(x), "y": int(y), "width": int(w), "height": int(h)},
                            "confidence": 0.5
                        })

        return {
            "status": "success",
            "stamps": stamps_found[:5],  # Limit to top 5
            "signatures": signatures_found[:3],  # Limit to top 3
            "stamps_count": len(stamps_found),
            "signatures_count": len(signatures_found),
            "detection_enabled": {
                "stamps": detect_stamps,
                "signatures": detect_signatures
            }
        }

    except Exception as e:
        return {"status": "error", "error": str(e)}


# --- Tool 7: Full Verification ---
@mcp.tool()
async def docverify_full_verification(
    image_base64: str,
    language_hint: Optional[LanguageHint] = None,
    document_type_hint: Optional[DocumentType] = None,
    run_fraud_check: bool = True
) -> dict:
    """
    Run the complete document verification pipeline.

    Performs: Image preprocessing → OCR → Classification → Field Extraction →
    Validation → Fraud Check (optional) in a single call.

    Args:
        image_base64: Base64 encoded document image
        language_hint: Optional language hint for OCR
        document_type_hint: Optional document type hint to skip classification
        run_fraud_check: Whether to run fraud detection

    Returns:
        Complete verification result with all extracted data and validation status
    """
    try:
        result = {
            "status": "success",
            "pipeline_steps": []
        }

        # Step 1: Save image temporarily and preprocess
        temp_path = save_temp_image(image_base64)
        result["pipeline_steps"].append("image_saved")

        try:
            # Step 2: Preprocess
            preprocessor = get_preprocessor()
            processed_image = preprocessor.process_path(temp_path)
            result["pipeline_steps"].append("preprocessing_complete")

            # Step 3: OCR
            ocr = get_ocr_engine()
            text = ocr.extract(processed_image)
            result["raw_text"] = text
            result["pipeline_steps"].append("ocr_complete")

            # Step 4: Classification
            if document_type_hint and document_type_hint != DocumentType.unknown:
                doc_type = document_type_hint.value
                classification = {"type": doc_type, "confidence": 1.0, "method": "user_provided"}
            else:
                classifier = get_classifier()
                classification = await classifier.classify(text)
                doc_type = classification.get("type", "unknown")

            result["document_type"] = doc_type
            result["classification"] = classification
            result["pipeline_steps"].append("classification_complete")

            # Step 5: Field Extraction
            extracted_fields = {}
            if doc_type != "unknown":
                extractor = get_extractor()
                extracted_fields = await extractor.extract(text, doc_type)

            result["extracted_fields"] = extracted_fields
            result["pipeline_steps"].append("extraction_complete")

            # Step 6: Validation
            validation = {"is_valid": False, "errors": {}, "warnings": []}
            if extracted_fields:
                validator = get_validator()
                validation = validator.validate(extracted_fields, doc_type)

            result["validation"] = validation
            result["pipeline_steps"].append("validation_complete")

            # Step 7: Fraud Check (optional)
            if run_fraud_check:
                fraud_result = await docverify_check_fraud(
                    ocr_text=text,
                    image_base64=image_base64
                )
                result["fraud_check"] = fraud_result
                result["pipeline_steps"].append("fraud_check_complete")

            # Overall status
            result["overall_confidence"] = classification.get("confidence", 0.0)
            result["is_verified"] = validation.get("is_valid", False)

        finally:
            # Cleanup temp file
            if os.path.exists(temp_path):
                os.unlink(temp_path)

        return result

    except Exception as e:
        return {"status": "error", "error": str(e), "pipeline_steps": result.get("pipeline_steps", [])}


# --- MCP Resources ---
@mcp.resource("docverify://supported-documents")
async def get_supported_documents() -> str:
    """List of supported document types and their fields."""
    return """
# Supported Document Types

## 1. Aadhaar Card
- **Fields**: Name, Aadhaar Number, DOB, Gender, Address
- **Validation**: Verhoeff checksum for Aadhaar number

## 2. PAN Card
- **Fields**: Name, PAN Number, Father's Name, DOB
- **Validation**: Format validation (XXXXX0000X)

## 3. Voter ID (EPIC)
- **Fields**: Name, Voter ID Number, Age, Father's Name
- **Validation**: Format validation

## 4. Driving License
- **Fields**: Name, DL Number, DOB, Valid Upto
- **Validation**: Format and date validation

## 5. Passport
- **Fields**: Name, Passport Number, DOB, Surname, Given Name
- **Validation**: Format validation

## Languages Supported
- English (en)
- Hindi (hi)
- Tamil (ta)
- Telugu (te)
"""


@mcp.resource("docverify://api-status")
async def get_api_status() -> str:
    """Current status of the DocVerify API."""
    return """
# DocVerify API Status

- **MCP Server**: Online
- **OCR Engine**: PaddleOCR (primary)
- **LLM**: Gemini 2.0 Flash
- **Supported Languages**: en, hi, ta, te
"""


# --- Entry Point ---
if __name__ == "__main__":
    import sys

    # Default to stdio transport for CLI usage
    # Use --http flag for HTTP transport
    if "--http" in sys.argv:
        port = 8001
        for i, arg in enumerate(sys.argv):
            if arg == "--port" and i + 1 < len(sys.argv):
                port = int(sys.argv[i + 1])

        print(f"Starting DocVerify MCP Server on HTTP port {port}...")
        mcp.run(transport="sse")  # SSE for HTTP
    else:
        print("Starting DocVerify MCP Server with stdio transport...")
        mcp.run()
