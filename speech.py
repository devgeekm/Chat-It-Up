import os
from pathlib import Path
from dotenv import load_dotenv
from openai import AzureOpenAI
from azure.core.credentials import AzureKeyCredential
from azure.ai.contentsafety import ContentSafetyClient
from azure.ai.textanalytics import TextAnalyticsClient
from azure.core.exceptions import HttpResponseError
from azure.ai.contentsafety.models import AnalyzeTextOptions, TextCategory
from collections import defaultdict
from typing import Optional
import requests
import uuid
import json
import yt_dlp
from pydub import AudioSegment

def print_styled_message(message: str, color: str = "", style: str = "") -> None:
    """
    Imprime un mensaje en la consola.
    """
    print(message)

def milliseconds_until_sound(sound, silence_threshold_in_decibels=-20.0, chunk_size=10):
    """
    Devuelve el número de milisegundos hasta el primer sonido.
    """
    trim_ms = 0  # ms
    assert chunk_size > 0  # para evitar bucles infinitos
    while sound[trim_ms:trim_ms + chunk_size].dBFS < silence_threshold_in_decibels and trim_ms < len(sound):
        trim_ms += chunk_size
    return trim_ms

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

def split_text(text: str, max_length: int) -> list:
    """
    Divide el texto en partes más pequeñas de longitud máxima `max_length`.
    """
    return [text[i:i + max_length] for i in range(0, len(text), max_length)]

def split_text_gpt(text: str, max_tokens: int) -> list:
    """
    Divide el texto en fragmentos que no excedan el límite de tokens.
    """
    words = text.split()
    chunks = []
    current_chunk = []

    for word in words:
        if len(current_chunk) + len(word.split()) > max_tokens:
            chunks.append(' '.join(current_chunk))
            current_chunk = [word]
        else:
            current_chunk.append(word)

    if current_chunk:
        chunks.append(' '.join(current_chunk))

    return chunks

def read_file(file_path: str) -> str:
    """
    Lee el contenido de un archivo de texto.
    """
    with open(file_path, 'r', encoding='utf-8') as file:
        return file.read()

def download_youtube_audio(url: str, output_folder: str) -> str:
    """
    Descarga el audio de un video de YouTube y lo guarda en formato MP3.
    """
    # Asegurarse de que la carpeta de salida exista
    output_folder = Path(output_folder)
    output_folder.mkdir(parents=True, exist_ok=True)

    # Opciones para yt-dlp
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
            # Descargar el audio
            ydl.download([url])

        print_styled_message("Descarga completada. Procesando el archivo de audio...")

        # Construir la ruta del archivo descargado
        mp3_file = output_folder / "audio01.mp3"

        # Verificar que el archivo final existe
        if not mp3_file.exists():
            raise FileNotFoundError(f"No se pudo encontrar el archivo descargado: {mp3_file}")

        return str(mp3_file)

    except Exception as e:
        print_styled_message(f"Error durante la descarga: {str(e)}")
        raise

def cargar_variables_entorno():
    """
    Carga las variables de entorno necesarias para el script.
    """
    load_dotenv()
    variables = {
        'ai_endpoint': os.getenv('AI_SERVICE_ENDPOINT'),
        'ai_key': os.getenv('AI_SERVICE_KEY'),
        'content_safety_endpoint': os.getenv('AZURE_CONTENT_SAFETY_ENDPOINT'),
        'content_safety_key': os.getenv('AZURE_CONTENT_SAFETY_KEY'),
        'gpt_endpoint': os.getenv('AZURE_GPT_ENDPOINT'),
        'gpt_api_key': os.getenv('AZURE_GPT_API_KEY'),
        'translator_key': os.getenv('AZURE_TRANSLATOR_KEY'),
        'translator_endpoint': os.getenv('AZURE_TRANSLATOR_ENDPOINT'),
        'translator_location': os.getenv('AZURE_TRANSLATOR_LOCATION'),
        'openai_endpoint': os.getenv('AZURE_OPENAI_ENDPOINT'),
        'openai_key': os.getenv('AZURE_OPENAI_API_KEY')
    }
    if not all(variables.values()):
        raise ValueError("Todas las variables de entorno requeridas deben estar configuradas.")
    return variables

