#!/bin/bash

# Descargar e instalar FFmpeg
apt-get update && apt-get install -y ffmpeg

# Verificar la instalación de FFmpeg
ffmpeg -version

# Iniciar la aplicación
gunicorn --bind=0.0.0.0 --timeout 600 run:app