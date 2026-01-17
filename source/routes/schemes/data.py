from pydantic import BaseModel, Field
from typing import Optional

class ProcessRequest(BaseModel):
    chunk_size : Optional[int] = Field(default=1024*1024)  # Default chunk size of 1 MB
    overlap_size : Optional[int] = Field(default=100)
    reset : Optional[bool] = Field(default=False)
