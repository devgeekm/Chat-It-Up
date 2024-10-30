import os
from azure.storage.blob import BlobServiceClient
from fastapi import UploadFile
from dotenv import load_dotenv

load_dotenv()
azure_blob_connection_string = os.getenv("AZURE_BLOB_CONNECTION_STRING")
container_name = os.getenv("AZURE_BLOB_CONTAINER_NAME")

blob_service_client = BlobServiceClient.from_connection_string( azure_blob_connection_string )
container_client = blob_service_client.get_container_client( container_name )

def upload_file_to_blob( file: UploadFile ) -> str:
    blob_client = container_client.get_blob_client( file.filename )
    
    blob_client.upload_blob( file.file, overwrite=True )
    
    return blob_client.url