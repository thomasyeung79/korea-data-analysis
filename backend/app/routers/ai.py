from typing import Optional

from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel

from backend.app.dependencies import get_current_user
from backend.app.models.user import User
from backend.app.schemas.ai import AIGenerateRequest, AIGenerateResponse
from backend.app.services.openai_service import openai_service

router = APIRouter(prefix="/api/v1/ai", tags=["ai"])


@router.post("/generate", response_model=AIGenerateResponse)
def generate_ai(
    data: AIGenerateRequest,
    current_user: User = Depends(get_current_user),
):
    if not openai_service.is_available():
        raise HTTPException(
            status_code=503,
            detail="OpenAI service is not configured. Please set OPENAI_API_KEY in backend/.env",
        )

    try:
        result = openai_service.generate(data.prompt_type, data.params)
        return AIGenerateResponse(result=result)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"AI generation failed: {str(e)}")


class ChatRequest(BaseModel):
    message: str
    history: Optional[list[dict]] = None


class ChatResponse(BaseModel):
    reply: str


@router.post("/chat", response_model=ChatResponse)
def chat_ai(
    data: ChatRequest,
    current_user: User = Depends(get_current_user),
):
    if not openai_service.is_available():
        return ChatResponse(
            reply="⚠️ AI service is not configured. Please set OPENAI_API_KEY in the backend .env file to enable the Korea Q&A chat."
        )

    try:
        history_text = ""
        if data.history:
            for msg in data.history[-6:]:  # last 6 messages for context
                role = msg.get("role", "user")
                content = msg.get("content", "")
                history_text += f"{role}: {content}\n"

        prompt = f"""You are a Korea intelligence assistant called "KoreaIntel AI". You help users understand Korean culture, technology, sports, society, tourism, and business.

User's language preference: {current_user.language_preference}
Answer in the same language as the user's question.

Conversation history:
{history_text}

User: {data.message}

Provide a helpful, accurate, and concise response about Korea. If the question is about topics outside Korea, politely redirect back to Korea-related subjects."""

        response = openai_service.client.responses.create(
            model="gpt-4o-mini",
            input=prompt,
        )

        return ChatResponse(reply=response.output_text)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Chat generation failed: {str(e)}")
