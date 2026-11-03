from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from.config import settings

# The @ in the password must be URL-encoded.
# url = f'postgresql+psycopg2://postgres:somnath%40123@localhost/fastapi_db'
#url = f'postgresql://{settings.database_username}:{settings.database_password}@{settings.database_hostname}/{settings.database_name}'
url= settings.database_url
engine = create_engine(url=url)
session_local = sessionmaker(bind=engine, autoflush=False, autocommit=False)
Base = declarative_base()
def get_db():
    db=session_local()
    try:
        yield db
    finally:
        db.close()
 
# import psycopg2  
# import time
# while True:
#     try:
#         conn=psycopg2.connect(host='localhost',database='fastapi_db',user='postgres',password='somnath@123',cursor_factory=RealDictCursor)
#         cursor = conn.cursor()
#         break
#     except Exception as error:
#         print('connecting to database failed')
#         print ('Error',error)
#         time.sleep(2)
# those route will be called first that are defined first if the same route is defined multiple times

 