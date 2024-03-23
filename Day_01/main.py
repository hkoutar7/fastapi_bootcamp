from fastapi import FastAPI , Body

from schema import BasePost, Post
from service import retrieve_posts, retrieve_post_by_id , add_post, update_post_by_id, delete_post_by_id

app = FastAPI()


@app.get("/api/v1/posts")
def get_posts() -> dict:

    posts = retrieve_posts()
    
    return {
        "detail" : "posts retrieved successfully",
        "status_code" : 200,
        "data" : posts
    }


@app.get("/api/v1/posts/{id}")
def get_post(id : int) -> dict : 

    is_post = retrieve_post_by_id(id)

    if is_post is None :
        return {
            "detail" : "post doesnt exists",
            "status_code" : 400,
            "data" : None
        }
    return  {
        "detail" : "post retrieved successfully",
        "status_code" : 200,
        "data" : is_post
    }


@app.post("/api/v1/posts")
def save_post(payload : BasePost) -> dict :

    payload = payload.__dict__
    post = add_post(payload)

    return  {
        "detail" : "post retrieved successfully",
        "status_code" : 201,
        "data" : post
    }

@app.put("/api/v1/posts/{id}")
def update_post(id : int, payload : BasePost) -> dict :

    payload = payload.__dict__
    is_exist = update_post_by_id(id, payload)

    if is_exist is None :
        return {
            "detail" : "post doesnt exists",
            "status_code" : 400,
            "data" : None
        }

    return  {
        "detail" : "post updated successfully",
        "status_code" : 201,
        "data" : is_exist
    } 


@app.delete("/api/v1/posts/{id}")
def delete_post(id : int) -> dict :

    is_exist = delete_post_by_id(id)

    if is_exist is None :
        return {
            "detail" : "post doesnt exists",
            "status_code" : 400,
            "data" : None
        }

    return  {
        "detail" : "post deleted successfully",
        "status_code" : 200,
        "data" : is_exist
    } 

