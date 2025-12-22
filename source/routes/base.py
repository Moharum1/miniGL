from fastapi import APIRouter, Depends
from helper.config import Setting, get_settings

base_router = APIRouter(
    prefix="/api/v1", # prefix for all routes in this router
    tags=["V1"] # tag for grouping routes for documentation
)

@base_router.get("/")
async def app_base(app_setting : Setting = Depends(get_settings)):
    return {"app_name": app_setting.APP_NAME, "app_version": app_setting.APP_VERSION}


