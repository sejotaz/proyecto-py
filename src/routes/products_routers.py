from src.models.ProductsModel import Product, ProductUpdate
from src.schemas.product import product_schema, products_schema
from database import db
from bson import ObjectId
from typing import Dict, Optional
from src.entities.productEntity import ProductResponse
from fastapi import APIRouter, HTTPException, status

router = APIRouter(prefix="/products", tags=["Product"], responses={404: {"message": "Not found"}})

@router.get("/query", response_model=list[Product])
async def products():
  return products_schema(db.products.find({"isRemove": False}))

@router.get("/query/{id}", response_model=Product)
async def product(id: str):
  return product_schema(db.products.find_one({"_id": ObjectId(id)}))


#Crear un usuario
@router.post("/create", response_model=Product, status_code=status.HTTP_201_CREATED)
async def create_product(product: Product):
   if type(search_product("name_product", product.name_product)) == Product:
       raise HTTPException(
           status_code=status.HTTP_404_NOT_FOUND, detail="El producto ya existe")
   try: 
      product_dict = product.model_dump()
      del product_dict["id"]

      id = db.products.insert_one(product_dict).inserted_id

      new_product = product_schema(db.products.find_one({"_id": id}))

      return Product(**new_product)
   
   except Exception as e:
       print("Error al crear el producto:", e)
       raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="Error al crear el producto")
   
@router.patch("/update/{id}", response_model=ProductResponse)
async def update_product(id: str, product: ProductUpdate):
   
   update_data: Dict[str, Optional[str]] = product.model_dump(exclude_unset=True)
   if not ObjectId.is_valid(id):
       raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Invalid product ID")
   try:
       update_product = db.products.find_one_and_update({"_id": ObjectId(id)},
           {"$set": update_data},
           return_document=True)

       if update_product is None:
           raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Product not found")

   except Exception as e:
       print("Error al actualizar el producto:", e)
       raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="Error al actualizar el producto")
    
   return ProductResponse(
        id=str(update_product["_id"]),
        name=update_product.get("name"),
        description=update_product.get("description"),
        price=update_product.get("price"),
        stock=update_product.get("stock"),
        isRemove=update_product.get("isRemove")
    )

@router.patch("/delete/{id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_product(id: str):
    try:
        db.products.find_one_and_update({"_id": ObjectId(id)}, {"$set": {"isRemove": True}})
        return {"message": "Producto eliminado"}
    except Exception as e:
        print("Error al eliminar el producto:", e)
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="Error al eliminar el producto")


#Funciones para validar
def search_product(field: str, key):
    try:
        product = db.products.find_one({field: key})
        print(f"Resultado de búsqueda para {field} = {key}: {product}")
        if product:
            return Product(**product_schema(product))
        return None
    except Exception as e:
        print(f"Error al buscar el producto: {e}")
        return None