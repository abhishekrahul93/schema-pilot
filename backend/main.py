from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import sys
import os

app = FastAPI(title="SchemaPilot API", version="1.0.0")

try:
    import agent
    AGENT_AVAILABLE = True
except ImportError:
    AGENT_AVAILABLE = False

class AgentRequest(BaseModel):
    parameters: dict

@app.get("/")
def health_check():
    return {"status": "online", "system": "SchemaPilot Backend"}

@app.post("/agent")
def run_agent(payload: AgentRequest):
    question = payload.parameters.get("question", "")
    if not AGENT_AVAILABLE:
        return {"error": "Module 'agent' could not be imported."}
    
    try:
        response = agent.run_agent_query(question)
        return response
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
