from fastapi import FastAPI, HTTPException, Query, File, UploadFile, APIRouter
from fastapi.responses import JSONResponse
from src.speech2text import Speech2Text
from src.config import CLASS_MODEL, HOST, PORT
from typing import Optional
from pydantic import BaseModel
import base64
import os

app = FastAPI(title="Speech-to-Text API", description="API for converting speech to text using various engines and languages")
stt = Speech2Text()

class InfoResponse(BaseModel):
    service: str
    message: str
    language: str
    results: Optional[dict] = None

def get_info(message: str, result: Optional[dict] = None) -> InfoResponse:
    return InfoResponse(
        service=CLASS_MODEL,
        message=message,
        language=stt.language,
        results=result
    )

@app.get("/", response_model=InfoResponse)
async def read_root():
    return get_info(
        "Welcome to Speech-to-Text API",
        {
            "version": "1.0.0",
            "description": "API for converting speech to text using various engines and languages",
            "endpoints": {
                "GET /": "This information",
                "PUT /v1/api/using/engine": "Update speech-to-text engine",
                "PUT /v1/api/using/language": "Update speech-to-text language",
                "POST /v1/api/using/speech2text": "Convert speech to text (file upload)",
                "POST /v1/api/using_base64/speech2text_base64": "Convert speech to text (base64 encoded audio)"
            }
        }
    )

using_router = APIRouter(prefix="/v1/api/using", tags=["using"])

@using_router.put("/engine", response_model=InfoResponse)
async def update_engine(engine: str = Query(..., description="Specify the engine")):
    stt.engine = engine
    return get_info(f"Speech-to-text engine successfully updated to '{engine}'")

@using_router.put("/language", response_model=InfoResponse)
async def update_language(language: str = Query(..., description="Specify the language")):
    stt.language = language
    return get_info(f"Speech-to-text language successfully set to '{language}'")

@using_router.post("/speech2text", response_model=InfoResponse)
async def speech_to_text(file: UploadFile = File(...)):
    try:
        temp_dir = "temp"
        os.makedirs(temp_dir, exist_ok=True)
        
        file_path = f"./{temp_dir}/{file.filename}"
        with open(file_path, "wb") as buffer:
            buffer.write(await file.read())        
        
        results, _, file_wav = stt.start(file_path)

        if file.content_type != "audio/wav":
            os.remove(file_path)
        if file_wav:
            os.remove(file_wav)

        return get_info("Speech-to-text conversion completed successfully.", results)
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

base64_router = APIRouter(prefix="/v1/api/using_base64", tags=["base64"])

class AudioBase64(BaseModel):
    filename: str
    content: str

@base64_router.post("/speech2text_base64", response_model=InfoResponse)
async def speech_to_text_base64(audio: AudioBase64):
    try:
        temp_dir = "temp"
        os.makedirs(temp_dir, exist_ok=True)
        
        file_path = f'./{temp_dir}/{audio.filename}'
        audio_content = base64.b64decode(audio.content)
        with open(file_path, "wb") as buffer:
            buffer.write(audio_content)
        
        results, _, file_wav = stt.start(file_path)

        if not file_path.endswith(".wav"):
            os.remove(file_path)
        if file_wav:
            os.remove(file_wav)

        return get_info("Speech-to-text conversion base64 completed successfully.", results)
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

app.include_router(using_router)
app.include_router(base64_router)

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host=HOST, port=PORT)