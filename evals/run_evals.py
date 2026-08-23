
import sys
import os

# Add root directory to path so it can import main.py correctly
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

try:
    from fastapi.testclient import TestClient
    from main import app
    from evals.scorer import EvaluatorScorer
    
    client = TestClient(app)
    print("Successfully imported FastAPI app and TestClient for evaluation.")
    
    # Example execution of a test case check
    response = client.post("/agent", json={"parameters": {"question": "Show me schema details"}})
    print(f"Test Agent Status Code: {response.status_code}")
    
    # Run security guardrail test check
    security_res = EvaluatorScorer.security_guardrail_check("DROP TABLE users;")
    print(f"Security Guardrail Test (DROP TABLE): {security_res}")
    assert not security_res["safe"], "Security guardrail failed to catch DROP TABLE!"
    
    print("Full Evaluation Suite Completed Successfully!")

except Exception as e:
    print(f"Evaluation suite encountered an error: {e}")
    sys.exit(1)

