from typing import Any, List

from fastapi import APIRouter, Body, Depends, HTTPException
from fastapi.encoders import jsonable_encoder
from pydantic.networks import EmailStr
from sqlalchemy.orm import Session

#from app import crud, models, schemas
#from app.api import deps
from core.config import Settings
from core.security import generate_confirmation_token, confirm_token

from utils import send_new_account_email, send_ses

import os

import uvicorn
from dotenv import load_dotenv
from fastapi import FastAPI
from fastapi_sqlalchemy import DBSessionMiddleware, db
from fastapi.security import HTTPBearer
from models.user import User as Modeluser
from schemas.users import Users as SchemaUsers, UserDelete

from schemas.users import UserCreate as SchemaUserCreate

import crud, models, schemas
import logging

router = APIRouter()

from api import deps

settings= Settings()

security = HTTPBearer()


@router.post("/signup/", response_model=SchemaUsers)
def create_user(user_in: SchemaUsers, db: Session = Depends(deps.get_db) ):
    user = crud.user.get_by_email( email=user_in.email)
    if user:
        raise HTTPException(
            status_code=400,
            detail="The user with this username or email already exists in the system.",
        )
    user = crud.user.create( obj_in=user_in)
    if settings.EMAILS_ENABLED and user_in.email:
        token = generate_confirmation_token(user_in.email)
        send_ses(
            email_to=user_in.email, username=user_in.email, password=user_in.password, email_token = token
        )
    return user

@router.post("/confirm/<token>")
def confirm_email(token: str):
    try:
        email = confirm_token(token)
    except:
        raise HTTPException(
            status_code=400,
            detail="The confirmation link is invalid or has expired. ",
        )
    user = crud.user.get_by_email( email=email)
    if not user:
        raise HTTPException(
            status_code=400,
            detail="Email already confirmed",
        )
    else:
        user.confirmed = True
        db.session.add(user)
        db.session.commit()
        logging.info("User confirmed")
        return True

@router.post("/delete_account/")
def delete_account(user_in: UserDelete,token: str = Depends(security)):
    user = crud.user.get_by_email( email=user_in.email)
    if not user:
        raise HTTPException(
            status_code=400,
            detail="User not found",
        )
    else:
        response = crud.user.delete( email=user_in.email)
        if response:
            logging.info("User deleted")
            return 200




"""
@router.put("/update_password/", response_model=SchemaUsers)
def add_user(user: SchemaUsers,  token: str = Depends(oauth2_scheme)):
    db_user = Modeluser( email=user.email, password=user.password)
    db.session.add(db_user)
    db.session.commit()
    return db_user, token


@router.post("/reset_password/", response_model=SchemaUsers)
def add_user(user: SchemaUsers,  token: str = Depends(oauth2_scheme)):
    db_user = Modeluser( email=user.email, password=user.password)
    db.session.add(db_user)
    db.session.commit()
    return db_user, token

@router.post("/delete_account/", response_model=SchemaUsers)
def add_user(user: SchemaUsers,  token: str = Depends(oauth2_scheme)):
    db_user = Modeluser( email=user.email, password=user.password)
    db.session.add(db_user)
    db.session.commit()
    return db_user, token

"""
