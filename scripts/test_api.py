import sys
import os

# Add src to path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from fastapi.testclient import TestClient
from src.api.main import app


def run_tests():
    with TestClient(app) as client:
        # 1. Health
        response = client.get("/health")
        assert response.status_code == 200
        print("Health Check:", response.json())
        
        # 2. Verify
        if os.path.exists("valid_aadhaar.jpg"):
             print(f"Testing verify with valid_aadhaar.jpg...")
             with open("valid_aadhaar.jpg", "rb") as f:
                response = client.post(
                    "/api/v1/verify",
                    files={"file": ("test_doc.jpg", f, "image/jpeg")}
                )
             print("Status Code:", response.status_code)
             print("Response:", response.json())
        else:
             print("Skipping detailed verification test: valid_aadhaar.jpg not found")

if __name__ == "__main__":
    print("--- Running API Tests ---")
    run_tests()
