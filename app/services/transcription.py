from pathlib import Path
from collections import defaultdict
from typing import Optional
from openai import AzureOpenAI
from azure.ai.contentsafety import ContentSafetyClient
from azure.ai.textanalytics import TextAnalyticsClient
from app.utils.file_utils import print_styled_message, read_file, cleanup_temp_files
from app.utils.text_utils import split_text, split_text_gpt
from app.services.audio import convert_audio_to_wav, split_audio
from app.services.azure_clients import initialize_azure_clients
from app.services.youtube import get_youtube_title
from app.services.content_safety import analyze_content_safety, display_content_safety_results
from app.services.translation import translate_text
from app.services.improvement import improve_transcription

def transcribe_audio(file_path: str, output_folder: str, whisper_client: AzureOpenAI, youtube_url: Optional[str] = None) -> str:
    """
    Transcribe un archivo de audio y guarda el resultado en un archivo .txt.
    """
    try:
        if youtube_url:
            video_title = get_youtube_title(youtube_url).rstrip()
        else:
            video_title = Path(file_path).stem

        file_path = Path(file_path)
        output_folder = Path(output_folder)
        output_folder.mkdir(parents=True, exist_ok=True)
        output_path = output_folder / f"{video_title}.txt"

        if not file_path.exists():
            raise FileNotFoundError(f"No se encuentra el archivo de audio: {file_path}")

        wav_path = file_path.with_suffix('.wav')
        convert_audio_to_wav(str(file_path), str(wav_path))

        audio_parts = split_audio(wav_path)
        transcribed_parts = transcribe_audio_parts(audio_parts, whisper_client)

        transcribed_text = ' '.join(transcribed_parts)
        with open(output_path, 'w', encoding='utf-8') as file:
            file.write(transcribed_text)

        print_styled_message(f"Transcripción guardada en: {output_path}")

        cleanup_temp_files(file_path, audio_parts)
        return str(output_path)

    except Exception as e:
        print_styled_message(f"Error en la transcripción: {str(e)}")
        raise

def transcribe_audio_parts(audio_parts: list[Path], whisper_client: AzureOpenAI) -> list[str]:
    """
    Transcribe múltiples partes de audio usando el modelo Whisper de Azure OpenAI.
    """
    transcribed_parts = []
    total_parts = len(audio_parts)

    print_styled_message(f"Iniciando transcripción de {total_parts} {'parte' if total_parts == 1 else 'partes'}...")

    for audio_file in audio_parts:
        try:
            with open(audio_file, "rb") as audio:
                result = whisper_client.audio.transcriptions.create(file=audio, model="whisper")
                transcribed_parts.append(result.text)
        except Exception as e:
            print_styled_message(f"Error al transcribir {audio_file.name}: {str(e)}")
            raise

    print_styled_message("Transcripción de todas las partes completada")
    return transcribed_parts

def analyze_and_improve_transcription(text: str, ai_client: TextAnalyticsClient, content_safety_client: ContentSafetyClient, variables: dict) -> str:
    """
    Analiza la seguridad del contenido, detecta el idioma, traduce si es necesario y mejora la transcripción.
    """
    # Análisis de seguridad del contenido
    text_parts = split_text(text, 5120)
    all_safety_results = [
        analyze_content_safety(content_safety_client, part)
        for part in text_parts
    ]

    # Consolidar y mostrar resultados de seguridad
    consolidated_results = defaultdict(int)
    for result in all_safety_results:
        for category, analysis in result.items():
            if analysis:
                consolidated_results[category] = max(consolidated_results[category], analysis.severity)

    display_content_safety_results(consolidated_results)

    # Detección de idioma
    languages = defaultdict(int)
    for part in text_parts:
        detected = ai_client.detect_language(documents=[{"id": "1", "text": part}])[0]
        languages[detected.primary_language.iso6391_name] += 1

    predominant_language = max(languages.items(), key=lambda x: x[1])[0]

    # Traducción si es necesario
    if predominant_language == 'en':
        print_styled_message("El texto está en inglés. Se procederá a traducirlo al español.")
        translated_text = translate_text(text_parts, variables)
        text_to_improve = translated_text
        language_to_improve = 'es'
    else:
        print_styled_message("El texto está en español. No es necesaria la traducción.")
        text_to_improve = text
        language_to_improve = predominant_language

    # Mejorar el texto
    print_styled_message("Mejorando el texto...")
    improved_text = improve_transcription(text_to_improve, ai_client, language=language_to_improve)

    return improved_text