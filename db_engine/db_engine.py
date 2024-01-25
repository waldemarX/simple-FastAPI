from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from os import getenv
from dotenv import load_dotenv, find_dotenv


load_dotenv(find_dotenv())
DB_PASSWORD = getenv("DB_PASSWORD")
DB_USERNAME = getenv("DB_USERNAME")

# connect to database
engine = create_engine(
    f"postgresql+psycopg2://{DB_USERNAME}:{DB_PASSWORD}@localhost/test"
)
engine.connect()

Base = declarative_base()
Base.metadata.create_all(bind=engine)

# creare session to interact with database
SessionLocal = sessionmaker(autoflush=False, bind=engine)


# open session when need and close after usage
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
