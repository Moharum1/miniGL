from pydantic import BaseModel, Field
from typing import Optional
from bson.objectid import ObjectId
from datetime import datetime

class Asset(BaseModel):
    id : Optional[ObjectId] = Field(None, alias="_id")
    asset_name : str = Field(..., min_length=1)
    asset_type : str = Field(..., min_length=1)
    asset_size : int = Field(ge=0, default=None)
    asset_pushed_at : datetime = Field(default=datetime.now())
    asset_config : dict = Field(default=None)
    project_id : str

    @classmethod
    def get_index(cls):
        return [{
            "key" : [("asset_project_id", 1)],
            "name" : "asset_project_id_index_1",
            "unique" : False
        },
        {
            "key" : [("asset_name", 1)],
            "name" : "asset_name_index_1",
            "unique" : True
        }
        ]

    class Config:
        arbitrary_types_allowed = True