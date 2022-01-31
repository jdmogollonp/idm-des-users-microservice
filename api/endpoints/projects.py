from typing import Any, List

from fastapi import APIRouter, Body, Depends, HTTPException
from fastapi.encoders import jsonable_encoder
from pydantic.networks import EmailStr
from sqlalchemy.orm import Session

#from app import crud, models, schemas
#from app.api import deps
#from core.config import settings
#from app.utils import send_new_account_email

import os
import uvicorn
from dotenv import load_dotenv
from fastapi import FastAPI
from fastapi_sqlalchemy import DBSessionMiddleware, db
from fastapi.security import OAuth2PasswordBearer
from models.user import User as Modeluser
from schemas.users import Users as SchemaUsers



from schemas.users import UserCreate as SchemaUserCreate

from schemas.users import UserCreate as SchemaUserCreate

router = APIRouter()


oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

@router.post("/create_project/", response_model=SchemaUsers)
def create_project(user: SchemaUsers,  token: str = Depends(oauth2_scheme)):
    db_user = Modeluser(name=user.name, surname=user.surname, email=user.email, password=user.password)
    db.session.add(db_user)
    db.session.commit()
    return db_user

@router.put("/update_project/", response_model=SchemaUsers)
def update_project(user: SchemaUsers,  token: str = Depends(oauth2_scheme)):
    db_user = Modeluser( email=user.email, password=user.password)
    db.session.add(db_user)
    db.session.commit()
    return db_user, token

@router.post("/delete_project/", response_model=SchemaUsers)
def delete_project(user: SchemaUsers,  token: str = Depends(oauth2_scheme)):
    db_user = Modeluser( email=user.email, password=user.password)
    db.session.add(db_user)
    db.session.commit()
    return db_user, token

@router.get("/view_project/", response_model=SchemaUsers)
def view_project(user: SchemaUsers,  token: str = Depends(oauth2_scheme)):
    db_user = Modeluser( email=user.email, password=user.password)
    db.session.add(db_user)
    db.session.commit()
    return db_user, token


@router.get("/invite_user/", response_model=SchemaUsers)
def invite_user(user: SchemaUsers,  token: str = Depends(oauth2_scheme)):
    db_user = Modeluser(name=user.name, surname=user.surname, email=user.email, password=user.password)
    db.session.add(db_user)
    db.session.commit()
    return db_user


@router.get("/search_project/", response_model=SchemaUsers)
def search_project(user: SchemaUsers,  token: str = Depends(oauth2_scheme)):
    db_user = Modeluser( email=user.email, password=user.password)
    db.session.add(db_user)
    db.session.commit()
    return db_user, token



