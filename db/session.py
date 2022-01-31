from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
import os
from core.config import settings
from dotenv import load_dotenv

#engine = create_engine(settings.SQLALCHEMY_DATABASE_URI, pool_pre_ping=True)

#from fastapi_sqlalchemy import DBSessionMiddleware, db
#SessionLocal = db.session

#SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
load_dotenv(os.path.join(BASE_DIR, ".env"))
load_dotenv(".env")


engine = create_engine(os.environ["DATABASE_URL"], pool_pre_ping=True)




SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
