from fastapi import FastAPI, HTTPException



from pydantic import BaseModel
from db.client import db_client

from router import products,users,basic_auth_users, users_db
from fastapi.staticfiles import StaticFiles

app = FastAPI()

#Routers
app.include_router(products.router)
app.include_router(users.router)
app.mount("/static", StaticFiles(directory="static"), name="static")
app.include_router(basic_auth_users.router)
app.include_router(users_db.router)


class User(BaseModel):
    id: int
    nombre: str
    email: str



usuarios = [
    User(id=1, nombre="Juan Perez", email="juan.perez@example.com"),
    User(id=2, nombre="Ana Gomez", email="ana.gomez@example.com"),
]

@app.get("/users")
def obtener_usuarios():
    return usuarios

@app.get("/user/{user_id}")
def obtener_usuario(user_id: int):
    usuario =  list(filter (lambda user: user.id == user_id, usuarios))
    if usuario is None:
        raise HTTPException(status_code=404, detail="Usuario no encontrado")
    return usuario[0]

@app.post("/user", status_code=201)
async def agregar_usuario(user: User):
   
    
    usuarios.append(user)
    return {"mensaje": "usuario agregado"}


@app.put("/user/")
async def update_user(user: User):
    found = False

    for index, saved_user in enumerate(usuarios):
        if saved_user.id == user.id:
            usuarios[index] = user
            found = True
            return user  # devolver el actualizado

    if not found:
        return {"mensaje": "no se actualizó el usuario"}
    
    
@app.delete("/user/{id}")
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
    
    