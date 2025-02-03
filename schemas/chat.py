from pydantic import BaseModel

class ChatRequest(BaseModel):
    user_query: str
    session_id: str = "default"

class ChatResponse(BaseModel):
    response: str
    session_id: str
    agent_used: str