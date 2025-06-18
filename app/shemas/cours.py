from pydantic import BaseModel
from enum import Enum

class Status(str,Enum):
    encours = "encours"
    terminer = "terminer"

class SectionSchema(BaseModel):
    titre:str
    contenu:str

class SectionSchemaOfDetail(BaseModel):
    titre:str

class AuteurSchema(BaseModel):
    nom:str
    prenom:str
    biographie:str
    mail:str

class AllCoursSchema(BaseModel):
    auteur:AuteurSchema
    titre:str
    description:str

    


class ResponseAllCoursSchema(BaseModel):
    all_cours:list[AllCoursSchema]


class DetailCoursSchema(BaseModel):
    auteur:AuteurSchema
    titre:str
    description:str
    sections:list[SectionSchemaOfDetail]

class ResponseDetailCoursSchema(BaseModel):
    detail_cours: DetailCoursSchema


class ViewCoursSchema(BaseModel):
    auteur:AuteurSchema
    titre:str
    sections:list[SectionSchema]

class ResponseViewCoursSchema(BaseModel):
    cours_complet: ViewCoursSchema