from pathlib import Path

def print_styled_message(message: str, color: str = "", style: str = "") -> None:
    """
    Imprime un mensaje en la consola.
    """
    print(message)

def read_file(file_path: str) -> str:
    """
    Lee el contenido de un archivo de texto.
    """
    try:
        with open(file_path, 'r', encoding='utf-8') as file:
            return file.read()
    except FileNotFoundError:
        print_styled_message(f"Error: El archivo {file_path} no se encuentra.")
        raise
    except Exception as e:
        print_styled_message(f"Error al leer el archivo {file_path}: {str(e)}")
        raise

def cleanup_temp_files(file_path: Path, audio_parts: list[Path]):
    """Limpia los archivos temporales generados durante el proceso."""
    try:
        for wav_file in file_path.parent.glob("*.wav"):
            wav_file.unlink()

        for part in audio_parts:
            if part.exists():
                part.unlink()
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