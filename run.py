from fastapi import FastAPI
from app.api.endpoints import transcribe
import subprocess
import os
import signal
import time

app = FastAPI()

app.include_router(transcribe.router, prefix="/api/v1/transcribe", tags=["transcribe"])

@app.get("/")
def read_root():
    return {"message": "Welcome to the FastAPI YouTube Transcription Service"}

def clean_port(port):
    try:
        # Encuentra el proceso que está utilizando el puerto
        result = subprocess.run(["lsof", "-i", f":{port}"], capture_output=True, text=True)
        lines = result.stdout.splitlines()
        if len(lines) > 1:
            # Extrae el PID del proceso
            pid = int(lines[1].split()[1])
            # Mata el proceso
            os.kill(pid, signal.SIGKILL)
            print(f"Proceso {pid} que utilizaba el puerto {port} ha sido terminado.")
        else:
            print(f"No se encontró ningún proceso utilizando el puerto {port}.")
    except Exception as e:
        print(f"Error al limpiar el puerto {port}: {str(e)}")

def is_port_in_use(port):
    result = subprocess.run(["lsof", "-i", f":{port}"], capture_output=True, text=True)
    lines = result.stdout.splitlines()
    return len(lines) > 1

import uvicorn

if __name__ == "__main__":
    uvicorn.run("app.main:app", host="0.0.0.0", port=8000, reload=True)