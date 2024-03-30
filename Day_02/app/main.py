from fastapi import FastAPI , Body , status , HTTPException

from app.service import retrieve_products , retrieve_product, add_product, update_product_by_id, delete_product_by_id
from app.schema import CreateProductSchema , ProductSchema , UpdateProductSchema


app = FastAPI()


@app.get("/api/v1/products") 
def get_all_products() -> dict :
    products = retrieve_products()

    return {
        "data" : products,
        "status_code" : status.HTTP_200_OK,
        "message" : "products fetched successfully"
    }


@app.get("/api/v1/products/{id}")
def get_product(id : int) -> dict :
    product = retrieve_product(id)

    if product == None :
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail= {
            "data" : product,
            "status_code" : status.HTTP_404_NOT_FOUND,
            "message" : "product is Unfound"
        })

    return {
        "data" : product,
        "status_code" : status.HTTP_200_OK,
        "message" : "product fetched successfully"
    }


@app.post("/api/v1/products", status_code= status.HTTP_201_CREATED)
def save_product(payload : CreateProductSchema) -> dict :
    try : 
        product = add_product(payload)
        
        return {
            "data" : product,
            "status_code" : status.HTTP_201_CREATED,
            "message" : "product created successfully"
        }

    except Exception as e:
        print("Error occur when adding product")


@app.put("/api/v1/products/{id}", status_code= status.HTTP_201_CREATED)
def update_product(id : int , payload : UpdateProductSchema) -> dict :
    product = update_product_by_id(id, payload)
    
    if product == None :
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail= {
            "data" : None,
            "status_code" : status.HTTP_404_NOT_FOUND,
            "message" : "product is Unfound"
        })
    
    return {
        "data" : product,
        "status_code" : status.HTTP_201_CREATED,
        "message" : "product updated successfully"
    }


@app.delete("/api/v1/products/{id}")
def delete_product(id: int) -> dict :
    product = delete_product_by_id(id)

    if product == None :
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail= {
            "data" : None,
            "status_code" : status.HTTP_404_NOT_FOUND,
            "message" : "product is Unfound"
        })
    
    return {
        "data" : product,
        "status_code" : status.HTTP_200_OK,
        "message" : "product deleted successfully"
    }