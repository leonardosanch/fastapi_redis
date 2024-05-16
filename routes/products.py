from fastapi import APIRouter
from redis_client.crud import delete, get_hash, save_hash
from schemas.product import Product
from fastapi import HTTPException

routes_product = APIRouter()

fake_db = [
   {
    "id": "a0153beb-4fa7-4304-8d85-023d6f3a71e2",
    "name": "Zapato",
    "price": 20,
    "date": "2024-05-15 11:42:31.035778"
    }
]

@routes_product.post("/create", response_model=Product)
def create(product:Product):
    try:
       
        fake_db.append(product.dict())
        
        #OPERATION CACHE
        
        save_hash(key=product.dict()["id"], data=product.dict())
        
        return product
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    
    

@routes_product.get("/get/{id}")
def get(id:str):
    try:
        # OPERATION CACHE
        
        data = get_hash(key=id)
        if len(data) ==0:
           
            #OPERATION DB
            product = list(filter(lambda field: field["id"]==id, fake_db))[0]
               
            # OPERACION CACHE 
        
            save_hash(key=id, data=product)
        
            return product
    
        return data
    
    except Exception as e:
        return e
    

@routes_product.delete("/delete/{id}")
def get(id:str):
    try:
        keys = Product.__fields__.keys()
        #OPERATION CACHE
        delete(key=id, keys=keys)
        product= list(filter(lambda field: field["id"]!=id, fake_db))
        if len(product) !=0:
            fake_db.remove(product)
        
        return {
            "message": "success"
        }
    
    except Exception as e:
        return e