from fastapi import HTTPException, status
from prisma.models import Student, Teacher

from app.security.security import hashed_password, verify_password, create_token, register_image
from app.shemas.authentication import RegisterSchema, LoginSchema, Role


class AuthService:

    @staticmethod
    async def register(user_info:RegisterSchema):

        """
        Cette fonction permet d'enrégistrer un nouvel utilisateur
        dans la base de données

        :param user_info: schema pydantic
        :return: user
        """


        if user_info.role == Role.teacher:

            # On vérifie si l'utilisateur n'existe pas déjà en se basant sur le mail
            user_existe = await Teacher.prisma().find_unique(where={"mail":user_info.mail})
            if user_existe:
                raise HTTPException(detail="L'utilisateur existe déjà", status_code=status.HTTP_409_CONFLICT)

            # Vérifie si les password sont identiques
            if user_info.password != user_info.conf_password:
                raise HTTPException(detail="Mot de pass différent", status_code=status.HTTP_400_BAD_REQUEST)
            hashed = hashed_password(user_info.password)
            # Ajout de l'utilisateur dans la base de données
            user = await Teacher.prisma().create(
                data={
                    "nom": user_info.nom,
                    "prenom": user_info.prenom,
                    "biographie": user_info.biographie,
                    "mail": user_info.mail,
                    "password": hashed
                }
            )

        else:
            # On vérifie si l'utilisateur n'existe pas déjà en se basant sur le mail
            user_existe = await Student.prisma().find_unique(where={"mail": user_info.mail})
            if user_existe:
                raise HTTPException(detail="L'utilisateur existe déjà", status_code=status.HTTP_409_CONFLICT)

            # Vérifie si les password sont identiques
            if user_info.password != user_info.conf_password:
                raise HTTPException(detail="Mot de pass différent", status_code=status.HTTP_401_UNAUTHORIZED)

            #hasher le password de l'utilisateur avant de l'enregistrer
            hashed = hashed_password(user_info.password)

            # Ajout de l'utilisateur dans la base de données
            user = await Student.prisma().create(
                data={
                    "nom": user_info.nom,
                    "prenom": user_info.prenom,
                    "biographie": user_info.biographie,
                    "mail": user_info.mail,
                    "password": hashed
                }
            )

            if user_info.image:
                await Cours.prisma().update(where={"id":user.id},
                data={
                    "url_image":register_image(user_info.image)
                    })

        return  {"response": "Utilisateur enrégistré avec succès"}

    @staticmethod
    async def login(user:LoginSchema):

        if user.role == Role.teacher:

            # On vérifie si l'utilisateur existe
            exist_user = await Teacher.prisma().find_unique(where={"mail":user.mail})
            if not exist_user:
                raise HTTPException(detail="Identifiant incorrect", status_code=status.HTTP_401_UNAUTHORIZED)

            #On vérifie le hash du mot de pass
            is_valid = verify_password(user.password, exist_user.password)
            if not is_valid:
                raise HTTPException(detail="Identifiant incorrect", status_code=status.HTTP_401_UNAUTHORIZED)

            #On crée un token pour l'utilisateur
            token = create_token(exist_user, user.role)
        else:
            # On vérifie si l'utilisateur existe
            exist_user = await Student.prisma().find_unique(where={"mail": user.mail})
            if not exist_user:
                raise HTTPException(detail="Identifiant incorrect", status_code=status.HTTP_401_UNAUTHORIZED)

            # On vérifie le hash du mot de pass
            is_valid = verify_password(user.password, exist_user.password)
            if not is_valid:
                raise HTTPException(detail="Identifiant incorrect", status_code=status.HTTP_401_UNAUTHORIZED)

            # On crée un token pour l'utilisateur
            token = create_token(exist_user, user.role)

        return {"token": token}

    @staticmethod
    async def current_user(user:Student|Teacher):
        return user
