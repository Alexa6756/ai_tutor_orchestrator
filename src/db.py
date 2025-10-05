# from sqlalchemy import create_engine, Column, Integer, String, JSON, DateTime
# from sqlalchemy.ext.declarative import declarative_base
# from sqlalchemy.orm import sessionmaker
# import datetime
# import os
# from dotenv import load_dotenv

# load_dotenv()

# DATABASE_URL = os.getenv("DATABASE_URL", "sqlite:///./app.db")


# connect_args = {"check_same_thread": False} if DATABASE_URL.startswith("sqlite") else {}

# engine = create_engine(DATABASE_URL, connect_args=connect_args)
# SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
# Base = declarative_base()

# class User(Base):
#     __tablename__ = "users"
#     id = Column(Integer, primary_key=True, index=True)
#     user_id = Column(String, unique=True, index=True)
#     user_info = Column(JSON)
#     conversation_history = Column(JSON)
#     last_interaction = Column(DateTime, default=datetime.datetime.utcnow)

# def init_db():
#     Base.metadata.create_all(bind=engine)

from sqlalchemy import create_engine, Column, Integer, String, JSON, DateTime
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import datetime


DATABASE_URL = "postgresql://ai_tutor_user:Alexa2005@localhost:5432/ai_tutor_db"

engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(String, unique=True, index=True)
    user_info = Column(JSON)
    conversation_history = Column(JSON)
    last_interaction = Column(DateTime, default=datetime.datetime.utcnow)

def init_db():
    Base.metadata.create_all(bind=engine)


if __name__ == "__main__":
    init_db()
