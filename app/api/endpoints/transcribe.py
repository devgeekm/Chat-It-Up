from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from app.services.youtube import download_youtube_audio
from app.services.audio import trim_start, convert_audio_to_wav, split_audio
from app.services.azure_clients import initialize_azure_clients
from app.services.transcription import transcribe_audio
from app.services.content_safety import analyze_content_safety, display_content_safety_results
from app.services.translation import translate_text
from app.services.improvement import improve_transcription
from app.utils.file_utils import read_file, print_styled_message, cleanup_temp_files
from app.utils.text_utils import split_text
from collections import defaultdict
from pathlib import Path
from app.services.blob_storage_service import upload_file_to_blob, delete_file_from_blob
from app.models.blob_storage import FileUploadRequest

router = APIRouter()

class YouTubeURL(BaseModel):
    url: str

@router.post("/")
async def transcribe_youtube_audio(youtube_url: YouTubeURL):
    try:
        # Descargar y procesar el audio
        original_file_url = download_youtube_audio(youtube_url.url)
        trimmed_file_url, is_trimmed = trim_start(original_file_url)

        # Usar el archivo original si no se realizó ninguna edición
        file_to_transcribe = trimmed_file_url if is_trimmed else original_file_url

        # Inicializar clientes de Azure
        clients = initialize_azure_clients()

        # Transcribir el audio
        output_url = transcribe_audio(file_to_transcribe, clients['whisper'], youtube_url.url)
        text = read_file(output_url)

        # Imprimir mensaje de iniciar análisis de seguridad
        print_styled_message('\nIniciando análisis de seguridad...')
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
            # Subir el texto traducido a Blob Storage
            translated_request = FileUploadRequest(
                filename=f"translated_{Path(output_url).name}",
                file_data=translated_text.encode('utf-8')
            )
            translated_url = upload_file_to_blob(translated_request)
            print_styled_message(f"Texto traducido guardado en Blob Storage: {translated_url}")
        else:
            print_styled_message("El texto está en español. No es necesaria la traducción.")
            text_to_improve = text
            language_to_improve = predominant_language

        # Mejorar el texto
        print_styled_message("Mejorando el texto...")
        improved_text = improve_transcription(text_to_improve, clients['gpt'], language=language_to_improve)

        # Subir el texto mejorado a Blob Storage
        improved_request = FileUploadRequest(
            filename=f"improved_{Path(output_url).name}",
            file_data=improved_text.encode('utf-8')
        )
        improved_url = upload_file_to_blob(improved_request)
        print_styled_message(f"Texto mejorado guardado en Blob Storage: {improved_url}")

        return {
            "message": "Transcripción completada y mejorada",
            "transcription": improved_text,
            "blob_url": improved_url
        }

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.delete("/delete/{filename}")
async def delete_file(filename: str):
    try:
        delete_file_from_blob(filename)
        return {"message": "Archivo eliminado correctamente"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))