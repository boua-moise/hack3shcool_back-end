import datetime

from prisma.models import Cours, Student, SuiviCours
from fastapi import HTTPException, status
from app.shemas.authentication import Role
from app.shemas.cours import Status


class CoursService:
    @staticmethod
    async def get_all_cours():

        """
        Elle charge tous les cours dans la BD et les envoie
        au niveau du front-end.
        :return: All cours in data base
        """

        all_cours = await Cours.prisma().find_many(include={"auteur":True})

        return {"all_cours": all_cours}



    @staticmethod
    async def details_cours(cours_id:int):

        """
        Renvoie tous un cours avec ses détails:
        -Trite du cours
        -Titre des sections
        -Bref explication et objectifs du cours
        -Auteur du cours
        :param cours_id:
        :return: cours avec ses relations
        """

        cours = await Cours.prisma().find_unique(where={"id":cours_id}, include={"sections":True, "auteur":True})

        if not cours:
            raise HTTPException(detail="Ce cours n'existe pas", status_code=status.HTTP_404_NOT_FOUND)

        return {"detail_cours": cours}


    @staticmethod
    async def register_of_cours(cours_id:int, user_info:dict):

        if (not user_info) or (user_info["role"] != Role.student):
            raise HTTPException(detail="Accès non autorisé", status_code=status.HTTP_401_UNAUTHORIZED)

        user = await Student.prisma().find_unique(where={"id":user_info["id"]}, include={"coursSuivis":True})

        cours_user = [cours.id for cours in user.coursSuivis]

        if cours_id in cours_user:
            raise HTTPException(detail="Déjà enrégistré", status_code=status.HTTP_409_CONFLICT)

        await Student.prisma().update(
            where={"id": user_info["id"]},

            data={
                "coursSuivis":{
                    'connect': [{"id":cours_id}]
                }
            }
        )

        await SuiviCours.prisma().create(data={"coursId":cours_id, "studentId":user_info["id"], "statut":Status.encours})

        return {"response": "Utilisateur enregistré au cours avec succès"}

    

    @staticmethod
    async def view_cours(cours_id:int, user_info):

        if (not user_info) or (user_info.get("role") != Role.student):
            raise HTTPException(detail="Accès non autorisé", status_code=status.HTTP_401_UNAUTHORIZED)

        """
        Elle vérifie d'abord si l'utilisateur est connecté.
        Donc, elle dépend de la connexion.
        Elle renvoie toutes les sections liées à un cours au front-end.
        :return: Une section
        """

        user = await Student.prisma().find_unique(where={"id": user_info["id"]}, include={"coursSuivis": True})

        cours_user = [cours.id for cours in user.coursSuivis]

        if not (cours_id in cours_user):
            raise HTTPException(detail="Accès non autorisé", status_code=status.HTTP_401_UNAUTHORIZED)

        cours_complet = await Cours.prisma().find_unique(where={"id":cours_id}, include={"sections":True, "auteur":True})

        return {"cours_complet": cours_complet}



    @staticmethod
    async def update_cours_following(cours_id, user_info:dict):

        if (not user_info) or (user_info["role"] != Role.student):
            raise HTTPException(detail="Accès non autorisé", status_code=status.HTTP_401_UNAUTHORIZED)

        user = await Student.prisma().find_unique(where={"id":user_info["id"]}, include={"suiviCours":True, "coursSuivis":True})

        cours_user = [cours.id for cours in user.coursSuivis]

        if not (cours_id in cours_user):
            raise HTTPException(detail="Accès non autorisé", status_code=status.HTTP_401_UNAUTHORIZED)

        following_cours = [id.id for id in user.suiviCours if id.coursId == cours_id]

        if not following_cours:
            raise HTTPException(detail="Accès non autorisé", status_code=status.HTTP_401_UNAUTHORIZED)


        await SuiviCours.prisma().update(where={"id":following_cours[0]}, data={"statut": Status.terminer, "fin":datetime.datetime.now()})

        return {"response":"Cours terminé avec succès"}


