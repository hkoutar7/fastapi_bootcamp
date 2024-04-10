from sqlalchemy.orm import Session

from app.schema.UserSchema import UserSchema, UserCreateSchema, UserUpdateSchema
from app.service.AuthService import get_password_hash
from app.model.UserModel import UserModel

def retrieve_user_by_email(email : str, db : Session) -> bool :
    is_user_exist = db.query(UserModel).filter(UserModel.email == email).first()
    if not is_user_exist :
        return False
    return True


def save_user(user : UserCreateSchema, db : Session) -> None | UserModel :
    user_created = UserModel(
        email = user.email,
        password = get_password_hash(user.password)
    )

    db.add(user_created)
    db.commit()
    db.refresh(user_created)

    return user_created