def inicializar_clientes(variables):
    """
    Inicializa los clientes de Azure necesarios.
    """
    credential = AzureKeyCredential(variables['ai_key'])
    ai_client = TextAnalyticsClient(endpoint=variables['ai_endpoint'], credential=credential)
    content_safety_client = ContentSafetyClient(
        endpoint=variables['content_safety_endpoint'],
        credential=AzureKeyCredential(variables['content_safety_key'])
    )
    gpt_client = AzureOpenAI(
        azure_endpoint=variables['gpt_endpoint'],
        api_key=variables['gpt_api_key'],
        api_version="2023-09-15-preview"
    )
    whisper_client = AzureOpenAI(
        azure_endpoint=variables['openai_endpoint'],
        api_key=variables['openai_key'],
        api_version="2023-09-01"
    )
    return ai_client, content_safety_client, gpt_client, whisper_client

def initialize_azure_clients():
    """Inicializa y retorna los clientes de Azure necesarios."""
    whisper_client = AzureOpenAI(
        azure_endpoint=os.getenv('AZURE_OPENAI_ENDPOINT'),
        api_key=os.getenv('AZURE_OPENAI_API_KEY'),
        api_version="2024-06-01"
    )

    return {
        'whisper': whisper_client
    }

def get_youtube_title(url: str) -> str:
    """
    Obtiene el título del video de YouTube.

    Args:
        url (str): URL del video de YouTube.

    Returns:
        str: Título del video.
    """
    ydl_opts = {'quiet': True}
    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        # Extraer información del video sin descargarlo
        info_dict = ydl.extract_info(url, download=False)
        return info_dict.get('title')

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

def cleanup_temp_files(file_path: Path, audio_parts: list[Path]):
    """Limpia los archivos temporales generados durante el proceso."""
    for wav_file in file_path.parent.glob("*.wav"):
        wav_file.unlink()

    for part in audio_parts:
        if part.exists():
            part.unlink()

def transcribe_audio(file_path: str, output_folder: str, ai_client: AzureOpenAI, youtube_url: Optional[str] = None) -> str:
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

        load_dotenv()
        clients = initialize_azure_clients()

        audio_parts = split_audio(wav_path)
        transcribed_parts = transcribe_audio_parts(audio_parts, clients['whisper'])

        transcribed_text = ' '.join(transcribed_parts)
        with open(output_path, 'w', encoding='utf-8') as file:
            file.write(transcribed_text)

        print_styled_message(f"Transcripción guardada en: {output_path}")

        cleanup_temp_files(file_path, audio_parts)
        return str(output_path)

    except Exception as e:
        print_styled_message(f"Error en la transcripción: {str(e)}")
        raise

def analyze_content_safety(client: ContentSafetyClient, text: str) -> dict:
    """
    Analiza el texto utilizando la API de Azure Content Safety.
    """
    request = AnalyzeTextOptions(
        text=text,
        categories=[TextCategory.HATE, TextCategory.SELF_HARM, TextCategory.SEXUAL, TextCategory.VIOLENCE]
    )

    try:
        response = client.analyze_text(request)
    except HttpResponseError as e:
        print_styled_message("Error al analizar el texto.")
        if e.error:
            print_styled_message(f"Código de error: {e.error.code}")
            print_styled_message(f"Mensaje de error: {e.error.message}")
        raise

    results = {
        "hate": next((item for item in response.categories_analysis if item.category == TextCategory.HATE), None),
        "self_harm": next((item for item in response.categories_analysis if item.category == TextCategory.SELF_HARM), None),
        "sexual": next((item for item in response.categories_analysis if item.category == TextCategory.SEXUAL), None),
        "violence": next((item for item in response.categories_analysis if item.category == TextCategory.VIOLENCE), None)
    }

    return results

