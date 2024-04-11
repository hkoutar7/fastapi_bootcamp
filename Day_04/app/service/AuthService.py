from fastapi import status, HTTPException
from sqlalchemy.orm import Session
from datetime import datetime, timedelta, timezone
from os import getenv
from jose import jwt, JWTError

from app.model.UserModel import UserModel
from app.schema.AuthSchema import Token, TokenData
from app.service.UtilsService import verify_password


SECRET_KEY = getenv("SECRET_KEY")
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 1



def get_user_by_email(email : str, db : Session) -> None | UserModel :
    is_user = db.query(UserModel).filter(UserModel.email == email).first()
    if not is_user :
        return None 
    return is_user


def get_user_by_id(id : int, db : Session) -> None | UserModel :
    is_user = db.query(UserModel).filter(UserModel.id == id).first()
    if not is_user :
        return None 
    return is_user


def authentificate_user(email : str, password : str, db : Session) -> None | UserModel :
    is_user = get_user_by_email(email, db)
    if not is_user :
        return None

    is_user_exist = verify_password(password, is_user.password)
    if not is_user_exist :
        return None
    
    return is_user


def create_acess_token(data : dict) -> str :
    to_encode = data.copy()
    expire_datetime = datetime.now(timezone.utc) + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"expire_datetime" : expire_datetime.isoformat()})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, ALGORITHM)

    return encoded_jwt


def retrieve_current_user(token : str, db : Session) -> UserModel | None :
    try : 
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])

        user_id = payload.get("id")
        if not user_id :
            return None
        
        expire_datetime = datetime.fromisoformat(payload.get("expire_datetime"))
        if expire_datetime < datetime.now(timezone.utc):
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail={
                    "message" : f"The token has been expired {expire_datetime}",
                    "status_code" : status.HTTP_400_BAD_REQUEST
                }
            )

        token_data = TokenData(id = user_id)
        if not token_data :
            return None
        
        user = get_user_by_id(user_id, db)
        if not user :
            return None
        
        return user
    
    except JWTError:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail={
                "message" : "The token verificationfailed ",
                "status_code" : status.HTTP_400_BAD_REQUEST
            }
        )


def check_user_actif(user : UserModel  , db : Session ) -> UserModel | None :
    is_user_actif = user.__dict__["is_active"]

    if is_user_actif == False :
        return None

    return user

