from pydantic import BaseModel, Field, field_validator
from typing import Optional
from bson.objectid import ObjectId

class DataChunk(BaseModel):
    _id : Optional[ObjectId]
    project_id : ObjectId
    chunk_order : int = Field(..., gt=0)

    chunk_text : str = Field(..., min_length=1)
    metadata : dict
    
    class Config:
        arbitrary_types_allowed = True