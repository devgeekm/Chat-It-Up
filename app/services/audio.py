import os
from pathlib import Path
from pydub import AudioSegment
from app.utils.file_utils import print_styled_message, milliseconds_until_sound
from app.services.blob_storage_service import upload_file_to_blob, download_file_from_blob, delete_file_from_blob
from app.models.blob_storage import FileUploadRequest
from io import BytesIO
from urllib.parse import urlparse

# Configurar Pydub para usar FFmpeg desde la variable de entorno
ffmpeg_path = os.getenv('FFMPEG_PATH', 'ffmpeg')
AudioSegment.converter = ffmpeg_path

def trim_start(blob_url: str, silence_threshold_in_decibels=-20.0, min_silence_len=2000):
    """
    Recorta el silencio inicial de un archivo de audio si es mayor a 2 segundos.
    """
    try:
        # Descargar el archivo de Blob Storage
        path = download_file_from_blob(blob_url)
        parsed_url = urlparse(blob_url)
        filename = Path(parsed_url.path).name
        audio = AudioSegment.from_file(path, format="mp3")

        # Detectar el silencio inicial
        start_trim = milliseconds_until_sound(audio, silence_threshold_in_decibels)

        # Si el silencio inicial es mayor a 2 segundos, recortar el audio
        if start_trim > min_silence_len:
            print_styled_message("Recortando el silencio inicial del audio...")
            trimmed = audio[start_trim:] if start_trim < len(audio) else audio

            # Exportar el audio recortado en memoria
            buffer = BytesIO()
            trimmed.export(buffer, format="mp3")
            buffer.seek(0)
            file_data = buffer.read()

            # Subir el archivo recortado a Blob Storage
            file_request = FileUploadRequest(
                filename=f"trimmed_{filename}",
                file_data=file_data
            )
            trimmed_blob_url = upload_file_to_blob(file_request)
            print_styled_message(f"Audio recortado guardado en Blob Storage: {trimmed_blob_url}")

            return trimmed_blob_url, True
        else:
            print_styled_message("No se encontró un silencio inicial mayor a 2 segundos. No se recortará el audio.")
            return blob_url, False
    except Exception as e:
        print_styled_message(f"Error al recortar el audio: {str(e)}")
        raise

def convert_audio_to_wav(input_url: str) -> str:
    """
    Convierte un archivo de audio a formato WAV.
    """
    try:
        # Descargar el archivo de Blob Storage
        path = download_file_from_blob(input_url)
        audio = AudioSegment.from_file(path)

        # Extraer el nombre y extensión del archivo
        parsed_url = urlparse(input_url)
        filename = Path(parsed_url.path).name
        stem = Path(filename).stem
        output_filename = stem + '.wav'

        # Exportar el audio a WAV en memoria
        buffer = BytesIO()
        audio.export(buffer, format='wav')
        buffer.seek(0)
        file_data = buffer.read()

        # Subir el archivo WAV a Blob Storage
        file_request = FileUploadRequest(
            filename=output_filename,
            file_data=file_data
        )
        wav_blob_url = upload_file_to_blob(file_request)
        print_styled_message(f"Archivo WAV guardado en Blob Storage: {wav_blob_url}")

        return wav_blob_url
    except Exception as e:
        print_styled_message(f"Error al convertir el archivo de audio: {str(e)}")
        raise

def split_audio(file_url: str, max_size_mb: int = 25) -> list[str]:
    """
    Divide un archivo de audio en partes más pequeñas si excede el tamaño máximo permitido.
    """
    try:
        # Descargar el archivo de Blob Storage
        file_path = download_file_from_blob(file_url)
        audio = AudioSegment.from_file(file_path)
        max_size_bytes = max_size_mb * 1024 * 1024

        if len(audio.raw_data) <= max_size_bytes:
            return [file_url]

        num_parts = len(audio.raw_data) // max_size_bytes + (1 if len(audio.raw_data) % max_size_bytes != 0 else 0)
        part_duration_ms = len(audio) // num_parts

        audio_parts = []
        print_styled_message(f"Dividiendo audio en {num_parts} partes...")

        # Extraer el nombre y extensión del archivo
        parsed_url = urlparse(file_url)
        filename = Path(parsed_url.path).name
        stem = Path(filename).stem
        suffix = Path(filename).suffix

        for i in range(num_parts):
            start_time = i * part_duration_ms
            end_time = min((i + 1) * part_duration_ms, len(audio))

            part = audio[start_time:end_time]
            part_filename = f"{stem}_part{i+1}{suffix}"

            # Exportar la parte de audio en memoria
            buffer = BytesIO()
            part.export(buffer, format=suffix[1:])
            buffer.seek(0)
            file_data = buffer.read()

            # Subir cada parte a Blob Storage
            file_request = FileUploadRequest(
                filename=part_filename,
                file_data=file_data
            )
            part_url = upload_file_to_blob(file_request)
            audio_parts.append(part_url)

        return audio_parts

    except Exception as e:
        print_styled_message(f"Error al dividir el audio: {str(e)}")
        raise

def convert_audio(input_path: str, output_path: str, format: str = 'mp3'):
    """
    Convierte un archivo de audio a otro formato usando Pydub y FFmpeg.
    """
    audio = AudioSegment.from_file(input_path)
    audio.export(output_path, format=format)
    return output_path

# Ejemplo de uso
# convert_audio('/path/to/input/file.wav', '/path/to/output/file.mp3')