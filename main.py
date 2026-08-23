import os
import sys
import traceback
import uvicorn
from fastapi import FastAPI, Request
from fastapi.staticfiles import StaticFiles
from fastapi.responses import HTMLResponse
from pydantic import BaseModel, Field
from typing import Optional, Dict, Any

# Ensure backend directory is in sys.path so internal imports work from any execution root
backend_dir = os.path.dirname(os.path.abspath(__file__))
if backend_dir not in sys.path:
    sys.path.insert(0, backend_dir)

app = FastAPI(title="SchemaPilot API", version="1.0.0")

class AgentRequestPayload(BaseModel):
    test_mode: Optional[bool] = True
    custom_schema: Optional[str] = Field(default="default", max_length=50)
    parameters: Optional[Dict[str, Any]] = None

# Safely import modules individually with fallback paths
agent = multi_agent = multi_agent_audited = multi_agent_healing = extract_metadata = extract_alt_metadata = evaluate = None

try:
    import agent
except Exception:
    try:
        from backend import agent
    except Exception:
        agent = None

try:
    import multi_agent
except Exception:
    try:
        from backend import multi_agent
    except Exception:
        multi_agent = None

try:
    import multi_agent_audited
except Exception:
    try:
        from backend import multi_agent_audited
    except Exception:
        multi_agent_audited = None

try:
    import multi_agent_healing
except Exception:
    try:
        from backend import multi_agent_healing
    except Exception:
        multi_agent_healing = None

try:
    import extract_metadata
except Exception:
    try:
        from backend import extract_metadata
    except Exception:
        extract_metadata = None

try:
    import extract_alt_metadata
except Exception:
    try:
        from backend import extract_alt_metadata
    except Exception:
        extract_alt_metadata = None

try:
    import evaluate
except Exception:
    try:
        from backend import evaluate
    except Exception:
        evaluate = None

# Mount static files if directory exists
static_path = os.path.join(backend_dir, "static")
if os.path.exists(static_path):
    app.mount("/static", StaticFiles(directory=static_path), name="static")
elif os.path.exists("static"):
    app.mount("/static", StaticFiles(directory="static"), name="static")

@app.get("/", response_class=HTMLResponse)
def read_root():
    for path in ["static/index.html", os.path.join(backend_dir, "static/index.html")]:
        if os.path.exists(path):
            with open(path, "r", encoding="utf-8") as f:
                return f.read()
    return "<h1>Welcome to SchemaPilot 🚀</h1>"

@app.get("/health")
def health_check():
    return {"status": "healthy", "service": "schema-pilot"}

# --- DYNAMIC AGENT ENDPOINTS ---

@app.post("/agent")
@app.get("/agent")
def run_agent(request: Request, payload: Optional[AgentRequestPayload] = None):
    if not agent:
        return {"error": "Module 'agent' could not be imported."}
    try:
        custom_question = None
        if payload and payload.parameters:
            custom_question = payload.parameters.get("question")
         
        if hasattr(agent, "run"):
            result = agent.run(question=custom_question) if custom_question else agent.run()
        elif hasattr(agent, "inspect_schema"):
            result = agent.inspect_schema()
        else:
            result = {"status": "success", "message": "Agent module loaded successfully."}
            
        return {"action": "Dynamic Analyst", "result": result}
    except Exception as e:
        return {"action": "Dynamic Analyst", "error": str(e), "traceback": traceback.format_exc()}

@app.post("/multi-agent")
@app.get("/multi-agent")
def run_multi_agent(request: Request, payload: Optional[AgentRequestPayload] = None):
    if not multi_agent:
        return {"error": "Module 'multi_agent' could not be imported."}
    try:
        result = multi_agent.run() if hasattr(multi_agent, "run") else {"status": "success"}
        return {"action": "Multi-Agent Validation", "result": result}
    except Exception as e:
        return {"action": "Multi-Agent Validation", "error": str(e), "traceback": traceback.format_exc()}

@app.post("/multi-agent-audited")
@app.get("/multi-agent-audited")
def run_multi_agent_audited(request: Request, payload: Optional[AgentRequestPayload] = None):
    if not multi_agent_audited:
        return {"error": "Module 'multi_agent_audited' could not be imported."}
    try:
        result = multi_agent_audited.run() if hasattr(multi_agent_audited, "run") else {"status": "success"}
        return {"action": "Audited Pipeline", "result": result}
    except Exception as e:
        return {"action": "Audited Pipeline", "error": str(e), "traceback": traceback.format_exc()}

@app.post("/multi-agent-healing")
@app.get("/multi-agent-healing")
def run_multi_agent_healing(request: Request, payload: Optional[AgentRequestPayload] = None):
    if not multi_agent_healing:
        return {"error": "Module 'multi_agent_healing' could not be imported."}
    try:
        result = multi_agent_healing.run() if hasattr(multi_agent_healing, "run") else {"status": "success"}
        return {"action": "Self-Healing Audit", "result": result}
    except Exception as e:
        return {"action": "Self-Healing Audit", "error": str(e), "traceback": traceback.format_exc()}

@app.post("/extract-metadata")
@app.get("/extract-metadata")
def run_extract_metadata(request: Request):
    if not extract_metadata:
        return {"error": "Module 'extract_metadata' could not be imported."}
    try:
        result = extract_metadata.run() if hasattr(extract_metadata, "run") else {"status": "success"}
        return {"action": "Extract Metadata", "result": result}
    except Exception as e:
        return {"action": "Extract Metadata", "error": str(e), "traceback": traceback.format_exc()}

@app.post("/extract-alt-metadata")
@app.get("/extract-alt-metadata")
def run_extract_alt_metadata(request: Request):
    if not extract_alt_metadata:
        return {"error": "Module 'extract_alt_metadata' could not be imported."}
    try:
        result = extract_alt_metadata.run() if hasattr(extract_alt_metadata, "run") else {"status": "success"}
        return {"action": "Extract Alt Metadata", "result": result}
    except Exception as e:
        return {"action": "Extract Alt Metadata", "error": str(e), "traceback": traceback.format_exc()}

@app.post("/evaluate")
@app.get("/evaluate")
def run_evaluate(request: Request):
    if not evaluate:
        return {"error": "Module 'evaluate' could not be imported."}
    try:
        result = evaluate.run() if hasattr(evaluate, "run") else {"status": "success"}
        return {"action": "Evaluate Performance", "result": result}
    except Exception as e:
        return {"action": "Evaluate Performance", "error": str(e), "traceback": traceback.format_exc()}

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 8000))
    uvicorn.run("main:app", host="0.0.0.0", port=port)
