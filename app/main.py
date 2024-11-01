from fastapi import FastAPI
from app.api.endpoints import transcribe

app = FastAPI()

app.include_router(transcribe.router, prefix="/transcribe", tags=["transcribe"])

@app.get("/")
async def root():
    return {"message": "Welcome to the FastAPI YouTube Transcription Service"}
