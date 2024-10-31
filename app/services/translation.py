import requests
import uuid
import os
from app.utils.file_utils import print_styled_message

def translate_text(text_parts: list, clients, target_language: str = "es") -> str:
    """
    Traduce el texto completo al idioma objetivo utilizando Azure Translator.
    """
    translator_key = os.getenv('AZURE_TRANSLATOR_KEY')
    translator_endpoint = os.getenv('AZURE_TRANSLATOR_ENDPOINT')
    location = os.getenv('AZURE_TRANSLATOR_LOCATION')

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