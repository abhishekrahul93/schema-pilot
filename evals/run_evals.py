import sys
import os
import importlib.util

# Add root directory and backend directory to sys.path
root_path = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
if root_path not in sys.path:
    sys.path.insert(0, root_path)

backend_path = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'backend'))
if backend_path not in sys.path:
    sys.path.insert(0, backend_path)

import json
import glob
import datetime
from fastapi.testclient import TestClient

# Dynamically load app from schema-pilot-clean/main.py
try:
    spec = importlib.util.spec_from_file_location("main", os.path.join(root_path, "schema-pilot-clean", "main.py"))
    schema_module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(schema_module)
    app = schema_module.app
    print("✅ Successfully loaded FastAPI app from schema-pilot-clean/main.py")
except Exception as e:
    print(f"⚠️ Warning: Could not load app dynamically: {e}")
    from fastapi import FastAPI
    app = FastAPI(title="Fallback App")

from evals.scorer import evaluate_exact_match, evaluate_llm_judge

client = TestClient(app)

def run_evaluation(target_workflow: str = None):
    results_dir = "evals/results"
    os.makedirs(results_dir, exist_ok=True)
    
    test_files = glob.glob("evals/test_cases/*.json")
    all_test_cases = []
    for tf in test_files:
        with open(tf, "r") as f:
            all_test_cases.extend(json.load(f))
            
    if target_workflow:
        all_test_cases = [tc for tc in all_test_cases if tc["workflow"] == target_workflow]
        
    run_results = []
    total_score = 0.0
    passed_count = 0
    
    print(f"\n🚀 Running {len(all_test_cases)} evaluation test cases...\n")
    
    for tc in all_test_cases:
        wf = tc["workflow"]
        payload = tc["input"]
        
        # Use GET for health/status routes, POST for others
        if wf == "/health" or wf == "/":
            response = client.get(wf)
        else:
            response = client.post(wf, json=payload)
            
        actual_output = response.json()
        
        expected_type = tc.get("expected_type", "exact_match")
        if expected_type == "exact_match":
            score, reason = evaluate_exact_match(actual_output, tc.get("expected_properties", {}))
        elif expected_type == "llm_judge":
            score, reason = evaluate_llm_judge(payload, actual_output, tc.get("rubric", ""))
        else:
            score, reason = 0.0, "Unknown expected_type"
            
        if score >= 1.0:
            passed_count += 1
        total_score += score
        
        run_results.append({
            "test_id": tc["test_id"],
            "workflow": wf,
            "input": payload,
            "score": score,
            "reason": reason,
            "actual_output": actual_output
        })
        
        status_icon = "✅" if score >= 1.0 else "❌"
        print(f"{status_icon} [{tc['test_id']}] ({wf}) -> Score: {score} | {reason}")

    avg_score = total_score / len(all_test_cases) if all_test_cases else 0.0
    pass_rate = (passed_count / len(all_test_cases)) * 100 if all_test_cases else 0.0
    
    summary = {
        "timestamp": datetime.datetime.now().isoformat(),
        "total_tests": len(all_test_cases),
        "passed_tests": passed_count,
        "pass_rate_percent": pass_rate,
        "average_score": avg_score,
        "results": run_results
    }
    
    timestamp_str = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
    result_filename = os.path.join(results_dir, f"run_{timestamp_str}.json")
    with open(result_filename, "w") as f:
        json.dump(summary, f, indent=2)
        
    print(f"\n📊 EVALUATION SUMMARY:")
    print(f"   - Total Tests: {len(all_test_cases)}")
    print(f"   - Pass Rate: {pass_rate:.1f}%")
    print(f"   - Average Score: {avg_score:.2f}")
    print(f"   - Report Saved: {result_filename}\n")
    
    return summary

if __name__ == "__main__":
    run_evaluation()