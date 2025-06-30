from pydantic import BaseModel
from enum import Enum

class Level(str, Enum):
    facile = "facile"
    moyenne = "moyenne"
    difficile = "difficile"

class Status(str,Enum):
    encours = "encours"
    terminer = "terminer"

class SectionSchema(BaseModel):
    titre:str
    url_image:str|None
    contenu:str

class SectionSchemaOfDetail(BaseModel):
    titre:str

class AuteurSchema(BaseModel):
    nom:str
    biographie:str
    prenom:str
    url_image:str|None
    mail:str

class AllCoursSchema(BaseModel):
    id:int
    auteur:AuteurSchema
    titre:str
    description:str
    image:str|None
    url_image:str|None
    niveau:Level
    duree:str


class ResponseAllCoursSchema(BaseModel):
    all_cours:list[AllCoursSchema]


class DetailCoursSchema(BaseModel):
    auteur:AuteurSchema
    titre:str
    url_image:str|None
    niveau:Level
    duree:str
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