def display_content_safety_results(results: dict) -> None:
    """
    Muestra un resumen consolidado de los resultados del análisis de contenido.
    """
    print_styled_message("Analizando contenido del archivo:")
    contenido_seguro = True

    for category, result in results.items():
        if result:
            severity = result.severity
            if severity >= 5:
                print_styled_message(f"Categoría: {category}, Severidad: {severity}")
                print_styled_message("El contenido no es aceptable. El script se detendrá.")
                exit(1)
            elif severity >= 4:
                print_styled_message(f"Categoría: {category}, Severidad: {severity}")
            elif severity >= 2:
                print_styled_message(f"Categoría: {category}, Severidad: {severity}")
            if severity >= 5:
                contenido_seguro = False

    if contenido_seguro:
        print_styled_message("El contenido es seguro y confiable.")

def detect_language(ai_client: TextAnalyticsClient, text_parts: list) -> str:
    """
    Detecta el idioma predominante en el texto.
    """
    languages = defaultdict(int)
    for part in text_parts:
        detected = ai_client.detect_language(documents=[{"id": "1", "text": part}])[0]
        languages[detected.primary_language.iso6391_name] += 1

    predominant_language = max(languages.items(), key=lambda x: x[1])[0]
    return predominant_language

def translate_text(text_parts: list, variables, target_language: str = "es") -> str:
    """
    Traduce el texto completo al idioma objetivo utilizando Azure Translator.
    """
    translator_key = variables['translator_key']
    translator_endpoint = variables['translator_endpoint']
    location = variables['translator_location']

    if not all([translator_key, translator_endpoint, location]):
        raise ValueError("Faltan variables de entorno para el servicio de traducción")

    path = '/translate'
    constructed_url = translator_endpoint + path

    params = {
        'api-version': '3.0',
        'from': 'en',
        'to': [target_language]
    }

    headers = {
        'Ocp-Apim-Subscription-Key': translator_key,
        'Ocp-Apim-Subscription-Region': location,
        'Content-type': 'application/json',
        'X-ClientTraceId': str(uuid.uuid4())
    }

    translated_parts = []

    print_styled_message("Iniciando la traducción del texto...")

    for idx, part in enumerate(text_parts, 1):
        body = [{'text': part}]
        response = requests.post(constructed_url, params=params, headers=headers, json=body)
        response.raise_for_status()
        translations = response.json()
        translated_parts.append(translations[0]['translations'][0]['text'])
        print_styled_message(f"Parte {idx}/{len(text_parts)} traducida.")

    print_styled_message("Traducción completada.")

    return ' '.join(translated_parts)

