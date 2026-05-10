from fastapi import APIRouter
router = APIRouter(prefix="/products", 
    responses = {404: {"message": "No encontrado"}})

products_list =["Producto1", "Producto2", "Producto3"]


@router.get("/")
async def products():
        return  products_list
    
    
@router.get("/products/{id}")
async def products(id:int):
        return  products_list[id]