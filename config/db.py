import os
from fastapi import status
from dotenv import load_dotenv
from sqlalchemy.orm import sessionmaker
from .exceptions import DatabaseConnectionFailedException
from sqlalchemy import create_engine

load_dotenv()
url = os.getenv('DATABASE_URL') or None
if url is None:
    raise DatabaseConnectionFailedException

engine = create_engine(url=url)

session = sessionmaker(
    bind=engine,
    autoflush=False,
    autocommit=False
)

def db_connection(): 
    try:
        new_session = session()
        yield new_session
    finally:
        new_session.close()