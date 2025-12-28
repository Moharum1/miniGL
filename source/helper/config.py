from pydantic_settings import BaseSettings

class Setting(BaseSettings):

    APP_NAME: str
    APP_VERSION: str
    FILE_ALLOWED_EXTENSIONS: list[str]
    FILE_MAX_SIZE_MB: int
    DEFAULT_CHUNK_SIZE: int

    MONGODB_URI: str
    DATABASE_NAME: str

    class Config:
        env_file = ".env"

def get_settings() -> Setting:
    return Setting()