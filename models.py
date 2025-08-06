from pydantic import BaseModel, Field

class SessionCreateRequest(BaseModel):
    session_user: str = Field(..., min_length=1)

class SessionResponse(BaseModel):
    session_id: int
    session_user: str
    created_at: str

class MessageRequest(BaseModel):
    role: str
    content: str

class Message(BaseModel):
    role: str
    content: str
