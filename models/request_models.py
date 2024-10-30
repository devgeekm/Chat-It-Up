from pydantic import BaseModel

# Azure Blob Storage
class FileUploadRequest( BaseModel ):
    filename: str
    file_data: bytes

# Azure OpenAI
class ChatRequest( BaseModel ):
    message: str