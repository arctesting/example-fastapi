from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
# import psycopg
# from psycopg.rows import dict_row
from .config import settings

# SQLALCHEMY_DATABASE_URL = f"postgresql://postgres:$password03@localhost/fastapi"
SQLALCHEMY_DATABASE_URL = f"postgresql://{settings.database_username}:{settings.database_password}@{settings.database_hostname}:{settings.database_port}/{settings.database_name}"
#SQLALCHEMY_DATABASE_URL = "postgresql://<username>:<password>@<ip-address/hostname>/<database_name>"

engine = create_engine(SQLALCHEMY_DATABASE_URL)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()

# Dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


# while True:
#     try:
#         conn = psycopg.connect(host='localhost', dbname='fastapi', user='postgres', 
#                             password='$password03', row_factory=dict_row)
#         cursor = conn.cursor()
#         print("Database connection was successful!")
#         break

#     except Exception as error:   
#         print("Connecting to database failed")
#         print("Error: ", error)
#         time.sleep(2)

#     my_post = [{"title": "title numero 1", "content": "contnent 1", "id": 1},
#             {"title": "Japan Place", "content": "Euno Station", "id": 2}]