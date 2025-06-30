from pydantic import BaseModel
from app.shemas.cours import AllCoursSchema, SectionSchema
from enum import Enum

class Level(str, Enum):
    facile = "facile"
    moyenne = "moyenne"
    difficile = "difficile"

class StudentCoursShema(BaseModel):
    encours:list[AllCoursSchema]
    terminer:list[AllCoursSchema]

class CoursSchema(BaseModel):
    id:int
    titre:str
    niveau:Level
    image:str
    duree:str
    description:str

class ResponseCoursSchema(BaseModel):
    cours:list[CoursSchema]

class AddCoursSchema(BaseModel):
    titre:str
    description:str
    url_image:str
    niveau:Level
    duree:str
    sections:list[SectionSchema]
