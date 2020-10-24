from sqlalchemy import create_engine, Column, Integer, String, ForeignKey
from sqlalchemy.ext.declarative import declarative_base

engine = create_engine("sqlite:///test.db", echo=True)

Base = declarative_base()

class User(Base):
    __tablename__ = "user"

    id = Column("id", Integer, primary_key=True)
    first_name = Column("first_name", String)
    last_name = Column("last_name", String)
    username = Column("username", String, unique=True)

    
Base.metadata.create_all(bind=engine)