from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from app.services.youtube import download_youtube_audio
from app.services.audio import trim_start
from app.services.azure_clients import initialize_azure_clients
from app.services.transcription import transcribe_audio
from app.services.content_safety import analyze_content_safety, display_content_safety_results
from app.services.translation import translate_text
from app.services.improvement import improve_transcription
from app.utils.file_utils import read_file, print_styled_message, cleanup_temp_files
from app.utils.text_utils import split_text
from collections import defaultdict
from pathlib import Path

router = APIRouter()

class YouTubeURL(BaseModel):
    url: str

@router.post("/")
async def transcribe_youtube_audio(youtube_url: YouTubeURL):
    try:
        # Descargar y procesar el audio
        original_file_path = download_youtube_audio(youtube_url.url, "audio")
        trimmed_file_path, is_trimmed = trim_start(str(original_file_path))

        file_to_transcribe = str(trimmed_file_path)
        output_folder = "reviews"

        # Inicializar clientes de Azure
        clients = initialize_azure_clients()

        # Transcribir el audio
        output_path = transcribe_audio(file_to_transcribe, output_folder, clients['whisper'], youtube_url.url)
        text = read_file(output_path)

        # Análisis de seguridad del contenido
        text_parts = split_text(text, 5120)
        all_safety_results = [
            analyze_content_safety(clients['content_safety'], part)
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
            detected = clients['ai'].detect_language(documents=[{"id": "1", "text": part}])[0]
            languages[detected.primary_language.iso6391_name] += 1

        predominant_language = max(languages.items(), key=lambda x: x[1])[0]

        # Traducción si es necesario
        if predominant_language == 'en':
            print_styled_message("El texto está en inglés. Se procederá a traducirlo al español.")
            translated_text = translate_text(text_parts, clients)
            text_to_improve = translated_text
            language_to_improve = 'es'
            # Guardar el texto traducido
            translated_path = Path(output_path).parent / f"translated_{Path(output_path).name}"
            with open(translated_path, 'w', encoding='utf-8') as f:
                f.write(translated_text)
            print_styled_message(f"Texto traducido guardado en: {translated_path}")
        else:
            print_styled_message("El texto está en español. No es necesaria la traducción.")
            text_to_improve = text
            language_to_improve = predominant_language

        # Mejorar el texto
        print_styled_message("Mejorando el texto...")
        improved_text = improve_transcription(text_to_improve, clients['gpt'], language=language_to_improve)

        # Guardar el texto mejorado
        improved_path = Path(output_path).parent / f"improved_{Path(output_path).name}"
        with open(improved_path, 'w', encoding='utf-8') as f:
            f.write(improved_text)
        print_styled_message(f"Texto mejorado guardado en: {improved_path}")

        return {"message": "Transcripción completada y mejorada", "transcription": improved_text}

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))