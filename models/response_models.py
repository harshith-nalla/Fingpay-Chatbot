from pydantic import BaseModel

class ChatResponse(BaseModel):
    reply: str
    intent: str
    disposition: str

class EndResponse(BaseModel):
    reply: str
    intent: str
    disposition: str
