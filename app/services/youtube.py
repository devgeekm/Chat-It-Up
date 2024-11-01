import yt_dlp
from pathlib import Path
from app.utils.file_utils import print_styled_message
from app.services.blob_storage_service import upload_file_to_blob, download_file_from_blob
from app.models.blob_storage import FileUploadRequest

def download_youtube_audio(url: str) -> str:
    """
    Descarga el audio de un video de YouTube y lo guarda en formato MP3.
    """
    ydl_opts = {
        'format': 'bestaudio/best',
        'postprocessors': [{
            'key': 'FFmpegExtractAudio',
            'preferredcodec': 'mp3',
            'preferredquality': '192',
        }],
        'outtmpl': '/tmp/audio01.%(ext)s',  # Guardar temporalmente en /tmp
        'quiet': True,
    }

    print_styled_message("Iniciando la descarga del audio del video de YouTube...")

    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            ydl.download([url])

        print_styled_message("Descarga completada. Procesando el archivo de audio...")
        mp3_file = Path('/tmp/audio01.mp3')

        if not mp3_file.exists():
            raise FileNotFoundError(f"No se pudo encontrar el archivo descargado: {mp3_file}")

        # Leer el archivo MP3 y subirlo a Blob Storage
        with open(mp3_file, 'rb') as f:
            file_data = f.read()
        file_request = FileUploadRequest(
            filename="audio01.mp3",  # Asegurarse de que el nombre del archivo sea correcto
            file_data=file_data
        )
        blob_url = upload_file_to_blob(file_request)
        print_styled_message(f"Archivo subido a Blob Storage: {blob_url}")

        return blob_url

    except Exception as e:
        print_styled_message(f"Error durante la descarga: {str(e)}")
        raise

def get_youtube_title(url: str) -> str:
    """
    Obtiene el título del video de YouTube.
    """
    ydl_opts = {'quiet': True}
    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        info_dict = ydl.extract_info(url, download=False)
        return info_dict.get('title')