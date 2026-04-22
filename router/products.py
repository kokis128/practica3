from fastapi import APIRouter
router = APIRouter()

@router.get("/products")
async def products():
        return  ["Producto 1", "Producto 2", "Producto 3"]