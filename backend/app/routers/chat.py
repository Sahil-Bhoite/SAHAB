from fastapi import APIRouter, HTTPException
from fastapi.responses import StreamingResponse
from app.models.schemas import ChatRequest
from app.services.rag_service import rag_service
from deep_translator import GoogleTranslator
import json

router = APIRouter()

@router.post("/chat")
async def chat_endpoint(request: ChatRequest):
    try:
        if request.language.lower() == "english":
            # Stream directly from Gemini
            return StreamingResponse(
                rag_service.get_response_stream(request.prompt),
                media_type="text/event-stream"
            )
        else:
            # For other languages, we must wait for full response to translate contextually
            # Then stream the translated result to keep frontend consistent
            full_response_generator = rag_service.get_response_stream(request.prompt)
            full_text = "".join([chunk for chunk in full_response_generator])
            
            try:
                translator = GoogleTranslator(source='auto', target=request.language.lower())
                translated_text = translator.translate(full_text)
            except Exception as e:
                print(f"Translation error: {e}")
                translated_text = full_text # Fallback

            # Fake generator for streaming
            async def fake_stream():
                # Split by words or small chunks to simulate streaming
                words = translated_text.split(' ')
                for word in words:
                    yield word + " "
                    # A tiny delay could be added here but maybe not needed
            
            return StreamingResponse(
                fake_stream(),
                media_type="text/event-stream"
            )

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
