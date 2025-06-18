import datetime
import json
from typing import Annotated

from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm, OAuth2PasswordBearer
import bcrypt
import jwt
from prisma.models import Student, Teacher

from app.shemas.authentication import Role

from upyloadthing import UTApi, UTApiOptions

api = UTApi(UTApiOptions(token="eyJhcGlLZXkiOiJza19saXZlX2ZiMzZmMjllY2VlMmRmMzFkZWQ4MWQ2YjIxMmIxMzk2M2RmMzZiMThhMDc5Y2I5M2Q0OTNiZGIwN2I0OGUzMGQiLCJhcHBJZCI6InkxdjYwM3g1YTYiLCJyZWdpb25zIjpbInNlYTEiXX0="))




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
        raise HTTPException(detail="Accès non autorisé", status_code=status.HTTP_401_UNAUTHORIZED)

    user = json.loads(decoded.get("sub"))

    if not user:
        raise HTTPException(detail="Accès non autorisé", status_code=status.HTTP_401_UNAUTHORIZED)


    if user.get("role") == Role.teacher:
        current_user = await Teacher.prisma().find_unique(where={"id": user.get("id")})

    else:
        current_user = await Student.prisma().find_unique(where={"id": user.get("id")})

    return current_user




def permission_access(token:Annotated[str, Depends(get_token)]):

    try:
        decoded = verify_token(token)
    except:
        raise HTTPException(detail="Accès non autorisé", status_code=409)

    user = json.loads(decoded.get("sub"))

    if not user:
        raise HTTPException(detail="Accès non autorisé", status_code=status.HTTP_401_UNAUTHORIZED)

    return user


def register_image(image):
    with open(image, "rb") as f:
        result = api.upload_files(f)
    return result.url