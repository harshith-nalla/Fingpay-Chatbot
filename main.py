import os
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from pathlib import Path

# FastAPI imports
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware

# Local imports
from models.request_models import ChatRequest, EndRequest
from models.response_models import ChatResponse, EndResponse
from core.orchestrator import process_user_query

# Create FastAPI app
app = FastAPI(title="Payment Chatbot API", version="1.0.0")

# Allow CORS (optional)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Serve static frontend
app.mount("/static", StaticFiles(directory="static"), name="static")

@app.get("/")
def home():
    """Serve frontend HTML file"""
    return FileResponse(Path("static/index.html"))

# Health check endpoint
@app.get("/health")
def health():
    return {"status": "ok"}

# Chatbot API endpoints
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

# 🔥 Main entry point for both local & Cloud Run
if __name__ == "__main__":
    import uvicorn

    # Cloud Run passes the port via $PORT, default = 8080
    port = int(os.getenv("PORT", 8080))

    # Run with app reference as a string — "main:app"
    uvicorn.run("main:app", host="0.0.0.0", port=port, reload=False)
