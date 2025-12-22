from fastapi import APIRouter, Depends, UploadFile, status
from helper.config import Setting, get_settings
from controllers import DataController, ProjectController
from fastapi.responses import JSONResponse
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
    print("Project Path:", project_path)
    file_path = os.path.join(project_path, file.filename)

    async with aiofiles.open(file_path, 'wb') as out_file:
        while chunk := await file.read(app_setting.DEFAULT_CHUNK_SIZE):
            await out_file.write(chunk)

    return JSONResponse(
        status_code=status.HTTP_200_OK,
        content={
            "detail": "File uploaded successfully.",
            "file_path": file_path
        }
    )
    