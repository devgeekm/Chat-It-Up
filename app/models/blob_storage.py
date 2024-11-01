from pydantic import BaseModel, ConfigDict

class FileUploadRequest(BaseModel):
    filename: str  # Puede ser .mp3, .wav, .txt, .doc, .pdf, etc.
    file_data: bytes
    model_config = ConfigDict(json_schema_extra={})