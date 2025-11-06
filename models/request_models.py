from pydantic import BaseModel, Field
from typing import Optional

class ChatRequest(BaseModel):
    message: str = Field(..., min_length=1, description="User message text")
    session_id: Optional[str] = Field(default="default")

class EndRequest(BaseModel):
    session_id: Optional[str] = "default"
