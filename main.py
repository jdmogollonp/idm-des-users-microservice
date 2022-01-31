from fastapi import FastAPI
from starlette.middleware.cors import CORSMiddleware

import os
import uvicorn
from dotenv import load_dotenv
import core
from fastapi_sqlalchemy import DBSessionMiddleware, db
from api.api import api_router

from core.config import settings
from dotenv import load_dotenv

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
load_dotenv(os.path.join(BASE_DIR, ".env"))
load_dotenv(".env")

app = FastAPI()

# Set all CORS enabled origins
if core.config.settings.BACKEND_CORS_ORIGINS:
    app.add_middleware(
        CORSMiddleware,
        allow_origins=[str(origin) for origin in settings.BACKEND_CORS_ORIGINS],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )


app.add_middleware(DBSessionMiddleware, db_url=os.environ["DATABASE_URL"])
app.include_router(api_router)
