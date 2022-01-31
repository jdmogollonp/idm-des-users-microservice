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

router = APIRouter()


oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

@router.post("/upload_resource/", response_model=SchemaUsers)
def upload_resource(user: SchemaUsers):
    db_user = Modeluser(name=user.name, surname=user.surname, email=user.email, password=user.password)
    db.session.add(db_user)
    db.session.commit()
    return db_user


@router.get("/download_resource/", response_model=SchemaUsers)
def download_resource(user: SchemaUsers,token: str = Depends(oauth2_scheme)):
    db_user = Modeluser(name=user.name, surname=user.surname, email=user.email, password=user.password)
    db.session.add(db_user)
    db.session.commit()
    return db_user

@router.post("/delete_resource/", response_model=SchemaUsers)
def delete_resource(user: SchemaUsers,token: str = Depends(oauth2_scheme)):
    db_user = Modeluser(name=user.name, surname=user.surname, email=user.email, password=user.password)
    db.session.add(db_user)
    db.session.commit()
    return db_user


@router.get("/check_data_quality/", response_model=SchemaUsers)
def check_data_quality(user: SchemaUsers,token: str = Depends(oauth2_scheme)):
    db_user = Modeluser(name=user.name, surname=user.surname, email=user.email, password=user.password)
    db.session.add(db_user)
    db.session.commit()
    return db_user

@router.get("/resource_data/", response_model=SchemaUsers)
def resource_data(user: SchemaUsers,  token: str = Depends(oauth2_scheme)):
    db_user = Modeluser( email=user.email, password=user.password)
    db.session.add(db_user)
    db.session.commit()
    return db_user, token


@router.get("/process_data/", response_model=SchemaUsers)
def process_data(user: SchemaUsers,  token: str = Depends(oauth2_scheme)):
    db_user = Modeluser( email=user.email, password=user.password)
    db.session.add(db_user)
    db.session.commit()
    return db_user, token

@router.get("/export_results/", response_model=SchemaUsers)
def export_results(user: SchemaUsers,  token: str = Depends(oauth2_scheme)):
    db_user = Modeluser( email=user.email, password=user.password)
    db.session.add(db_user)
    db.session.commit()
    return db_user, token