def improve_transcription(text: str, ai_client: AzureOpenAI, language: str = None) -> str:
    """
    Mejora el texto completo utilizando el modelo GPT-3.5-turbo-instruct de Azure OpenAI.
    """
    if not text:
        raise ValueError("El texto de entrada está vacío")

    max_tokens = 1000  # Límite de tokens por fragmento
    text_chunks = split_text_gpt(text, max_tokens)

    # Definir el prompt según el idioma
    if language == 'es':
        prompt = (
            "Actúa como un especialista en optimización de textos en español. "
            "Cuando te proporcione contenido de texto de diversas fuentes, analízalo y mejóralo de la siguiente manera:\n"
            "1. Primero, identifica el tema principal, estilo de escritura y nivel técnico del contenido\n"
            "2. Elimina anuncios, palabras de relleno, marcas de tiempo y contenido fuera de tema\n"
            "3. Organiza los puntos clave usando formato apropiado (viñetas, números, párrafos)\n"
            "4. Preserva la terminología especializada y acrónimos, asegurando su uso correcto\n"
            "5. Estandariza valores numéricos y ecuaciones en notación apropiada\n"
            "6. Corrige gramática, ortografía y puntuación manteniendo la voz del autor\n"
            "7. Estructura el contenido con encabezados y secciones claras donde sea apropiado\n"
            "8. Mantén toda la precisión técnica e información esencial\n"
            "9. Mantén el texto en español\n"
            "10. Finaliza con una breve verificación de calidad\n"
            "Mejora el siguiente texto:\n\n"
        )
    else:
        prompt = (
            "I want you to act as a text optimization specialist. "
            "When I provide you with raw text content from various sources, analyze it and improve it in the following structured way:\n"
            "1. First, identify the main topic, writing style, and technical level of the content\n"
            "2. Remove all advertisements, filler words, timestamps, and off-topic content\n"
            "3. Organize the key points using appropriate formatting (bullets, numbers, paragraphs)\n"
            "4. Preserve specialized terminology and acronyms while ensuring they're used correctly\n"
            "5. Standardize numerical values and equations into proper notation\n"
            "6. Fix grammar, spelling, and punctuation while maintaining the author's voice\n"
            "7. Structure the content with clear headings and sections where appropriate\n"
            "8. Maintain all technical accuracy and essential information\n"
            "9. Keep the text in its original language\n"
            "10. End with a brief quality check\n"
            "Improve the following text:\n\n"
        )

    improved_texts = []

    print_styled_message("Mejorando la transcripción...")

    for idx, chunk in enumerate(text_chunks, 1):
        try:
            response = ai_client.completions.create(
                model="gpt-35-turbo-instruct",
                prompt=f"{prompt}{chunk}",
                temperature=0,
                max_tokens=max_tokens,
                top_p=0.9,  # Ajuste del parámetro top_p para mejorar la coherencia
                frequency_penalty=0,
                presence_penalty=0,
                stop=None
            )
            improved_text = response.choices[0].text.strip()
            improved_texts.append(improved_text)
            print_styled_message(f"Fragmento {idx}/{len(text_chunks)} mejorado.")
        except Exception as e:
            print_styled_message(f"Error al mejorar el texto: {str(e)}")
            raise

    print_styled_message("Mejora de transcripción completada.")

    return ' '.join(improved_texts)

def main():
    """
    Función principal que maneja el flujo de ejecución del programa.
    """
    try:
        # Cargar variables de entorno
        variables = cargar_variables_entorno()

        # Inicializar clientes
        ai_client, content_safety_client, gpt_client, whisper_client = inicializar_clientes(variables)

        # Solicitar URL de YouTube al usuario
        youtube_url = input("Ingrese la URL del video de YouTube: ")
        audio_folder = Path('audio')
        audio_folder.mkdir(exist_ok=True)

        # Descargar y procesar el audio
        original_file_path = download_youtube_audio(youtube_url, str(audio_folder))
        trimmed_file_path, is_trimmed = trim_start(str(original_file_path))

        file_to_transcribe = str(trimmed_file_path)
        output_folder = Path('reviews')
        output_folder.mkdir(exist_ok=True)

        # Transcribir el audio
        print_styled_message('\nTranscribiendo archivo de audio: ' + os.path.basename(file_to_transcribe))
        output_path = transcribe_audio(file_to_transcribe, str(output_folder), whisper_client, youtube_url)
        print_styled_message('Transcripción completada y guardada en: ' + output_path)
        text = read_file(output_path)

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
        improved_text = improve_transcription(text_to_improve, gpt_client, language=language_to_improve)

        # Guardar el texto mejorado
        improved_path = Path(output_path).parent / f"improved_{Path(output_path).name}"
        with open(improved_path, 'w', encoding='utf-8') as f:
            f.write(improved_text)
        print_styled_message(f"Texto mejorado guardado en: {improved_path}")

    except Exception as ex:
        print_styled_message(f"Error: {str(ex)}")

if __name__ == "__main__":
    main()