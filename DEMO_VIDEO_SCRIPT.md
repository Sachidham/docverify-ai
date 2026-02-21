# DocVerify AI - Demo Video Script

**Target Duration:** 3-5 minutes
**Tool:** Loom, OBS, or QuickTime screen recording

---

## Scene 1: Introduction (30 seconds)

**Show:** The Streamlit dashboard landing page

**Say:**
> "Hi, I'm [Your Name]. This is DocVerify AI - an AI-powered document verification platform built for Indian government services. It can verify Aadhaar cards, PAN cards, Voter IDs, Driving Licenses, Passports, and Birth Certificates using multi-engine OCR and LLM-powered intelligence."

**Action:** Scroll through the sidebar showing supported documents and "System Online" status.

---

## Scene 2: Document Upload & Verification (90 seconds)

### 2a. Aadhaar Card Verification

**Say:**
> "Let me start with an Aadhaar card verification."

**Action:**
1. Click "Browse files" in the upload area
2. Upload `synthetic_data/samples/sample_aadhaar.jpg`
3. Show the document preview on the left
4. Click "Verify Now" button
5. Show the progress animation (uploading → OCR → validating)
6. Walk through the results:
   - Document type detected: "Aadhaar Card"
   - Confidence score
   - Extracted fields (Name, DOB, Gender, Aadhaar Number, Address)
   - Validation results (Verhoeff checksum pass/fail)
7. Click "View Raw API Response" to show the full JSON

**Say:**
> "The system preprocesses the image, runs multi-engine OCR using PaddleOCR and EasyOCR, classifies the document type, extracts all fields, and validates them - including the Verhoeff checksum that Aadhaar uses. All in under 10 seconds."

### 2b. PAN Card Verification

**Action:**
1. Upload `synthetic_data/samples/sample_pan.jpg`
2. Click Verify Now
3. Show results with PAN format validation

**Say:**
> "Same pipeline works for PAN cards - it detects the document type, extracts the PAN number, name, and validates the PAN format."

---

## Scene 3: API Documentation (30 seconds)

**Action:** Open browser tab to `http://localhost:8000/docs`

**Say:**
> "The backend is a FastAPI REST API with full Swagger documentation. You can upload documents, run verification, standalone OCR, classification, and get analytics - all through the API."

**Action:** Briefly scroll through the endpoints.

---

## Scene 4: Architecture Overview (30 seconds)

**Show:** The architecture diagram from PRD or a quick whiteboard

**Say:**
> "Under the hood, the architecture uses:
> - Multi-engine OCR with PaddleOCR and EasyOCR in an ensemble
> - Google Gemini 2.0 Flash for intelligent classification and extraction
> - Rule-based validation with Verhoeff checksums and format checks
> - A FastAPI backend with Streamlit frontend
> - And an MCP server that exposes 7 tools for AI assistant integration
>
> All running at zero API cost using free tiers."

---

## Scene 5: History & Analytics (20 seconds)

**Action:**
1. Switch to "History" tab - show the list of verified documents
2. Switch to "Analytics" tab - show metrics (total documents, verifications, success rate)

**Say:**
> "The dashboard also tracks verification history and provides analytics on processing volumes and success rates."

---

## Scene 6: Closing (20 seconds)

**Say:**
> "DocVerify AI was built in 15 days as a capstone project for 100xEngineers. It supports 6 document types, 4 languages, and processes documents in under 10 seconds.
>
> Check out the GitHub repo for the full source code. Thank you!"

**Show:** GitHub repo URL on screen

---

## Recording Tips

1. **Screen resolution:** Set to 1920x1080 for crisp recording
2. **Browser:** Use Chrome/Firefox in clean mode (no bookmarks bar, no extensions)
3. **Tabs:** Have pre-loaded: Streamlit UI, API docs, GitHub repo
4. **Sample files:** Have all 6 sample documents ready in the file picker
5. **Audio:** Use a quiet room, speak clearly
6. **Pace:** Don't rush - let the verification animations play out
7. **If errors occur:** It's okay! Explain what happened and retry

## Quick Checklist Before Recording

- [ ] FastAPI server running (`http://localhost:8000/health` returns online)
- [ ] Streamlit UI running (`http://localhost:8501`)
- [ ] Sample documents ready in `synthetic_data/samples/`
- [ ] Google API key configured (if showing LLM features)
- [ ] Screen recording tool ready
- [ ] Microphone working
