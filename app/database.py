from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from .config import settings

# hado jabnahom brk elajal bch nchofo la cnx mea database njhat wla lala
import time
import psycopg2
from psycopg2.extras import RealDictCursor


# hadi tchtarit ano database deja endk f database

# hna had l file ftahnah bch mana ndiro create l table bla ma nadakhlo ll pg admin

""" SQLALCHEMY_DATABASE_URL = 'postgresql:// postgres:password@ip_adress/database_name ' """

""" SQLALCHEMY_DATABASE_URL = f"postgresql://{settings.database_username}:{settings.database_password}@{settings.database_hostname}:{settings.database_port}/{settings.database_name}"
 """


# hadi nafsha li rahi lfo9 mais hadi khir
from sqlalchemy.engine.url import URL

SQLALCHEMY_DATABASE_URL = URL.create(
    drivername="postgresql",
    username=settings.database_username,
    password=settings.database_password,
    host=settings.database_hostname,
    port=settings.database_port,
    database=settings.database_name,
)

engine = create_engine(SQLALCHEMY_DATABASE_URL)

session_local = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()

# hna lsl hado homa lkhotowat li lazam ndirohom bch nhalo database mn python with sqlalchemy


def get_db():
    db = session_local()
    try:
        yield db
    finally:
        db.close()


# hada yaetik ida la connexion mea database najhat

while True:
    try:
        connection = psycopg2.connect(
            host=settings.database_hostname,
            database=settings.database_name,
            user=settings.database_username,
            password=settings.database_password,
            cursor_factory=RealDictCursor,
        )
        cursor = connection.cursor()
        print("database was successfully connected")
        break
    except Exception as Error:
        print("connection to database failed")
        print(f"Error : {Error}")
        time.sleep(2)
