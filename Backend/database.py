from sqlalchemy import create_engine, Column, Integer, String, ForeignKey, Text, Boolean, DateTime
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, relationship
import datetime
import os
from dotenv import load_dotenv

load_dotenv()

# Database setup
engine = create_engine(os.getenv("DATABASE_URL"))
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True, index=True)
    hashed_password = Column(String)
    full_name = Column(String)
    workspaces = relationship("Workspace", back_pop_name="owner")

class Workspace(Base):
    __tablename__ = "workspaces"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String)
    color = Column(String)
    owner_id = Column(Integer, ForeignKey("users.id"))
    owner = relationship("User", back_pop_name="workspaces")
    papers = relationship("Paper", back_pop_name="workspace")

class Paper(Base):
    __tablename__ = "papers"
    id = Column(String, primary_key=True)  # arXiv ID
    title = Column(String)
    authors = Column(Text)  # JSON string of authors
    abstract = Column(Text)
    publication_date = Column(DateTime)
    workspace_id = Column(Integer, ForeignKey("workspaces.id"))
    is_vectorized = Column(Boolean, default=False)
    workspace = relationship("Workspace", back_pop_name="papers")

# Create tables
def init_db():
    Base.metadata.create_all(bind=engine)
