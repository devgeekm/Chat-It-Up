from pathlib import Path
from pydub import AudioSegment
from app.utils.file_utils import print_styled_message, milliseconds_until_sound

def trim_start(filepath, silence_threshold_in_decibels=-20.0, min_silence_len=2000):
    """
    Recorta el silencio inicial de un archivo de audio si es mayor a 2 segundos.
    """
    path = Path(filepath)
    directory = path.parent
    filename = path.name
    audio = AudioSegment.from_file(filepath, format="mp3")

    # Detectar el silencio inicial
    start_trim = milliseconds_until_sound(audio, silence_threshold_in_decibels)

    # Si el silencio inicial es mayor a 2 segundos, recortar el audio
    if (start_trim > min_silence_len):
        print_styled_message("Recortando el silencio inicial del audio...")
        trimmed = audio[start_trim:] if start_trim < len(audio) else audio
        new_filename = directory / f"trimmed_{filename}"
        trimmed.export(new_filename, format="mp3")
        print_styled_message(f"Audio recortado guardado en: {new_filename}")
        return new_filename, True
    else:
        print_styled_message("No se encontró un silencio inicial mayor a 2 segundos. No se recortará el audio.")
        return filepath, False

def convert_audio_to_wav(input_path: str, output_path: str) -> None:
    """
    Convierte un archivo de audio a formato WAV.
    """
    try:
        audio = AudioSegment.from_file(input_path)
        audio.export(output_path, format='wav')
    except Exception as e:
        print_styled_message(f"Error al convertir el archivo de audio: {str(e)}")
        raise

def split_audio(file_path: Path, max_size_mb: int = 25) -> list[Path]:
    """
    Divide un archivo de audio en partes más pequeñas si excede el tamaño máximo permitido.
    """
    try:
        audio = AudioSegment.from_file(str(file_path))
        max_size_bytes = max_size_mb * 1024 * 1024

        if len(audio.raw_data) <= max_size_bytes:
            return [file_path]

        num_parts = len(audio.raw_data) // max_size_bytes + (1 if len(audio.raw_data) % max_size_bytes != 0 else 0)
        part_duration_ms = len(audio) // num_parts

        audio_parts = []
        print_styled_message(f"Dividiendo audio en {num_parts} partes...")

        for i in range(num_parts):
            start_time = i * part_duration_ms
            end_time = min((i + 1) * part_duration_ms, len(audio))

            part = audio[start_time:end_time]
            part_file_path = file_path.parent / f"{file_path.stem}_part{i+1}{file_path.suffix}"
            part.export(str(part_file_path), format=file_path.suffix[1:])
            audio_parts.append(part_file_path)

        return audio_parts

    except Exception as e:
        print_styled_message(f"Error al dividir el audio: {str(e)}")
        raise