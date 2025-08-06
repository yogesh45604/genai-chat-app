from fastapi import FastAPI, HTTPException, Path, Query
from datetime import datetime
from typing import List, Optional

from models import SessionCreateRequest, SessionResponse, MessageRequest, Message
from store import session_store, chat_store

app = FastAPI()

@app.post("/sessions", response_model=SessionResponse)
def create_session(session_data: SessionCreateRequest):
    username = session_data.session_user.strip().lower()

    if not username:
        raise HTTPException(status_code=400, detail="Username cannot be empty.")

    session_id = len(session_store) + 1
    created_at = datetime.utcnow().isoformat()

    session = {
        "session_id": session_id,
        "session_user": username,
        "created_at": created_at
    }

    session_store.append(session)
    chat_store[session_id] = []

    return session

@app.post("/sessions/{session_id}/messages")
def add_message_to_session(
    session_id: int = Path(..., gt=0),
    message: MessageRequest = None
):
    if session_id not in chat_store:
        raise HTTPException(status_code=404, detail="Session not found.")

    if message.role not in {"user", "assistant"}:
        raise HTTPException(status_code=400, detail="Role must be 'user' or 'assistant'.")

    chat_store[session_id].append({"role": message.role, "content": message.content})
    return {"status": "message added"}

@app.get("/sessions/{session_id}/messages", response_model=List[Message])
def get_session_messages(
    session_id: int = Path(..., gt=0),
    role: Optional[str] = Query(None)
):
    if session_id not in chat_store:
        raise HTTPException(status_code=404, detail="Session not found.")

    messages = chat_store[session_id]
    if role:
        messages = [msg for msg in messages if msg["role"] == role]

    return messages
