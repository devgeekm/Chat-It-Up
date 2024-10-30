from fastapi import APIRouter, HTTPException
from models.request_models import ChatRequest
from services.openai_service import chat_with_openai

router = APIRouter()

@router.post('/')
async def chat( request: ChatRequest ):
    try:
        resp = await chat_with_openai( request.message )
        return { 'response': resp }
    except Exception as e:
        raise HTTPException( status_code=500, detail=str(e) )