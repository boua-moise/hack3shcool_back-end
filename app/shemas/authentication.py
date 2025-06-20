from enum import Enum
from fastapi import File
from pydantic import BaseModel

class Role(str,Enum):
    teacher = "teacher"
    student = "student"

class RegisterSchema(BaseModel):
    nom:str
    prenom:str
    role:Role
    biographie:str = None
    mail:str
    image:bytes = None
    password:str
    conf_password:str


class LoginSchema(BaseModel):
    mail:str
    password:str
    role:Role
