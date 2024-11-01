from pydantic import BaseModel

class FileUploadRequest(BaseModel):
    filename: str  # Puede ser .mp3, .wav, .txt, .doc, .pdf, etc.
    file_data: bytes

    class Config:
        schema_extra = {
            "example": {
                "filename": "example.mp3",
                "file_data": "base64encodedstring"
            }
        }