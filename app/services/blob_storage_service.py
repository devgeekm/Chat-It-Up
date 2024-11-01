import os
from azure.storage.blob import BlobServiceClient, BlobClient, ContainerClient
from app.models.blob_storage import FileUploadRequest
from dotenv import load_dotenv
from pathlib import Path
from urllib.parse import urlparse, unquote

# Cargar variables de entorno
load_dotenv()
azure_blob_connection_string = os.getenv("AZURE_BLOB_CONNECTION_STRING")
container_name = os.getenv("AZURE_BLOB_CONTAINER_NAME")

# Inicializar el cliente de Blob Storage
blob_service_client = BlobServiceClient.from_connection_string(azure_blob_connection_string)
container_client = blob_service_client.get_container_client(container_name)

def upload_file_to_blob(file_request: FileUploadRequest) -> str:
    """
    Sube un archivo a Blob Storage y permite sobrescribirlo si ya existe.
    Retorna la URL pública del blob.
    """
    try:
        blob_client = container_client.get_blob_client(file_request.filename)
        blob_client.upload_blob(file_request.file_data, overwrite=True)

        # Construir la URL completa del blob
        blob_url = f"https://{blob_service_client.account_name}.blob.core.windows.net/{container_name}/{file_request.filename}"
        return blob_url
    except Exception as e:
        raise RuntimeError(f"Error al subir el archivo a Blob Storage: {str(e)}")

def download_file_from_blob(blob_url: str) -> Path:
    """
    Descarga un archivo desde Blob Storage y lo guarda temporalmente en /tmp.
    """
    try:
        # Extraer el nombre del blob desde la URL
        parsed_url = urlparse(blob_url)
        blob_name = parsed_url.path.split('/')[-1]

        # Usar el container_name configurado en lugar de extraerlo de la URL
        blob_client = blob_service_client.get_blob_client(container=container_name, blob=blob_name)

        # Descargar el blob al directorio temporal
        download_path = Path("/tmp") / blob_name
        with open(download_path, "wb") as download_file:
            download_file.write(blob_client.download_blob().readall())
        return download_path
    except Exception as e:
        raise RuntimeError(f"Error al descargar el archivo desde Blob Storage: {str(e)}")
    
def download_text_file_from_blob(blob_url: str) -> Path:
    """
    Descarga un archivo de texto desde Blob Storage con manejo mejorado de caracteres especiales.
    """
    try:
        # Decodificar la URL y obtener el nombre del blob
        decoded_url = unquote(blob_url)
        parsed_url = urlparse(decoded_url)
        
        # Extraer el path completo del blob manteniendo la estructura
        blob_name = parsed_url.path.lstrip('/')
        
        # Remover el nombre del contenedor si está presente en el path
        if blob_name.startswith(f"{container_name}/"):
            blob_name = blob_name[len(container_name)+1:]
            
        print(f"Intentando acceder al blob: {blob_name}")
        
        # Crear el blob client directamente con el nombre completo
        blob_client = container_client.get_blob_client(blob_name)
        
        # Descargar el contenido sin verificar existencia
        try:
            blob_data = blob_client.download_blob()
            
            # Usar el nombre original del archivo para la descarga local
            local_filename = Path(blob_name).name
            download_path = Path("/tmp") / local_filename
            
            with open(download_path, "wb") as download_file:
                download_file.write(blob_data.readall())
            
            print(f"Archivo descargado exitosamente a: {download_path}")
            return download_path
            
        except Exception as download_error:
            print(f"Error al descargar el blob: {str(download_error)}")
            print(f"URL original: {blob_url}")
            print(f"URL decodificada: {decoded_url}")
            print(f"Nombre del blob: {blob_name}")
            raise FileNotFoundError(f"No se pudo acceder al blob: {blob_name}")
            
    except Exception as e:
        print(f"Error general: {str(e)}")
        raise RuntimeError(f"Error al procesar la descarga: {str(e)}")

def delete_file_from_blob(blob_url: str):
    """
    Elimina un archivo de Blob Storage usando su URL.
    """
    try:
        # Extraer el nombre del blob desde la URL
        parsed_url = urlparse(blob_url)
        blob_name = parsed_url.path.split('/')[-1]

        # Usar el container_name configurado en lugar de extraerlo de la URL
        blob_client = blob_service_client.get_blob_client(container=container_name, blob=blob_name)
        blob_client.delete_blob()
    except Exception as e:
        raise RuntimeError(f"Error al eliminar el archivo de Blob Storage: {str(e)}")