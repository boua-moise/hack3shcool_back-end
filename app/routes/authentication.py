from typing import Annotated
from app.security.security import get_current_user
from fastapi import APIRouter
from prisma.models import Student, Teacher
from fastapi import Depends
from app.services.authentication import AuthService
from app.shemas.authentication import RegisterSchema, LoginSchema
from app.shemas.cours import AuteurSchema

auth_router = APIRouter(prefix="/auth", tags=["Authentification"])

@auth_router.post("/register")
async def register(user:RegisterSchema):
    return await AuthService.register(user)

@auth_router.post("/login")
async def login(user:LoginSchema):
    return await AuthService.login(user)

@auth_router.get("/", response_model=AuteurSchema)
async def current_user(user:Annotated[Student|Teacher, Depends(get_current_user)]):
    return await AuthService.current_user(user)
