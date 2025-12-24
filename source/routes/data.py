from fastapi import APIRouter, Depends, UploadFile, status
from helper.config import Setting, get_settings
from controllers import DataController, ProjectController, ProcessController
from fastapi.responses import JSONResponse
from routes.schemes import ProcessRequest
import os
import aiofiles

data_router = APIRouter(
    prefix="/api/v1/data", # prefix for all routes in this router
    tags=["Data"] # tag for grouping routes for documentation
)

@data_router.post("/upload/{project_id}")
async def upload_file(project_id: str, file: UploadFile, 
                      app_setting: Setting = Depends(get_settings)):

    data_controller = DataController()
    is_valid, message = data_controller.validate_data(file)
    if not is_valid:
        return JSONResponse(
            status_code=status.HTTP_400_BAD_REQUEST,
            content={
                "detail": message
            }
        )
    
    project_path = ProjectController().get_project_pass(project_id)
    file_name, file_path = data_controller.generate_unique_filename(file.filename, project_id)

    try:
        async with aiofiles.open(file_path, 'wb') as out_file:
            while chunk := await file.read(app_setting.DEFAULT_CHUNK_SIZE):
                await out_file.write(chunk)
    except Exception as e:
        return JSONResponse(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            content={
                "detail": f"An error occurred while saving the file: {str(e)}"
            }
        )

    return JSONResponse(
        status_code=status.HTTP_200_OK,
        content={
            "detail": "File uploaded successfully.",
            "file_path": file_name
        }
    )

@data_router.post("/process/{project_id}")
async def process_file(project_id: str, request: ProcessRequest):
    filename = request.file_id
    chunk_size = request.chunk_size
    overlap_size = request.overlap_size

    process_controller = ProcessController(project_id)
    chunks = process_controller.process_file_content(
        filename, 
        chunk_size, 
        overlap_size
    )
    if chunks is None:
        return JSONResponse(
            status_code=status.HTTP_400_BAD_REQUEST,
            content={
                "detail": "Unsupported file type or unable to read file content."
            }
        )

    return JSONResponse(
        status_code=status.HTTP_200_OK,
        content={
            "detail": "File processed successfully.",
            "chunks": [chunk.page_content for chunk in chunks],
            "Meta": [chunk.metadata for chunk in chunks],
            "Source": [chunk.metadata['source'] for chunk in chunks]
        }
    )