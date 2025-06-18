from fastapi import FastAPI
from prisma import Prisma
from contextlib import asynccontextmanager

from app.routes.authentication import auth_router
from app.routes.cours import cours_router
from app.routes.dashboard import dashboard_router

prisma = Prisma(auto_register=True)

@asynccontextmanager
async def lifespan(app:FastAPI):
    await prisma.connect()
    yield
    if prisma.is_connected():
        await prisma.disconnect()

app = FastAPI(lifespan=lifespan)

app.include_router(auth_router)
app.include_router(cours_router)
app.include_router(dashboard_router)