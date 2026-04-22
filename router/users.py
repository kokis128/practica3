from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from typing import List

router = APIRouter()

class User(BaseModel):
    id: int
    nombre: str
    email: str



usuarios = [
    User(id=1, nombre="Juan Perez", email="juan.perez@example.com"),
    User(id=2, nombre="Ana Gomez", email="ana.gomez@example.com"),
]

@router.get("/users")
def obtener_usuarios():
    return usuarios

@router.get("/user/{user_id}")
def obtener_usuario(user_id: int):
    usuario =  list(filter (lambda user: user.id == user_id, usuarios))
    if usuario is None:
        raise HTTPException(status_code=404, detail="Usuario no encontrado")
    return usuario[0]

@router.post("/user", status_code=201)
async def agregar_usuario(user: User):
   
    
    usuarios.append(user)
    return {"mensaje": "usuario agregado"}


@router.put("/user/")
async def update_user(user: User):
    found = False

    for index, saved_user in enumerate(usuarios):
        if saved_user.id == user.id:
            usuarios[index] = user
            found = True
            return user  # devolver el actualizado

    if not found:
        return {"mensaje": "no se actualizó el usuario"}
    
    
@router.delete("/user/{id}")
async def delete_user(id: int): 
    for index, saved_user in enumerate(usuarios): 
        if saved_user.id == id:
            usuarios.remove(saved_user)
            return {"mensaje":"usuario eliminado"}       
    
    
def search_user(id: int):
    users = filter (lambda user: user.id == id, usuarios)
    try:
        return list(users)[0]
    except :
        return {"error": "User not found   "}