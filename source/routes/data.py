from fastapi import APIRouter, Depends, UploadFile
from helper.config import Setting, get_settings
from controllers import DataController

data_router = APIRouter(
    prefix="/api/v1/data", # prefix for all routes in this router
    tags=["Data"] # tag for grouping routes for documentation
)

@data_router.get("/upload/{project_id}")
async def upload_file(project_id: str, file: UploadFile, 
                      app_setting: Setting = Depends(get_settings)):

    data_controller = DataController()
    is_valid, message = data_controller.validate_data(file)
    if not is_valid:
        return {"success": False, "message": message}
    
    # Process the file (e.g., save to disk, database, etc.)

    