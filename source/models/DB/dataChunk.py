from pydantic import BaseModel, Field
from typing import Optional
from bson.objectid import ObjectId

class DataChunk(BaseModel):
    id : Optional[ObjectId] = Field(None, alias="_id")
    chunk_order : int = Field(..., gt=0)

    chunk_text : str = Field(..., min_length=1)
    metadata : dict
    project_id : str

    @classmethod
    def get_index(cls):
        return [{
            "key" : [("project_id", 1)],
            "name" : "chunk_project_id_index_1",
            "unique" : False
        }]


    class Config:
        arbitrary_types_allowed = True