from fastapi import FastAPI
from app.api.endpoints import transcribe
import os
import uvicorn

app = FastAPI()

app.include_router(transcribe.router, prefix="/api/v1/transcribe", tags=["transcribe"])

@app.get("/")
def read_root():
    return {"message": "Welcome to the FastAPI YouTube Transcription Service"}

if __name__ == "__main__":
    # Obtener el puerto desde la variable de entorno PORT (Azure asigna este puerto automáticamente)
    port = int(os.getenv("PORT", 5000))
    # Ejecutar la aplicación con Uvicorn
    uvicorn.run(app, host="0.0.0.0", port=port)