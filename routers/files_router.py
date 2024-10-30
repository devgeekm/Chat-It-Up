from fastapi import APIRouter, UploadFile, File, HTTPException
from services.blob_storage_service import upload_file_to_blob
from typing import List

router = APIRouter()

@router.post('/upload-files')
async def upload_files( files: List[UploadFile] = File(...) ):
    try:
        for file in files:
            print(f"Uploading {file.filename} to blob storage...")
            upload_file_to_blob( file )
            print(f"Successfully uploaded {file.filename}")
        return { 'status': 'success' }
    except Exception as e:
        # print(f"Failed to upload {file.filename}: {e}")
        raise HTTPException( status_code=500, detail=str(e) )