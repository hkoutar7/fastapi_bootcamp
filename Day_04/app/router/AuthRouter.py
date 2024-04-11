from fastapi import APIRouter, HTTPException, Depends, status
from fastapi.security import OAuth2PasswordRequestForm, OAuth2PasswordBearer
from sqlalchemy.orm import Session

from app.service.AuthService import authentificate_user, create_acess_token, retrieve_current_user, check_user_actif
from app.schema.UserSchema import UserSchema, UserCreateSchema, UserUpdateSchema
from app.schema.AuthSchema import Token, TokenData
from database.database import get_db


router = APIRouter(
    prefix="/api/v1/auth",
    tags=["auth"]
)

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/api/v1/auth/login")


@router.post("/login", status_code=status.HTTP_200_OK, summary="login in user", description="This endpoint allow a user to login in")
async def login(form_data : OAuth2PasswordRequestForm = Depends(), db : Session = Depends(get_db)) -> dict :
    try :
        is_user = authentificate_user(form_data.username, form_data.password, db)
        if not is_user :
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail={
                    "message" : "user doesn't login in successfully, Invalid credentials",
                    "status_code" : status.HTTP_403_FORBIDDEN,
                    "error" : str(e)
                }
            )
        
        access_token = create_acess_token (data = {"id" : is_user.id})
        token = Token(access_token=access_token, token_type="bearer")

        return {
            "message" : "user login successfully",
            "status_code" : status.HTTP_200_OK,
            "data" : token
        }
    
    except Exception as e :
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            headers={"WWW-Authenticate": "Bearer"},
            detail={
                "message" : "user doesn't login in successfully, Invalid credentials",
                "status_code" : status.HTTP_401_UNAUTHORIZED,
                "error" : str(e)
            }
        )


@router.get("/me", status_code=status.HTTP_200_OK, summary="get current user", description="This endpoint allow a user to get its informations")
async def get_current_user(token : str = Depends(oauth2_scheme), db : Session = Depends(get_db)) :
    try : 
        is_user = retrieve_current_user(token, db)

        if not is_user :
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                headers={"WWW-Authenticate": "Bearer"},
                detail={
                    "message" : "user doesn't login in successfully, Invalid credentials",
                    "status_code" : status.HTTP_401_UNAUTHORIZED,
                }
            )
        
        is_user_actif = check_user_actif(is_user, db)
        if not is_user_actif :
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail={
                    "message" : "user isn't actif",
                    "status_code" : status.HTTP_400_BAD_REQUEST,
                }
            )
        
        return {
            "message" : "user informations retieved successfully",
            "status_code" : status.HTTP_200_OK,
            "data" : UserSchema.from_orm(is_user_actif)
        }

    except Exception as e :
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            headers={"WWW-Authenticate": "Bearer"},
            detail={
                "message" : "user doesn't login in successfully, Invalid credentials",
                "status_code" : status.HTTP_401_UNAUTHORIZED,
                "error" : str(e)
            }
        )


