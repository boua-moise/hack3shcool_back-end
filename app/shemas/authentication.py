from enum import Enum
from fastapi import File
from pydantic import BaseModel

class Role(str,Enum):
    teacher = "teacher"
    student = "student"

class AuteurSchema(BaseModel):
    nom:str
    prenom:str
    url_image:str|None
    biographie:str
    mail:str
    role:str

class RegisterSchema(BaseModel):
    nom:str
    prenom:str
    role:Role
    biographie:str
    mail:str
    password:str
    conf_password:str


class LoginSchema(BaseModel):
    mail:str
    password:str
    role:Role

class UserSchema(BaseModel):
    nom:str
    prenom:str
    url_image:str|None
    biographie:str
    mail:str

class AllUserSchema(BaseModel):
    users:list[UserSchema]