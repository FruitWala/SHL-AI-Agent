from fastapi import APIRouter
from pydantic import BaseModel
from typing import List

from app.agents.recommender import chat

router = APIRouter()


class Message(BaseModel):
    role: str
    content: str


class ChatRequest(BaseModel):
    messages: List[Message]


@router.get("/health")
def health():
    return {
        "status": "ok"
    }


@router.post("/chat")
def chat_api(request: ChatRequest):

    return chat(request.messages)