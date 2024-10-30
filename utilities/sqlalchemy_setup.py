from sqlalchemy import create_engine,text
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

DATABASE_URL_START = "mysql+mysqlconnector://root:root@localhost:3306/"
DATABASE_URL = "mysql+mysqlconnector://root:root@localhost:3306/dbMovie"

engine = create_engine(DATABASE_URL)
engine2 = create_engine(DATABASE_URL_START)

Base = declarative_base()

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
SessionLocal2 = sessionmaker(autocommit=False, autoflush=False, bind=engine2)


session = SessionLocal()
session2 = SessionLocal2()
