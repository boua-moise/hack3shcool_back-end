from prisma.models import Student, SuiviCours, Teacher, Cours, Section
from fastapi import HTTPException, status
from app.shemas.cours import Status
from app.shemas.authentication import Role
from app.shemas.dashboard import AddCoursSchema
from app.security.security import save_local_image


class DashboardService:
    
    @staticmethod
    async def dashboard_student(user_info):
        if (not user_info) or (user_info["role"] != Role.student):
            raise HTTPException(detail="Accès non autorisé", status_code=status.HTTP_401_UNAUTHORIZED)
            
        all_cours = await Student.prisma().find_unique(where={"id":user_info["id"]}, include={"coursSuivis":{"include":{"auteur":True}}, "suiviCours": True})

        coursid_terminer = [el.coursId for el in all_cours.suiviCours if el.statut == Status.terminer]
        
        cours = {
            "encours": [],
            "terminer": []
        }

        for element in all_cours.coursSuivis:
            if element.id in coursid_terminer:
                cours["terminer"].append(element)
            else:
                cours["encours"].append(element)

        return cours




    @staticmethod
    async def erase(cours_id:int, user_info):


        if (not user_info) or (user_info["role"] != Role.student):
            raise HTTPException(detail="Accès non autorisé", status_code=status.HTTP_401_UNAUTHORIZED)
        
        cours_user = await Student.prisma().find_unique(where={"id":user_info["id"]}, include={"coursSuivis":True, "suiviCours":True})

        coursid = [el.id for el in cours_user.coursSuivis]

        if not (cours_id in coursid):
            raise HTTPException(detail="Accès non autorisé", status_code=stauts.HTTP_401_UNAUTHORIZED)

        suivi_id = [el.id for el in cours_user.suiviCours if el.coursId == cours_id][0]
        
        update = await Student.prisma().update(where={"id":user_info["id"]}, data={"coursSuivis":{"disconnect":{"id":cours_id}}})

        suivis = await SuiviCours.prisma().delete(where={"id":suivi_id})

        return suivi_id, update

    @staticmethod
    async def teacher(user_info):

        if (not user_info) or (user_info["role"] != Role.teacher):
            raise HTTPException(detail="Accès non autorisé", status_code=status.HTTP_401_UNAUTHORIZED)

        cours = await Teacher.prisma().find_unique(where={"id":user_info["id"]}, include={"coursCrees":True})

        return {"cours":cours.coursCrees}
    
    @staticmethod
    async def addcours(cours:AddCoursSchema, user_info):

        if not (user_info or user_info["role"] != Role.teacher):
            raise HTTPException(detail="Accès non autorisé", status_code=status.HTTP_401_UNAUTHORIZED)
        print("cours: ",cours)
        new_cours = await Cours.prisma().create(data={
            "auteurId":user_info["id"],
            "titre":cours.titre,
            "niveau":cours.niveau,
            "url_image":cours.url_image,
            "duree": cours.duree,
            "description":cours.description
            })
        
        for section in cours.sections:
            await Section.prisma().create(data={
                "coursId": new_cours.id,
                "titre":section.titre,
                "contenu":section.contenu
            })
        
        
        return {
                "response": "Cours crée avec succès",
                "id": new_cours.id
            }
    
    @staticmethod
    async def delete_cours(cours_id:int, user_info:dict):

        if (not user_info) or (user_info["role"] != Role.teacher):
            raise HTTPException(detail="Accès non autorisé", status_code=status.HTTP_401_UNAUTHORIZED)
        
        all_cours = await Teacher.prisma().find_first(where={"id":user_info["id"]}, include={"coursCrees":True})

        all_idcours = [el.id for el in all_cours.coursCrees if el.id == cours_id]

        if not all_idcours:
            raise HTTPException(detail="Accès non autorisé", status_code=status.HTTP_401_UNAUTHORIZED)

        suivis_delete = await SuiviCours.prisma().delete_many(where={"coursId":cours_id})
        
        sections_delete = await Section.prisma().delete_many(where={"coursId":cours_id})

        cours_delete = await Cours.prisma().delete(where={"id":cours_id})

        return suivis_delete, sections_delete, cours_delete

    @staticmethod
    async def update_cours(image, id:int):
        response = await save_local_image(image)
        await Cours.prisma().update(where={"id":id}, data={"image":response["file"]["url"]})
        return {"response":"success"}
