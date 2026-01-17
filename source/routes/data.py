from fastapi import APIRouter, Depends, UploadFile, status, Request
from helper.config import Setting, get_settings
from controllers import DataController, ProjectController, ProcessController
from fastapi.responses import JSONResponse
from routes.schemes import ProcessRequest
from models.ProjectModule import ProjectModule
from models.ChunckModel import ChunkModel
from models.DB.project import Project
from models.DB.dataChunk import DataChunk
import aiofiles

data_router = APIRouter(
    prefix="/api/v1/data", # prefix for all routes in this router
    tags=["Data"] # tag for grouping routes for documentation
)

@data_router.post("/upload/{project_id}")
async def upload_file(request : Request, project_id: str, file: UploadFile, 
                      app_setting: Setting = Depends(get_settings)):
    
    project_module = await ProjectModule.create_module(request.app.database)
    project = await project_module.create_project(Project(project_id=project_id))

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
            "file_path": file_name,
        }
    )

@data_router.post("/process/{project_id}")
async def process_file(request : Request, project_id: str, Process_request: ProcessRequest):
    filename = Process_request.file_id
    chunk_size = Process_request.chunk_size
    overlap_size = Process_request.overlap_size
    do_reset = Process_request.reset

    project_module = await ProjectModule.create_module(request.app.database)
    project = await project_module.get_project_by_id(project_id)

    chunk_model = await ChunkModel.create_module(request.app.database)

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
    
    file_chunks_records = [
        DataChunk(chunk_text=chunk.page_content, metadata=chunk.metadata, chunk_order= i + 1, project_id=project.project_id) 
        for i, chunk in enumerate(chunks)
    ]
    if do_reset:
        await chunk_model.delete_chunks_by_project_id(project.project_id)

    
    no_of_records = await chunk_model.insert_mini_chunks(file_chunks_records)

    return JSONResponse(
        status_code=status.HTTP_200_OK,
        content={
            "detail": f"{no_of_records} chunks created successfully."
        }
    )