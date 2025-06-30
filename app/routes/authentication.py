from typing import Annotated
from app.security.security import get_current_user, parse_register_schema
from fastapi import APIRouter, UploadFile, File, Request
from prisma.models import Student, Teacher
from fastapi import Depends
import json
from app.services.authentication import AuthService
from app.shemas.authentication import RegisterSchema, LoginSchema
from app.shemas.authentication import AuteurSchema, AllUserSchema, Role

auth_router = APIRouter(prefix="/auth", tags=["Authentification"])

@auth_router.post("/register")
async def register(user: RegisterSchema = Depends(parse_register_schema),image: UploadFile = File(...)):
    return  await AuthService.register(user, image)

@auth_router.post("/login")
async def login(user:LoginSchema):
    return await AuthService.login(user)

@auth_router.get("/", response_model=AuteurSchema)
async def current_user(user:Annotated[Student|Teacher, Depends(get_current_user)]):
    return await AuthService.current_user(user)

@auth_router.get("/all/{type_user}", response_model=AllUserSchema)
async def all_student(type_user:Role):
    return await AuthService.all_student(type_user)
