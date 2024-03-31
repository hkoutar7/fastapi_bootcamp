from fastapi import FastAPI, status, Depends, HTTPException
from sqlalchemy.orm import Session
from app.models import ItemModel, UserModel
from app.database.Database import engine, Base, get_db
from app.schemas.UserSchema import UserCreateSchema, UserSchema, UserUpdateSchema
from app.schemas.Itemschema import ItemCreateSchema, ItemSchema
from app.services.UserService import retrieve_users, retrieve_user, store_user, modify_user, destroy_user

Base.metadata.create_all(bind=engine)

app = FastAPI()


@app.get("/api/v1/users", status_code=status.HTTP_200_OK)
def get_all_users(db : Session = Depends(get_db)) -> dict :
    users = retrieve_users(db)

    return {
        "status_code" : status.HTTP_200_OK,
        "detail" : "users retrieved successfully",
        "data" : users,
    }


@app.get("/api/v1/users/{id}")
def get_user(id : int, db : Session = Depends(get_db)) -> dict :
    is_user = retrieve_user(id, db)

    if  not is_user :
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail= {
            "status_code" : status.HTTP_404_NOT_FOUND,
            "detail" : "user unfound ",
            "data" : None,
        })
    return {
        "status_code" : status.HTTP_200_OK,
        "detail" : "user retrieved successfully",
        "data" : UserSchema.from_orm(is_user),
    }


@app.post("/api/v1/users", status_code=status.HTTP_201_CREATED)
def create_user(user : UserCreateSchema, db : Session = Depends(get_db)) -> dict : 
    is_user_created = store_user(user, db)

    if not is_user_created :
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail= {
                "status_code" : status.HTTP_400_BAD_REQUEST,
                "detail" : "user didn't created",
                "data" : None
            }
        )
    
    return {
        "status_code" : status.HTTP_201_CREATED,
        "detail" : "user created successfully",
        "data" : UserSchema.from_orm(is_user_created),
    }


@app.put("/api/v1/users/{id}", status_code=status.HTTP_201_CREATED)
def update_post(id : int, user : UserUpdateSchema, db : Session = Depends(get_db)) -> dict :
    user = modify_user(id, user, db)

    if  not user :
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail= {
            "status_code" : status.HTTP_404_NOT_FOUND,
            "detail" : "user unfound ",
            "data" : None,
        })
    return {
        "status_code" : status.HTTP_201_CREATED,
        "detail" : "user updated successfully",
        "data" : UserSchema.from_orm(user),
    }


@app.delete("/api/v1/users/{id}", status_code= status.HTTP_200_OK)
def delete_post(id : int, db : Session = Depends(get_db)) -> dict :
    user = destroy_user(id, db)

    if  not user :
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail= {
            "status_code" : status.HTTP_404_NOT_FOUND,
            "detail" : "user unfound ",
            "data" : None,
        })
    return {
        "status_code" : status.HTTP_201_CREATED,
        "detail" : "user deleted successfully",
        "data" : UserSchema.from_orm(user),
    }

