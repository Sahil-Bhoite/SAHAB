from pydantic import BaseModel
from typing import List, Optional

class ChatMessage(BaseModel):
    role: str
    content: str

class ChatRequest(BaseModel):
    prompt: str
    language: str = "English"
    history: List[ChatMessage] = []

class ChatResponse(BaseModel):
    answer: str
    language: str
    sources: Optional[List[str]] = None
