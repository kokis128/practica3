from fastapi import FastAPI, Depends, HTTPException, status
from pydantic import BaseModel
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from fastapi import APIRouter


router = APIRouter()


oauth2 = OAuth2PasswordBearer(tokenUrl="login")


class User(BaseModel):
    username: str
    full_name: str
    email: str
    disabled: bool


class UserDb(User):
    password: str


users_db = {
    "johndoe": {
        "username": "johndoe",
        "full_name": "John Doe",
        "email": "john.doe@example.com",
        "disabled": False,
        "password": "123456"
    },
    "alice": {
        "username": "alice",
        "full_name": "Alice Smith",
        "email": "alice.smith@example.com",
        "disabled": False,
        "password": "abcdef"
    }
}


def search_user(username: str):
    if username in users_db:
        return UserDb(**users_db[username])
    return None


async def current_user(token: str = Depends(oauth2)):
    user = search_user(token)

    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Credenciales inválidas",
            headers={"WWW-Authenticate": "Bearer"}
        )

    if user.disabled:
        raise HTTPException(status_code=400, detail="Usuario inactivo")

    return user


@router.post("/login")
async def login(form: OAuth2PasswordRequestForm = Depends()):
    user = search_user(form.username)

    if not user:
        raise HTTPException(status_code=400, detail="Usuario no encontrado")

    if form.password != user.password:
        raise HTTPException(status_code=400, detail="Contraseña incorrecta")

    return {"access_token": form.username, "token_type": "bearer"}


@router.get("/users/me")
async def me(user: User = Depends(current_user)):
    return user


class LoginData(BaseModel):
    username: str
    password: str
    
    
users2_db = {
    "johndoe": "123456",
    "alice": "abcdef"
}

@router.post("/login2")
def login(data: LoginData):
    if data.username not in users2_db:
        raise HTTPException(status_code=400, detail="Usuario no existe")

    if users2_db[data.username] != data.password:
        raise HTTPException(status_code=400, detail="Contraseña incorrecta")

    return {"message": "Login correcto"}

@router.post("/users2/me")
def me(data: LoginData):
    if data.username not in users_db or users_db[data.username] != data.password:
        raise HTTPException(status_code=401, detail="No autorizado")

    return {"username": data.username}