# Utilizar una imagen base oficial de Python
FROM python:3.12-slim

# Establecer el directorio de trabajo
WORKDIR /app

# Copiar los archivos de requisitos
COPY requirements.txt .

# Instalar las dependencias
RUN pip install --no-cache-dir -r requirements.txt

# Instalar FFmpeg
RUN apt-get update && apt-get install -y ffmpeg

# Copiar el resto de los archivos de la aplicación
COPY . .

# Establecer las variables de entorno
ENV FFMPEG_PATH=/usr/bin/ffmpeg

# Exponer el puerto que usará la aplicación
EXPOSE 8000

# Comando para ejecutar la aplicación
CMD ["gunicorn", "--bind", "0.0.0.0:8000", "run:app"]