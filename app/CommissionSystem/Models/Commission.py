from pydantic import BaseModel, Field
from bson import ObjectId
from .PyObjectId import PyObjectId


class Commission(BaseModel):
    id: PyObjectId = Field(default_factory=PyObjectId, alias="_id")
    name: str = Field(...)
    files: list[PyObjectId] = Field(...) # _id of the files in mongofs

    class Config:
        allow_population_by_field_name = True
        arbitrary_types_allowed = True
        json_encoders = {ObjectId: str}