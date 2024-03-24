from fastapi import FastAPI , Body , status , HTTPException

from app.schema import BasePost, Post
from app.service import retrieve_posts, retrieve_post_by_id , add_post, update_post_by_id, delete_post_by_id, retrieve_latest_post

app = FastAPI()


@app.get("/api/v1/posts")
def get_posts() -> dict:

    posts = retrieve_posts()
    
    return {
        "detail" : "posts retrieved successfully",
        "status_code" : status.HTTP_200_OK,
        "data" : posts
    }


@app.get("/api/v1/posts/latest") 
def get_latest_post() -> dict :
    post = retrieve_latest_post()

    if post is None :
        raise HTTPException(
            status_code= status.HTTP_404_NOT_FOUND,
            detail= {
                "detail" : "post doesnt exists",
                "status_code" : status.HTTP_404_NOT_FOUND,
                "data" : None
            })
    return  {
        "detail" : "post retrieved successfully",
        "status_code" : status.HTTP_200_OK,
        "data" : post
    }


@app.get("/api/v1/posts/{id}")
def get_post(id : int) -> dict : 

    is_post = retrieve_post_by_id(id)

    if is_post is None :
        raise HTTPException(
            status_code= status.HTTP_404_NOT_FOUND,
            detail= {
                "detail" : "post doesnt exists",
                "status_code" : status.HTTP_404_NOT_FOUND,
                "data" : None
            })
    return  {
        "detail" : "post retrieved successfully",
        "status_code" : status.HTTP_200_OK,
        "data" : is_post
    }


@app.post("/api/v1/posts", status_code= status.HTTP_201_CREATED)
def save_post(payload : BasePost) -> dict :

    payload = payload.__dict__
    post = add_post(payload)

    return  {
        "detail" : "post retrieved successfully",
        "status_code" : status.HTTP_201_CREATED,
        "data" : post
    }


@app.put("/api/v1/posts/{id}" , status_code= status.HTTP_201_CREATED)
def update_post(id : int, payload : BasePost) -> dict :

    payload = payload.__dict__
    is_exist = update_post_by_id(id, payload)

    if is_exist is None :
        raise HTTPException(
            status_code= status.HTTP_404_NOT_FOUND,
            detail= {
                "detail" : "post doesnt exists",
                "status_code" : status.HTTP_404_NOT_FOUND,
                "data" : None
            })

    return  {
        "detail" : "post updated successfully",
        "status_code" : status.HTTP_201_CREATED,
        "data" : is_exist
    } 


@app.delete("/api/v1/posts/{id}" , status_code= status.HTTP_200_OK)
def delete_post(id : int) -> dict :

    is_exist = delete_post_by_id(id)

    if is_exist is None :
        raise HTTPException(
            status_code= status.HTTP_404_NOT_FOUND,
            detail= {
                "detail" : "post doesnt exists",
                "status_code" : status.HTTP_404_NOT_FOUND,
                "data" : None
            })

    return  {
        "detail" : "post deleted successfully",
        "status_code" : status.HTTP_200_OK,
        "data" : is_exist
    } 

