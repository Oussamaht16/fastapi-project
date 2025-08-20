from random import randrange
from typing import List, Optional
import stat
import time
from fastapi import FastAPI, HTTPException, Response, status, Depends

# hadi bach n9dro ndiro extraction l data li dakhal body
from fastapi.params import Body

# pydantic is a data validation and settings management library for Python
from pydantic import BaseModel

# optional bch t9dr tsta3ml type dyal data li rah ykon optional
from typing import Optional

# psycopg2 bch na9adro nahadro m3a database mn python
import psycopg2
from psycopg2.extras import RealDictCursor
from sqlalchemy import Engine
from . import models, schemas, utils
from .database import session_local, engine, get_db
from sqlalchemy.orm import Session

# dok hna bach nhmo password te user lazam ndirolo hashing pip install passlib[bcrypt]
# from passlib.context import CryptContext


""" # hadi hia tsma bch taktivi l hash ll password
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto") """


models.Base.metadata.create_all(bind=engine)

app = FastAPI()


# dok rah ndiro la connection m3a database
while True:
    try:
        connection = psycopg2.connect(
            host="localhost",
            database="postgres",
            user="postgres",
            password="Oussama.123@github",
            cursor_factory=RealDictCursor,
        )
        cursor = connection.cursor()
        print("database was successfully connected")
        break
    except Exception as Error:
        print("connection to database failed")
        print(f"Error : {Error}")
        time.sleep(2)


# doka 9lk kyn whd dependency lazam nakatboha hia l responssable to talk with data base
# chikh 9lk hada lcode mnich hab nchofo lhna
""" def get_db():
    db = session_local()
    try:
        yield db
    finally:
        db.close() """


# dok rah n3awdo les request tawaena malawal
# get posts
@app.get(
    "/posts",
    response_model=List[
        schemas.Post
    ],  # response_model is used to validate the response data
)
def get_posts(db: Session = Depends(get_db)):
    posts = db.query(models.Post).all()
    return posts


# post a post
# hna zadna response_model f dectinnary bach nthakmo fi wach iwali baed request
@app.post("/posts", status_code=status.HTTP_201_CREATED, response_model=schemas.Post)
def create_post(post: schemas.PostCreate, db: Session = Depends(get_db)):
    """new_post = models.Post(
        title=post.title, content=post.content, published=post.published
    )"""
    new_post = models.Post(**post.dict())  # ** for unpack the dictionary
    db.add(new_post)
    db.commit()
    db.refresh(new_post)
    return new_post


# get a post by id
@app.get("/posts/{id}")
def get_post_by_id(id: int, db: Session = Depends(get_db)):
    post = db.query(models.Post).filter(models.Post.id == id).first()
    if post is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Post with id {id} not found",
        )
    return post


# delete a post by id
@app.delete("/posts/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_post(id: int, db: Session = Depends(get_db)):
    post = db.query(models.Post).filter(models.Post.id == id).first()
    if post is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Post with id {id} not found",
        )
    # delete.post(synchronize_session=False) # this is for async
    # but we are not using async so we can use this
    db.delete(post)
    db.commit()
    return Response(status_code=status.HTTP_204_NO_CONTENT)


# update a post by id
@app.put("/posts/{id}")
def update_post(id: int, post: schemas.PostCreate, db: Session = Depends(get_db)):
    post_query = db.query(models.Post).filter(models.Post.id == id)
    existing_post = post_query.first()

    if existing_post is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Post with id {id} not found",
        )

    post_query.update(post.dict(), synchronize_session=False)

    db.commit()
    return post_query.first()


# ________| _________ Users |__________
@app.get(
    "/users",
    response_model=List[
        schemas.User
    ],  # response_model is used to validate the response data
)
def get_users(db: Session = Depends(get_db)):
    users = db.query(models.Users).all()
    return users


# post a user data
# hna zadna response_model f dectinnary bach nthakmo fi wach iwali baed request
@app.post("/users", status_code=status.HTTP_201_CREATED, response_model=schemas.User)
def create_user(user: schemas.UserIn, db: Session = Depends(get_db)):
    """# hash the password before saving it to the database
    hashed_password = pwd_context.hash(user.password)
    # create a new user object with the hashed password
    user.password = hashed_password  # replace the password with the hashed password
    # hadi tari9a fi halat makach utils"""

    hash_password = utils.hash_password(user.password)
    user.password = hash_password

    new_user = models.Users(**user.dict())  # ** for unpack the dictionary
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user


# get a user data by id
@app.get("/users/{id}", response_model=schemas.User)
def get_userdata_by_id(id: int, db: Session = Depends(get_db)):
    user = db.query(models.Users).filter(models.Users.id == id).first()
    if user is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"user with id {id} not found",
        )
    return user


# delete a user by id
@app.delete("/users/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_user(id: int, db: Session = Depends(get_db)):
    user = db.query(models.Users).filter(models.Users.id == id).first()
    if user is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"user with id {id} not found",
        )
    # delete.post(synchronize_session=False) # this is for async
    # but we are not using async so we can use this
    db.delete(user)
    db.commit()
    return Response(status_code=status.HTTP_204_NO_CONTENT)


# update a user by id
@app.put("/users/{id}", response_model=schemas.User)
def update_user(id: int, user: schemas.UserIn, db: Session = Depends(get_db)):
    user_query = db.query(models.Users).filter(models.Users.id == id)
    existing_user = user_query.first()

    if existing_user is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"User with id {id} not found",
        )

    user_query.update(user.dict(), synchronize_session=False)

    db.commit()
    return user_query.first()
