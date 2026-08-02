import os
import uvicorn
from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from fastapi.responses import HTMLResponse

app = FastAPI(title="SchemaPilot API", version="1.0.0")

# Mount static files if directory exists
if os.path.exists("static"):
    app.mount("/static", StaticFiles(directory="static"), name="static")

@app.get("/", response_class=HTMLResponse)
def read_root():
    if os.path.exists("static/index.html"):
        with open("static/index.html", "r", encoding="utf-8") as f:
            return f.read()
    return "<h1>Welcome to SchemaPilot 🚀</h1><p>Your AI-powered schema management agent is running successfully.</p>"

@app.get("/health")
def health_check():
    return {"status": "healthy", "service": "schema-pilot"}

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 8000))
    uvicorn.run("main:app", host="0.0.0.0", port=port)
