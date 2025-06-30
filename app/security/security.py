import datetime
import json
from pathlib import Path
from typing import Annotated
from app.shemas.authentication import RegisterSchema
from fastapi import Depends, HTTPException, status, Request
from fastapi.security import OAuth2PasswordRequestForm, OAuth2PasswordBearer
import bcrypt
import jwt
from prisma.models import Student, Teacher

from app.shemas.authentication import Role

from upyloadthing import UTApi, UTApiOptions

api = UTApi(UTApiOptions(token="eyJhcGlLZXkiOiJza19saXZlX2ZiMzZmMjllY2VlMmRmMzFkZWQ4MWQ2YjIxMmIxMzk2M2RmMzZiMThhMDc5Y2I5M2Q0OTNiZGIwN2I0OGUzMGQiLCJhcHBJZCI6InkxdjYwM3g1YTYiLCJyZWdpb25zIjpbInNlYTEiXX0="))

path = Path()

DIRECTORY_FILE = path.cwd() / "app/static"



def hashed_password(password:str) -> str:
    hashed = bcrypt.hashpw(password.encode(), bcrypt.gensalt())
    return hashed.decode()

def verify_password(password:str, hash_password:str) -> bool:
    is_valide = bcrypt.checkpw(password.encode(), hash_password.encode())
    return is_valide

def create_token(data:Student|Teacher, role) -> str:
    data = {
        "id":data.id,
        "role":role.value
    }

    payload = {
        "iat": datetime.datetime.now(),
        "sub":json.dumps(data),
        "exp":datetime.datetime.now()+datetime.timedelta(hours=5)
    }

    token = jwt.encode(payload,key="qmsldkfjmqsldjfqmslj",algorithm="HS256")
    return token


def verify_token(token:str):
    decoded = jwt.decode(token, key="qmsldkfjmqsldjfqmslj", algorithms="HS256")
    return decoded


get_token = OAuth2PasswordBearer(tokenUrl="auth/login")


async def get_current_user(token:Annotated[str, Depends(get_token)]):

    try:
        decoded = verify_token(token)
    except:
        raise HTTPException(detail="Accès non autorisé", status_code=status.HTTP_403_FORBIDDEN)

    user = json.loads(decoded.get("sub"))

    if not user:
        raise HTTPException(detail="Accès non autorisé", status_code=status.HTTP_404_NOT_FOUND)


    if user.get("role") == Role.teacher:
        current_user = await Teacher.prisma().find_unique(where={"id": user.get("id")})

    else:
        current_user = await Student.prisma().find_unique(where={"id": user.get("id")})
    
    user_current = {
        "mail": current_user.mail,
        "nom":current_user.nom,
        "prenom": current_user.prenom,
        "url_image": current_user.url_image,
        "biographie":current_user.biographie,
        "role":user["role"]
    }

    return user_current




def permission_access(token:Annotated[str, Depends(get_token)]):

    try:
        decoded = verify_token(token)
    except:
        raise HTTPException(detail="Accès non autorisé", status_code=status.HTTP_401_UNAUTHORIZED)

    user = json.loads(decoded.get("sub"))

    if not user:
        raise HTTPException(detail="Accès non autorisé", status_code=status.HTTP_404_NOT_FOUND)

    return user


def register_image(image):
    url = ""
    with open(image, "rb") as f:
        result = api.upload_files(f)
    for el in result:
        url = el.url
    return url


async def parse_register_schema(request: Request) -> RegisterSchema:
    form = await request.form()
    file: UploadFile = form.get("data")

    if not file:
        raise ValueError("Champ 'data' manquant.")

    # Lire une seule fois le contenu du fichier JSON
    raw = await file.read()

    try:
        return RegisterSchema.parse_raw(raw)
    except ValidationError as e:
        raise e

async def save_local_image(image):
    print(DIRECTORY_FILE)
    DIRECTORY_FILE.mkdir(exist_ok=True)
    contenu = await image.read()
    chemin = DIRECTORY_FILE / image.filename
    chemin.write_bytes(contenu)
    print("chemin: ",chemin)
    url = register_image(chemin)
    print("url:",url)
    response = {
    "success" : 1,
    "file": {
        "url" : url
    }
    }
    return response