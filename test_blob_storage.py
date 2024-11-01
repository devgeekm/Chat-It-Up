import os
from azure.storage.blob import BlobServiceClient
# importar variales de entorno
from dotenv import load_dotenv
# cargar variables de entorno
load_dotenv()

# Obtener la cadena de conexión desde las variables de entorno
azure_blob_connection_string = os.getenv('AZURE_BLOB_CONNECTION_STRING')
container_name = os.getenv("AZURE_BLOB_CONTAINER_NAME")

if not azure_blob_connection_string:
    raise ValueError("La variable de entorno AZURE_BLOB_CONNECTION_STRING no está configurada")

if not container_name:
    raise ValueError("La variable de entorno AZURE_BLOB_CONTAINER_NAME no está configurada")

# Inicializar el cliente de Blob Storage
blob_service_client = BlobServiceClient.from_connection_string(azure_blob_connection_string)
container_client = blob_service_client.get_container_client(container_name)

# Listar los blobs en el contenedor
try:
    blobs_list = container_client.list_blobs()
    print(f"Blobs en el contenedor '{container_name}':")
    for blob in blobs_list:
        print(f" - {blob.name}")
except Exception as e:
    print(f"Error al conectar con Azure Blob Storage: {str(e)}")
