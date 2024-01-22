import os

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

MYSQL_HOST = os.environ.get("MYSQL_HOST")
MYSQL_USER = os.environ.get("MYSQL_USER")
MYSQL_PASS = os.environ.get("MYSQL_PASS")
MYSQL_DB   = os.environ.get("MYSQL_DB")


def create_db_session():
    engine = create_engine(f"mysql+mysqlconnector://{MYSQL_USER}:{MYSQL_PASS}@{MYSQL_HOST}:3306/{MYSQL_DB}")
    session = sessionmaker(bind=engine)
    session = session()
    return session