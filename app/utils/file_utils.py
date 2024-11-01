from pathlib import Path
from azure.storage.blob import BlobServiceClient
from azure.core.exceptions import ResourceNotFoundError
from urllib.parse import urlparse, unquote
import os

def print_styled_message(message: str, color: str = "", style: str = "") -> None:
    """
    Imprime un mensaje en la consola.
    """
    print(message)

def read_file(file_path: str) -> str:
    """
    Lee el contenido de un archivo de texto.
    """
    with open(file_path, 'r', encoding='utf-8') as file:
        return file.read()

def cleanup_temp_files(file_path: Path, audio_parts: list[str]):
    """
    Limpia los archivos temporales generados durante el proceso.
    """
    try:
        # Eliminar archivos .wav en el directorio del archivo principal
        for wav_file in file_path.parent.glob("*.wav"):
            wav_file.unlink()

        # Convertir las rutas de audio_parts a objetos Path y eliminar los archivos
        for part in audio_parts:
            part_path = Path(part)
            if part_path.exists():
                part_path.unlink()
    except Exception as e:
        print_styled_message(f"Error al limpiar archivos temporales: {str(e)}")
        raise

def milliseconds_until_sound(sound, silence_threshold_in_decibels=-20.0, chunk_size=10):
    """
    Devuelve el número de milisegundos hasta el primer sonido.
    """
    trim_ms = 0  # ms
    assert chunk_size > 0  # para evitar bucles infinitos
    while sound[trim_ms:trim_ms + chunk_size].dBFS < silence_threshold_in_decibels and trim_ms < len(sound):
        trim_ms += chunk_size
    return trim_ms