

import os
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from pathlib import Path

# existing imports...
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from models.request_models import ChatRequest, EndRequest
from models.response_models import ChatResponse, EndResponse
from core.orchestrator import process_user_query

app = FastAPI(title="Payment Chatbot API", version="1.0.0")

# Mount static folder
app.mount("/static", StaticFiles(directory="static"), name="static")

@app.get("/")
def home():
    return FileResponse(Path("static/index.html"))

# ... your existing /chat and /end endpoints here

@app.get("/health")
def health():
    return {"status": "ok"}

@app.post("/chat", response_model=ChatResponse)
def chat(req: ChatRequest):
    try:
        result = process_user_query(req.message, session_id=req.session_id)
        return ChatResponse(**result)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/end", response_model=EndResponse)
def end(req: EndRequest):
    result = process_user_query("end", session_id=req.session_id)
    return EndResponse(**result)

if __name__ == "__main__":
    port=int(os.getenv("PORT", 8080))
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=port)
