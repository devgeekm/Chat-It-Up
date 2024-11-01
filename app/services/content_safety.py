from azure.core.exceptions import HttpResponseError, ResourceNotFoundError
from azure.ai.contentsafety import ContentSafetyClient
from azure.ai.contentsafety.models import AnalyzeTextOptions, TextCategory
from app.utils.file_utils import print_styled_message, read_file
from urllib.parse import unquote, urlparse
from azure.storage.blob import BlobServiceClient
import os

# Inicialización del cliente de Blob Storage
# azure_blob_connection_string = os.getenv("AZURE_BLOB_CONNECTION_STRING")
# container_name = os.getenv("AZURE_BLOB_CONTAINER_NAME")
# blob_service_client = BlobServiceClient.from_connection_string(azure_blob_connection_string)
# container_client = blob_service_client.get_container_client(container_name)

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