import email

from db.models import user
from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from typing import List

from db.models.user import User
from db.schemas.user import user_schema, users_schema

from db.client import db_client

from bson import ObjectId



router = APIRouter()




usuarios = [
    
]

@router.get("/usersdb", response_model=list[User])
def obtener_usuarios():
    return users_schema(db_client.local.users.find())

# obtener un usuario por id, el id es un string que representa el ObjectId de mongo, hay que convertirlo a ObjectId para buscarlo en la base de datos
@router.get("/userdb/{user_id}")
def obtener_usuario(user_id: str):
   
        return search_user("_id", ObjectId(user_id))

@router.post("/userdb", status_code=201)
async def agregar_usuario(user: User):
    if type(search_user("_id",user.id))==User:
        raise HTTPException(status_code=400, detail="Usuario con ese id ya existe")
   
    # user hay que transformarlo a json para que mongo lo pueda guardar
    user_dict=dict(user)
    del user_dict["id"] # eliminamos el id porque mongo lo genera automaticamente
    id=db_client.local.users.insert_one(user_dict).inserted_id # insertamos el usuario en la base de datos y obtenemos el id generado por mongo    
    new_user = user_schema(db_client.local.users.find_one({"_id": id}))
    if new_user is None:
        return {"error": "Usuario no encontrado después de insertar"}
     
   
    
    return User(**new_user) # devolvemos el usuario con su id generado por mongo


@router.put("/userdb", response_model=User)
async def update_user(user: User):
    
    user_dict=dict(user)
    del user_dict["id"] # eliminamos el id porque mongo lo genera automaticamente
    try:
        
        db_client.local.users.find_one_and_replace({"_id": ObjectId(user.id)}, user_dict)
        
        
        
    except:
           
        return {"mensaje": "no se actualizó el usuario"}
    return search_user("_id", ObjectId(user.id))
    
@router.delete("/userdb/{id}",status_code=204)
async def delete_user(id: str):
    found=db_client.local.users.find_one_and_delete({"_id": ObjectId(id)})
        
    if not found:
        return {"mensaje": "no se eliminó el usuario"}
    
def search_user_by_email(email: str):
    
    try:
        user=db_client.local.users.find_one({"email": email})
        print(email)
        return  User(**user_schema(user))
    except :
        return {"error": "User not found   "}
    
    
def search_user(field: str, key):
   
    try:
        user=db_client.local.users.find_one({field: key})
        
        return User(**user_schema(user))
    except :
        return {"error": "User not found   "}