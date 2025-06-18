from typing import Annotated

from fastapi import APIRouter, Depends

from app.services.cours import CoursService
from app.shemas.cours import ResponseAllCoursSchema, ResponseDetailCoursSchema, ResponseViewCoursSchema
from app.security.security import permission_access

cours_router = APIRouter(prefix="/cours", tags=["Cours"])




@cours_router.get("/list", response_model=ResponseAllCoursSchema)
async def all_cours():

    """
    Elle charge tous les cours dans la BD et
    les envoie au niveau du front-end.
    :return:
    """
    return await CoursService.get_all_cours()



@cours_router.get("/{cours_id}/details", response_model=ResponseDetailCoursSchema)
async def details_cours(cours_id:int):

    """
    Renvoie tous un cours avec ses détails:
    -Trite du cours
    -Titre des sections
    -Bref explication et objectifs du cours
    -Auteur du cours
    :param cours_id:
    :return:
    """
    return await CoursService.details_cours(cours_id)



@cours_router.post("/{cours_id}/register")
async def register_cours(cours_id:int, user:Annotated[dict, Depends(permission_access)]):
    return await CoursService.register_of_cours(cours_id, user)


@cours_router.get("/{cours_id}/view", response_model=ResponseViewCoursSchema)
async def view_cours(cours_id:int, user:Annotated[dict, Depends(permission_access)]):

    """
    Elle vérifie d'abord si l'utilisateur est connecté.
    Donc, elle dépend de la connexion.
    Elle renvoie toutes les sections liées à un cours au front-end.
    :param cours_id:
    :param user:
    :return:
    """
    return await CoursService.view_cours(cours_id, user)



@cours_router.put("/{cours_id}/update")
async def register_cours(cours_id:int, user:Annotated[dict, Depends(permission_access)]):
    return await CoursService.update_cours_following(cours_id, user)

