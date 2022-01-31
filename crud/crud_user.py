from typing import Any, Dict, Optional, Union


from core.security import get_password_hash, verify_password
from crud.base import CRUDBase
from models.user import User

from schemas.users import UserCreate, UserUpdate



from fastapi_sqlalchemy import DBSessionMiddleware, db

class CRUDUser(CRUDBase[User, UserCreate, UserUpdate]):
    def get_by_email(self,  email: str):
        return db.session.query(User).filter(User.email == email).first()

    def create(self,  obj_in: UserCreate) -> User:
        db_obj = User(
            email=obj_in.email,
            password=get_password_hash(obj_in.password),
            surname=obj_in.surname,
            username=obj_in.username,
            name=obj_in.name
        )
        db.session.add(db_obj)
        db.session.commit()
        db.session.refresh(db_obj)
        return db_obj

    def update(
        self, *, db_obj: User, obj_in: Union[UserUpdate, Dict[str, Any]]
    ) -> User:
        if isinstance(obj_in, dict):
            update_data = obj_in
        else:
            update_data = obj_in.dict(exclude_unset=True)
        if update_data["password"]:
            hashed_password = get_password_hash(update_data["password"])
            del update_data["password"]
            update_data["hashed_password"] = hashed_password
        return super().update(db, db_obj=db_obj, obj_in=update_data)

    def delete(self,  email: str) -> Optional[User]:
        user = self.get_by_email( email=email)
        db.session.delete(user)
        db.session.commit()
        if not user:
            return None
        return user

    def authenticate(self,  email: str, password: str) -> Optional[User]:
        user = self.get_by_email( email=email)
        if not user:
            return None
        if not verify_password(password, user.password):
            return None
        return user

    def is_active(self, user: User) -> bool:
        return user.isActive

    def is_superuser(self, user: User) -> bool:
        return user.is_superuser


user = CRUDUser(User)
