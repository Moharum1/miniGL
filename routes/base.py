from fastapi import APIRouter
import os

base_router = APIRouter(
    prefix="/api/v1", # prefix for all routes in this router
    tags=["V1"] # tag for grouping routes for documentation
)

@base_router.get("/")
async def app_base():
    app_name = os.getenv("APP_NAME", "miniGL")
    app_version = os.getenv("APP_VERSION", "0.0")

    return {"app_name": app_name, "app_version": app_version}