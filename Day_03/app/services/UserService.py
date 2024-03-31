from fastapi import status, HTTPException
from sqlalchemy.orm import Session
from bcrypt import hashpw, gensalt
from app.models.UserModel import UserModel
from app.schemas.UserSchema import UserCreateSchema, UserSchema, UserUpdateSchema

def check_user(id : int, db : Session) -> bool :
    is_exist_user = db.query(UserModel).filter(UserModel.id == id).first()
    if not is_exist_user :
        return False
    return True


def hashed_password(password : str) -> str :
    bytes = password.encode('utf-8')
    salt = gensalt() 
    hash_password = hashpw(bytes, salt) 
    return hash_password


def check_email(email : str, db : Session ) -> bool :
    is_email_exist = db.query(UserModel).filter(UserModel.email == email).first()
    if not is_email_exist :
        return True
    else : 
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail= {
                "status_code" : status.HTTP_400_BAD_REQUEST,
                "detail" : "user's email already in use ",
                "data" : None
            }
        )


def store_user(user : UserCreateSchema, db : Session) -> UserModel : 
    check_email(user.email, db)
    
    user_created = UserModel(first_name = user.first_name, last_name = user.last_name, email= user.email, password=hashed_password(user.password))
    db.add(user_created)
    db.commit()
    db.refresh(user_created)
    
    return user_created


def retrieve_users(db : Session) -> list :
    users = db.query(UserModel).all()
    user_list = [UserSchema.from_orm(user) for user in users]
    return user_list


def retrieve_user(id : int, db : Session) -> UserModel | None :
    user = db.query(UserModel).filter(UserModel.id == id).first()
    return user


def modify_user(id : int, user : UserUpdateSchema, db : Session) -> bool | UserModel :
    is_user_exist = retrieve_user(id, db)

    if not is_user_exist :
        return False

    db.query(UserModel).filter(UserModel.id == id).update({
        UserModel.first_name: user.first_name,
        UserModel.last_name: user.last_name
    })
    db.commit()

    updated_user = retrieve_user(id, db)
    return updated_user


def destroy_user(id : int, db : Session) -> bool | UserModel :
    is_user_exist = retrieve_user(id, db)

    if not is_user_exist :
        return False
    
    user_deleted = is_user_exist
    db.query(UserModel).filter(UserModel.id == id).delete(synchronize_session=False)

    return user_deleted

