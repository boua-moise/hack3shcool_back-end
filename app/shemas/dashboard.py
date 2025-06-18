from pydantic import BaseModel
from fastapi import File
from app.shemas.cours import AllCoursSchema, SectionSchema

class StudentCoursShema(BaseModel):
    encours:list[AllCoursSchema]
    terminer:list[AllCoursSchema]

class CoursSchema(BaseModel):
    titre:str
    description:str

class ResponseCoursSchema(BaseModel):
    cours:list[CoursSchema]


class AddCoursSchema(BaseModel):
    titre:str
    description:str
    image:bytes = None
    sections:list[SectionSchema]

