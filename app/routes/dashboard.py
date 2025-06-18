from fastapi import APIRouter, Depends
from typing import Annotated
from app.services.dashboard import DashboardService
from app.security.security import permission_access
from app.shemas.dashboard import StudentCoursShema, ResponseCoursSchema, AddCoursSchema



dashboard_router = APIRouter(prefix="/dashboard", tags=["Dashboard"], dependencies=[Depends(permission_access)])


@dashboard_router.get("/student", response_model=StudentCoursShema)
async def student(user:Annotated[dict, Depends(permission_access)]):
    return await DashboardService.dashboard_student(user)


@dashboard_router.delete("/student/cours/{id}/erase")
async def erase(id:int, user:Annotated[dict, Depends(permission_access)]):
    return await DashboardService.erase(id, user)


@dashboard_router.get("/teacher", response_model=ResponseCoursSchema)
async def teacher(user:Annotated[dict, Depends(permission_access)]):
    return await DashboardService.teacher(user)


@dashboard_router.post("/teacher/addcours")
async def addcours(cours:AddCoursSchema,user:Annotated[dict, Depends(permission_access)]):
    return await DashboardService.addcours(cours, user)


@dashboard_router.delete("/teacher/cours/{id}/delete")
async def delete_cours(id:int, user:Annotated[dict, Depends(permission_access)]):
    return await DashboardService.delete_cours(id, user)

