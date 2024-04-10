from fastapi import APIRouter, HTTPException, Depends, status
from sqlalchemy.orm import Session
from app.schema.UserSchema import UserCreateSchema, UserUpdateSchema, UserSchema
from app.service.UserService import retrieve_user_by_email ,save_user
from database.database import get_db


router = APIRouter(
    prefix="/api/v1/users",
    tags=["users"]
)


@router.post("", status_code=status.HTTP_201_CREATED, summary="register a user", description="register a new user withing the database")
async def register_user(user : UserCreateSchema, db : Session = Depends(get_db)) :
    try :
        is_user_exist = retrieve_user_by_email(user.email, db)
        if is_user_exist == True :
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail={
                    "message" : "user doesn't dreated successfully email already exist",
                    "status_code" : status.HTTP_400_BAD_REQUEST,
                }
            )

        user_created = save_user(user, db)
        if not user_created :
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail={
                    "message" : "user doesn't created successfully",
                    "status_code" : status.HTTP_400_BAD_REQUEST,
                }
            )
        
        return {
            "message" : "user created successfully",
            "status_code" : status.HTTP_201_CREATED,
            "data" : UserSchema.from_orm(user_created)
        }

    except Exception as e :
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail={
                "message" : "user doesn't created successfully",
                "status_code" : status.HTTP_400_BAD_REQUEST,
                "error" : str(e)
            }
        )

