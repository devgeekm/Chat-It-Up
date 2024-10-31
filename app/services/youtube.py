import yt_dlp
from pathlib import Path
from app.utils.file_utils import print_styled_message

def download_youtube_audio(url: str, output_folder: str) -> str:
    """
    Descarga el audio de un video de YouTube y lo guarda en formato MP3.
    """
    output_folder = Path(output_folder)
    output_folder.mkdir(parents=True, exist_ok=True)

    ydl_opts = {
        'format': 'bestaudio/best',
        'postprocessors': [{
            'key': 'FFmpegExtractAudio',
            'preferredcodec': 'mp3',
            'preferredquality': '192',
        }],
        'outtmpl': str(output_folder / 'audio01.%(ext)s'),
        'quiet': True,
    }

    print_styled_message("Iniciando la descarga del audio del video de YouTube...")

    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            ydl.download([url])

        print_styled_message("Descarga completada. Procesando el archivo de audio...")
        mp3_file = output_folder / "audio01.mp3"

        if not mp3_file.exists():
            raise FileNotFoundError(f"No se pudo encontrar el archivo descargado: {mp3_file}")

        return str(mp3_file)

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